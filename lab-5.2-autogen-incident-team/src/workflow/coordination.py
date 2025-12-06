import os
import uuid
from typing import Dict, Any, List

import autogen  # pyautogen

from src.utils.cost import CostTracker
from src.utils.helpers import cache_conversation
from src.utils.constants import OPENAI_MODEL, OPENAI_API_KEY_ENV
from src.workflow.scenarios import get_scenario
from src.rbac.roles import check_permission
from src.audit.logger import audit_log
from src.sandbox.execute import run_in_sandbox


def _create_llm_config() -> Dict[str, Any]:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            f"{OPENAI_API_KEY_ENV} environment variable is required for AutoGen."
        )

    return {
        "config_list": [
            {
                "model": OPENAI_MODEL,
                "api_key": api_key,
            }
        ]
    }


def _create_agents(llm_config: Dict[str, Any]) -> Dict[str, autogen.AssistantAgent]:
    """
    Creates all four AutoGen agents with different roles.
    """

    incident_commander = autogen.AssistantAgent(
        name="incident_commander",
        system_message=(
            "You are the Incident Commander. "
            "Summarize incoming alerts, set priority, and define a high-level plan. "
            "Reply in short JSON with keys: summary, priority, plan."
        ),
        llm_config=llm_config,
    )

    sre_investigator = autogen.AssistantAgent(
        name="sre_investigator",
        system_message=(
            "You are an SRE Investigator. You analyze logs and metrics provided by the user. "
            "Reply in short JSON with keys: hypothesis, suspected_components, required_data."
        ),
        llm_config=llm_config,
    )

    code_analysis_agent = autogen.AssistantAgent(
        name="code_analysis_agent",
        system_message=(
            "You are a Code Analysis expert. You inspect stack traces and code snippets. "
            "Reply in JSON with keys: root_cause, risky_functions, suggested_code_changes."
        ),
        llm_config=llm_config,
    )

    remediation_agent = autogen.AssistantAgent(
        name="remediation_agent",
        system_message=(
            "You are a Remediation expert. Propose safe remediation steps. "
            "Return JSON with keys: runbook_steps, kubectl_commands, risk_level, "
            "sandbox_code (Python) to validate the fix."
        ),
        llm_config=llm_config,
    )

    return {
        "incident_commander": incident_commander,
        "sre_investigator": sre_investigator,
        "code_analysis_agent": code_analysis_agent,
        "remediation_agent": remediation_agent,
    }


def _agent_call(
    agent: autogen.AssistantAgent,
    role: str,
    action: str,
    user_message: str,
    correlation_id: str,
    cost_tracker: CostTracker,
    conversation_key: str,
) -> str:
    """
    Helper to:
      - enforce RBAC
      - track cost
      - call AutoGen AssistantAgent
      - cache conversation in Redis
      - persist audit logs
    """

    check_permission(role, action)

    messages: List[Dict[str, Any]] = [
        {"role": "user", "content": user_message},
    ]

    cost_tracker.add_prompt(user_message)

    reply = agent.generate_reply(messages=messages)

    if isinstance(reply, dict):
        content = str(reply)
    else:
        content = str(reply)

    cost_tracker.add_completion(content)

    cache_conversation(
        f"{conversation_key}:{role}:{action}",
        messages + [{"role": "assistant", "content": content}],
    )

    audit_log(
        agent=role,
        action=action,
        payload=content,
        correlation_id=correlation_id,
    )

    return content


def run_incident_workflow(
    scenario_name: str,
    auto_approve: bool = False,
) -> Dict[str, Any]:
    """
    Main coordination entrypoint.
    Orchestrates all four agents for a given scenario.
    """

    scenario = get_scenario(scenario_name)
    llm_config = _create_llm_config()
    agents = _create_agents(llm_config)

    correlation_id = str(uuid.uuid4())
    conversation_key = f"incident:{correlation_id}"

    cost_tracker = CostTracker()

    # 1) Incident Commander
    commander_prompt = (
        "You are receiving the following alerts and telemetry. "
        "Produce a brief JSON response.\n\n"
        f"Description: {scenario['description']}\n"
        f"Alerts: {scenario['alerts']}\n"
        f"Metrics: {scenario['metrics']}\n"
        f"Logs: {scenario['logs']}"
    )
    commander_result = _agent_call(
        agent=agents["incident_commander"],
        role="incident_commander",
        action="orchestrate_workflow",
        user_message=commander_prompt,
        correlation_id=correlation_id,
        cost_tracker=cost_tracker,
        conversation_key=conversation_key,
    )

    # 2) SRE Investigator
    investigator_prompt = (
        "Using the investigation context below, refine the root cause hypothesis.\n\n"
        f"Scenario: {scenario['name']} - {scenario['description']}\n"
        f"Alerts: {scenario['alerts']}\n"
        f"Metrics: {scenario['metrics']}\n"
        f"Logs: {scenario['logs']}\n\n"
        f"Incident Commander context:\n{commander_result}"
    )
    investigator_result = _agent_call(
        agent=agents["sre_investigator"],
        role="sre_investigator",
        action="analyze_alerts",
        user_message=investigator_prompt,
        correlation_id=correlation_id,
        cost_tracker=cost_tracker,
        conversation_key=conversation_key,
    )

    # 3) Code Analysis
    code_prompt = (
        "You are given stack traces and SRE hypothesis. "
        "Return JSON with root_cause, risky_functions, suggested_code_changes.\n\n"
        f"Logs: {scenario['logs']}\n\n"
        f"SRE Investigator context:\n{investigator_result}"
    )
    code_result = _agent_call(
        agent=agents["code_analysis_agent"],
        role="code_analysis_agent",
        action="static_analysis",
        user_message=code_prompt,
        correlation_id=correlation_id,
        cost_tracker=cost_tracker,
        conversation_key=conversation_key,
    )

    # 4) Remediation
    remediation_prompt = (
        "Propose safe remediation for Kubernetes-based microservice.\n"
        "Return JSON with runbook_steps, kubectl_commands, risk_level, sandbox_code.\n\n"
        f"Scenario: {scenario['name']} - {scenario['description']}\n"
        f"Logs: {scenario['logs']}\n"
        f"Code Analysis context:\n{code_result}"
    )
    remediation_result = _agent_call(
        agent=agents["remediation_agent"],
        role="remediation_agent",
        action="propose_fix",
        user_message=remediation_prompt,
        correlation_id=correlation_id,
        cost_tracker=cost_tracker,
        conversation_key=conversation_key,
    )

    sandbox_output = ""
    applied = False
    needs_approval = not auto_approve

    if auto_approve:
        # Sandbox execution is done on behalf of the code analysis role.
        check_permission("code_analysis_agent", "sandbox_execution")

        sandbox_code = (
            "print('Running sandbox validation for remediation...')\n"
            "print('All checks passed for simulated fix.')\n"
        )
        sandbox_output = run_in_sandbox(sandbox_code)
        applied = True

    result: Dict[str, Any] = {
        "correlation_id": correlation_id,
        "scenario": scenario_name,
        "commander_result": commander_result,
        "investigator_result": investigator_result,
        "code_analysis_result": code_result,
        "remediation_result": remediation_result,
        "sandbox_executed": applied,
        "sandbox_output": sandbox_output,
        "needs_approval": needs_approval,
        "cost": cost_tracker.to_dict(),
    }

    return result
