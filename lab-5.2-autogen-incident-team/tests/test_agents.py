from src.agents.commander import CommanderAgent
from src.agents.investigator import InvestigatorAgent
from src.agents.code_analysis import CodeAnalysisAgent
from src.agents.remediation import RemediationAgent


def test_agents_initialization():
    api_key = "dummy-key"
    model = "gpt-4o-mini"

    commander = CommanderAgent(api_key=api_key, model=model)
    investigator = InvestigatorAgent(api_key=api_key, model=model)
    code_agent = CodeAnalysisAgent(api_key=api_key, model=model)
    remediation = RemediationAgent(api_key=api_key, model=model)

    assert commander.name == "incident_commander"
    assert investigator.name == "sre_investigator"
    assert code_agent.name == "code_analysis_agent"
    assert remediation.name == "remediation_agent"
