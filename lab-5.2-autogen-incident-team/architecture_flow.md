# 🧩 Architecture Flow — Multi-Agent AutoGen IR System

This document explains **how the system works end-to-end** so students understand the logic before modifying or extending it.

---

## 🏗 High-Level Architecture

```
 Incoming Alert
        |
        v
+--------------------+
|  FastAPI Backend   |
+--------------------+
        |
        v
+--------------------+
| Incident Pipeline  |
+--------------------+
        |
        v
+----------------------------+
| Multi-Agent Orchestration  |
+----------------------------+
  |         |         |      |
  v         v         v      v
Commander  SRE      Code  Remediation
 Agent   Investigator Analysis  Agent
                     Agent
```

Each agent has a **role, responsibilities, and permissions**.

---

## 🤖 Agent Responsibilities

| Agent | Purpose | Allowed Actions | Not Allowed |
|-------|---------|----------------|-------------|
| **Incident Commander** | Coordinates workflow & prioritization | delegate, approve | execute code |
| **SRE Investigator** | Diagnoses symptoms from logs & metrics | analyze alerts | deploy or change system |
| **Code Analysis Agent** | Reviews code patterns, risks, root causes | static analysis, sandbox execution | deploying fixes |
| **Remediation Agent** | Suggests safe operational fixes | propose runbooks | executing unapproved code |

---

## 🔐 RBAC Enforcement

Every agent action passes through:

```
check_permission(role, action)
```

If action is not explicitly in `allow:` list → system blocks it.

Example:

```
role=remediation_agent
action=sandbox_execution ❌ (blocked)
```

Only `code_analysis_agent` can perform sandbox execution.

---

## 🗄 Audit Logging Flow

Every message or decision is stored with:

- Agent name  
- Action performed  
- Timestamp  
- Correlation ID  
- Full content  

Stored in PostgreSQL:

```
audit_records
```

This creates a **forensic trail** like real enterprise IR platforms.

---

## 🧠 Conversation Memory & Caching

Each agent message session is stored in Redis using:

```
incident:{correlation_id}:{agent}:{action}
```

This enables:

- Replay
- Debugging
- Training future agent improvements

---

## 🧪 Safe Code Execution (Sandbox)

The system NEVER runs code directly.

Instead:

```
code → validate → sandbox → isolated Docker container
```

Sandbox includes:

| Restricted | Allowed |
|-----------|---------|
| network | print() |
| file system write | loops |
| subprocess | algorithm checks |
| os/system modules | safe logic |

Denylist protects the host from malicious execution.

---

## 🌀 Incident Execution Sequence

1. **Incident Commander**  
   Reads alert and creates summary + priority.

2. **SRE Investigator**  
   Processes logs + metrics → hypothesis.

3. **Code Analysis Agent**  
   Reviews suspected code patterns.

4. **Remediation Agent**  
   Suggests safe runbook and (optional) code fix.

5. (Optional) **Sandbox execution** validates fix.

6. **Final JSON report with cost + audit ID returned.**

---

## 📈 Cost Tracking

We count estimated tokens per agent response and show:

```
{
  "prompt_tokens": 1200,
  "completion_tokens": 1600,
  "estimated_cost_usd": 0.0031
}
```

This teaches **LLM cost awareness**.

---

## 🧩 Summary of Data Flow

```
Request → Pipeline → Coordinator → Agents
                 ↙︎         ↘︎
             Redis        PostgreSQL
                 ↘︎       ↙︎
              Sandbox (optional)
```

---

## 🎯 Learning Outcomes

Students now understand:

- How multi-agent systems cooperate
- Why RBAC + sandboxing is mandatory in production
- How audits and memory enable real compliance
- How LLM reasoning can automate root-cause analysis

---

You're now ready to:

- Extend the system  
- Add new agents  
- Add new scenarios  
- Integrate Slack/Jira/PagerDuty  
- Deploy to Kubernetes/EKS  

