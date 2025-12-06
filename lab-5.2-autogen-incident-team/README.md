# Lab 5.2 PAID Version – AutoGen Multi-Agent Incident Response System
## Enterprise-Grade AI Agent Team for DevOps Automation

---

## 🎯 What You Will Learn

### Core Concepts

By completing this lab, you will master:

1. **Production Multi-Agent Systems** - Enterprise AI orchestration:
   - **4-agent architecture**: Commander, Investigator, Code Analyst, Remediator
   - **Agent orchestration**: Complex multi-agent workflows
   - **Role-based permissions**: RBAC for each agent
   - **Approval workflows**: Human-in-the-loop for critical actions
   - **Agent coordination**: Consensus building and escalation

2. **Secure Agent Execution** - Production-grade safety:
   - **Docker sandboxing**: Isolated execution environments
   - **Resource limits**: CPU, memory, and network constraints
   - **Read-only filesystem**: Preventing unauthorized modifications
   - **Seccomp profiles**: System call filtering
   - **Audit trails**: Complete investigation logging

3. **Enterprise Incident Response** - Real-world automation:
   - **Automated triage**: AI-powered alert classification
   - **Multi-stage investigation**: Specialists collaborating
   - **Code analysis**: AI reviewing logs and code
   - **Safe remediation**: Validated fix generation
   - **Full audit compliance**: PostgreSQL logging

4. **Advanced AutoGen Patterns** - Complex workflows:
   - **Multi-agent conversations**: 4-way agent coordination
   - **Conditional routing**: Dynamic agent selection
   - **Tool integration**: Sandboxed command execution
   - **State management**: Tracking complex workflows
   - **Error handling**: Graceful degradation

### Practical Skills

You will be able to:

- ✅ Build 4+ agent systems with AutoGen
- ✅ Implement Docker sandboxes for safe execution
- ✅ Design RBAC systems for agent permissions
- ✅ Create PostgreSQL audit logging
- ✅ Orchestrate complex multi-agent workflows
- ✅ Build approval workflows for critical actions
- ✅ Test agent systems at scale
- ✅ Monitor and debug multi-agent conversations

### Real-World Applications

**Enterprise SRE Teams** will learn:
- Building production IR automation
- Multi-specialist agent coordination
- Secure tool execution frameworks
- Compliance-ready audit logging

**DevOps Platform Engineers** will learn:
- Deploying multi-agent systems
- Container-based sandboxing
- RBAC implementation for AI
- Production observability

**Security Teams** will learn:
- Sandboxed AI execution
- Permission frameworks
- Audit trail implementation
- Risk mitigation strategies

**AI/ML Teams** will learn:
- Production multi-agent deployment
- Complex agent orchestration
- State management at scale
- Enterprise LLM integration

---

## 📋 Prerequisites

### Required Software
- **Docker:** Version 24+ with Docker Compose
- **Python:** Version 3.11 or higher
- **PostgreSQL:** Version 15+ (via Docker)
- **curl:** For API testing

### Required API Keys
- **OpenAI API Key:** For LLM-powered agents
  ```bash
  export OPENAI_API_KEY="sk-your-key-here"
  ```

### Required Knowledge
- Completion of Lab 5.2 FREE version (strongly recommended)
- Advanced AutoGen framework understanding
- Docker and containerization concepts
- PostgreSQL and SQL basics
- RBAC and security principles
- Incident response workflows

### Verification Commands

```bash
# Check Docker and Compose
docker --version
docker compose version

# Check Python
python3 --version

# Check PostgreSQL client (optional)
psql --version
```

---

## 🏗️ Architecture Overview

### What You're Building

```
┌─────────────────────────────────────────────────────────────────────┐
│              Enterprise Multi-Agent Incident Response                │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Alert Input (Prometheus / PagerDuty / Manual)             │    │
│  │  {                                                          │    │
│  │    "alert": "Memory leak in auth-service",                 │    │
│  │    "severity": "critical",                                  │    │
│  │    "service": "auth-service",                               │    │
│  │    "namespace": "production"                                │    │
│  │  }                                                          │    │
│  └────────────────────────┬───────────────────────────────────┘    │
│                           │                                          │
│                           ▼                                          │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Agent 1: Incident Commander                               │    │
│  │  Role: Orchestration and Decision Making                   │    │
│  │                                                            │    │
│  │  Responsibilities:                                         │    │
│  │  ├─ Receive and classify alerts                            │    │
│  │  ├─ Assess severity and impact                             │    │
│  │  ├─ Route to appropriate specialist agents                 │    │
│  │  ├─ Coordinate multi-agent workflows                       │    │
│  │  ├─ Make escalation decisions                              │    │
│  │  ├─ Approve remediation plans                              │    │
│  │  └─ Generate final incident reports                        │    │
│  │                                                            │    │
│  │  Permissions:                                              │    │
│  │  ✓ Read all investigations                                 │    │
│  │  ✓ Delegate to any specialist                              │    │
│  │  ✓ Approve/reject remediation                              │    │
│  │  ✗ Execute commands directly                               │    │
│  │                                                            │    │
│  │  LLM: GPT-4 (for complex decision making)                 │    │
│  └────────────────┬───────────────────────────────────────────┘    │
│                   │                                                  │
│                   │ Delegates to specialists:                        │
│                   │                                                  │
│        ┌──────────┴──────────┬────────────────┬──────────────┐    │
│        │                     │                │              │    │
│        ▼                     ▼                ▼              ▼    │
│  ┌────────────┐      ┌────────────┐   ┌────────────┐  ┌─────────┐ │
│  │ Agent 2:   │      │ Agent 3:   │   │ Agent 4:   │  │ Sandbox │ │
│  │ SRE        │      │ Code       │   │ Remediation│  │ Docker  │ │
│  │ Investigator│     │ Analyst    │   │ Planner    │  │ Container│ │
│  └────────────┘      └────────────┘   └────────────┘  └─────────┘ │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Agent Details

```
┌─────────────────────────────────────────────────────────────┐
│  Agent 2: SRE Investigator                                  │
│  Role: Technical Diagnostics                                │
│                                                             │
│  Responsibilities:                                          │
│  ├─ Diagnose system symptoms                                │
│  ├─ Analyze pod health and resource usage                   │
│  ├─ Review recent deployments and changes                   │
│  ├─ Check metrics and logs                                  │
│  ├─ Identify probable root causes                           │
│  └─ Report findings to Commander                            │
│                                                             │
│  Permissions:                                               │
│  ✓ Read pod status (via sandbox)                            │
│  ✓ Read logs (via sandbox)                                  │
│  ✓ Query metrics                                            │
│  ✗ Modify resources                                         │
│  ✗ Execute remediation                                      │
│                                                             │
│  Tools:                                                     │
│  - kubectl get (read-only, sandboxed)                       │
│  - kubectl describe (sandboxed)                             │
│  - kubectl logs (sandboxed)                                 │
│  - Prometheus queries                                       │
│                                                             │
│  LLM: GPT-4 (for technical analysis)                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Agent 3: Code Analysis Agent                               │
│  Role: Code and Log Analysis                                │
│                                                             │
│  Responsibilities:                                          │
│  ├─ Review error logs and stack traces                      │
│  ├─ Analyze recent code changes                             │
│  ├─ Identify code-level issues                              │
│  ├─ Detect patterns (memory leaks, race conditions)         │
│  ├─ Assess code quality and risks                           │
│  └─ Report findings and recommendations                     │
│                                                             │
│  Permissions:                                               │
│  ✓ Read application logs                                    │
│  ✓ Review code diffs                                        │
│  ✓ Static analysis (sandboxed)                              │
│  ✗ Modify code                                              │
│  ✗ Deploy changes                                           │
│                                                             │
│  Tools:                                                     │
│  - Log parser (sandboxed)                                   │
│  - Pattern matcher                                          │
│  - Code reviewer (AI-powered)                               │
│  - Stack trace analyzer                                     │
│                                                             │
│  LLM: GPT-4 (for code understanding)                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Agent 4: Remediation Planner                               │
│  Role: Fix Generation and Validation                        │
│                                                             │
│  Responsibilities:                                          │
│  ├─ Synthesize findings from all agents                     │
│  ├─ Generate remediation plans                              │
│  ├─ Validate safety of proposed actions                     │
│  ├─ Create rollback plans                                   │
│  ├─ Estimate impact and risk                                │
│  └─ Submit for Commander approval                           │
│                                                             │
│  Permissions:                                               │
│  ✓ Propose remediation actions                              │
│  ✓ Generate kubectl commands                                │
│  ✓ Create rollback procedures                               │
│  ✗ Execute commands (requires approval)                     │
│  ✗ Auto-deploy fixes                                        │
│                                                             │
│  Tools:                                                     │
│  - Command generator                                        │
│  - Safety validator                                         │
│  - Impact estimator                                         │
│  - Rollback planner                                         │
│                                                             │
│  LLM: GPT-4 (for remediation planning)                     │
└─────────────────────────────────────────────────────────────┘
```

### 4-Agent Workflow

```
Step 1: Alert Reception
    ↓
┌──────────────────────────────────────────┐
│  Incident Commander                      │
│  - Receives alert                        │
│  - Classifies severity                   │
│  - Initiates investigation workflow      │
└──────────────┬───────────────────────────┘
               │
               │ Parallel delegation:
               │
    ┌──────────┴─────────┬──────────────┐
    │                    │              │
    ▼                    ▼              ▼
┌─────────┐      ┌──────────────┐  ┌─────────┐
│ SRE     │      │ Code         │  │ (ready) │
│ Agent   │      │ Analyst      │  │         │
└────┬────┘      └──────┬───────┘  └─────────┘
     │                  │
     │ Investigation    │ Code Analysis
     │                  │
     ▼                  ▼
┌──────────────────────────────────────────┐
│  Findings Aggregation                    │
│  - System diagnostics                    │
│  - Code-level issues                     │
│  - Root cause hypothesis                 │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  Remediation Planner                     │
│  - Synthesizes all findings              │
│  - Generates fix plan                    │
│  - Validates safety                      │
│  - Creates rollback procedure            │
└──────────────┬───────────────────────────┘
               │
               │ Submits for approval
               │
               ▼
┌──────────────────────────────────────────┐
│  Incident Commander                      │
│  - Reviews proposed remediation          │
│  - Assesses risk                         │
│  - APPROVES or REJECTS                   │
│  - Logs decision                         │
└──────────────┬───────────────────────────┘
               │
               ▼ (if approved)
┌──────────────────────────────────────────┐
│  Execution in Docker Sandbox             │
│  - Isolated environment                  │
│  - Resource limited                      │
│  - Audited execution                     │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  PostgreSQL Audit Log                    │
│  - Complete investigation trail          │
│  - All agent messages                    │
│  - Decisions and approvals               │
│  - Execution results                     │
└──────────────────────────────────────────┘
```

---

## 🛡️ Docker Sandbox Security

### Sandbox Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Docker Sandbox Container                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Security Constraints                             │  │
│  │  ├─ Read-only filesystem (except /tmp)            │  │
│  │  ├─ CPU limit: 0.5 cores                          │  │
│  │  ├─ Memory limit: 512MB                           │  │
│  │  ├─ No network by default                         │  │
│  │  ├─ Seccomp profile: restrict syscalls            │  │
│  │  ├─ No privileged operations                      │  │
│  │  └─ Time limit: 30 seconds max                    │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Allowed Operations                               │  │
│  │  ✓ kubectl get (read-only)                        │  │
│  │  ✓ kubectl describe (read-only)                   │  │
│  │  ✓ kubectl logs (read-only)                       │  │
│  │  ✓ grep, awk, sed (text processing)              │  │
│  │  ✓ Python scripts (in /tmp)                       │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Blocked Operations                               │  │
│  │  ✗ kubectl delete                                  │  │
│  │  ✗ kubectl apply/create                            │  │
│  │  ✗ kubectl exec                                    │  │
│  │  ✗ System modifications                            │  │
│  │  ✗ Network access (unless approved)               │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Sandbox Configuration

```dockerfile
FROM alpine:3.18
# Read-only filesystem
RUN mkdir -p /tmp && chmod 1777 /tmp
# Limited tools
RUN apk add --no-cache kubectl grep sed awk python3
# Security user
RUN adduser -D -u 1000 sandbox
USER sandbox
# Resource limits enforced by Docker
```

**docker-compose.yml:**
```yaml
sandbox:
  image: sandbox:latest
  read_only: true
  security_opt:
    - no-new-privileges:true
    - seccomp:unconfined  # Custom seccomp profile
  cpus: 0.5
  mem_limit: 512m
  network_mode: none
  tmpfs:
    - /tmp:size=100m
```

---

## 🗄️ PostgreSQL Audit Logging

### Database Schema

```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    investigation_id UUID UNIQUE NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    
    -- Alert details
    alert_type VARCHAR(100),
    service_name VARCHAR(100),
    severity VARCHAR(20),
    namespace VARCHAR(100),
    
    -- Agent interactions
    commander_messages JSONB,
    investigator_messages JSONB,
    code_analyst_messages JSONB,
    remediation_messages JSONB,
    
    -- Decisions
    root_cause TEXT,
    proposed_remediation JSONB,
    commander_approval BOOLEAN,
    approval_reason TEXT,
    
    -- Execution
    sandbox_commands JSONB,
    execution_results JSONB,
    execution_status VARCHAR(20),
    
    -- Metrics
    total_tokens INTEGER,
    cost_usd DECIMAL(10, 6),
    duration_seconds INTEGER,
    
    -- Outcome
    incident_resolved BOOLEAN,
    human_intervention_required BOOLEAN,
    
    -- Indexes for fast queries
    INDEX idx_investigation_id (investigation_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_service (service_name),
    INDEX idx_severity (severity)
);
```

### Audit Query Examples

```sql
-- Find all critical incidents
SELECT * FROM audit_logs 
WHERE severity = 'critical' 
ORDER BY timestamp DESC;

-- Cost analysis by service
SELECT 
    service_name,
    COUNT(*) as incidents,
    SUM(cost_usd) as total_cost,
    AVG(duration_seconds) as avg_duration
FROM audit_logs
GROUP BY service_name;

-- Approval rate
SELECT 
    commander_approval,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage
FROM audit_logs
GROUP BY commander_approval;
```

---

## 📁 Repository Structure

```
lab-05.2-autogen-incident-response-paid/
├── README.md                   ← This file
├── setup.md                    ← Detailed setup guide
├── docker-compose.yml          ← Full stack orchestration
├── Dockerfile.api              ← FastAPI application
├── Dockerfile.sandbox          ← Secure sandbox container
├── requirements.txt            ← Python dependencies
├── .env.example                ← Environment template
├── src/
│   ├── main.py                 ← FastAPI application entry
│   ├── agents/
│   │   ├── commander.py        ← Incident Commander
│   │   ├── investigator.py     ← SRE Investigator
│   │   ├── code_analyst.py     ← Code Analysis Agent
│   │   ├── remediator.py       ← Remediation Planner
│   │   └── orchestrator.py     ← Multi-agent workflow
│   ├── sandbox/
│   │   ├── executor.py         ← Sandbox command execution
│   │   └── security.py         ← Permission validation
│   ├── db/
│   │   ├── models.py           ← SQLAlchemy models
│   │   ├── audit.py            ← Audit logging
│   │   └── connection.py       ← Database connection
│   ├── rbac/
│   │   ├── permissions.py      ← Agent permissions
│   │   └── policies.py         ← RBAC policies
│   └── utils/
│       ├── config.py           ← Configuration
│       └── metrics.py          ← Monitoring
├── scenarios/
│   ├── memory_leak.json        ← Memory leak scenario
│   ├── cpu_spike.json          ← CPU spike scenario
│   ├── crashloop.json          ← CrashLoopBackOff
│   └── cascading_failure.json  ← Cascading failure
├── scripts/
│   ├── test_all.sh             ← Test all scenarios
│   ├── load_test.sh            ← Load testing
│   └── cleanup.sh              ← Cleanup resources
└── tests/
    ├── test_agents.py          ← Agent unit tests
    ├── test_sandbox.py         ← Sandbox security tests
    ├── test_rbac.py            ← RBAC tests
    ├── test_audit.py           ← Audit logging tests
    └── test_integration.py     ← End-to-end tests
```

---

## 🚀 Quick Start Guide

### Step 1: Start Full Stack

```bash
docker compose up --build -d
```

**Expected Output:**
```
[+] Running 5/5
 ✔ Network autogen-paid_default      Created
 ✔ Container postgres                Started
 ✔ Container sandbox                 Started
 ✔ Container autogen-api             Started
 ✔ Container prometheus              Started
 ✔ Container grafana                 Started
```

### Step 2: Verify Services

```bash
docker compose ps
```

**Expected:**
```
NAME              STATUS              PORTS
autogen-api       Up 30 seconds       0.0.0.0:8000->8000/tcp
postgres          Up 32 seconds       0.0.0.0:5432->5432/tcp
sandbox           Up 30 seconds       (no ports)
prometheus        Up 30 seconds       0.0.0.0:9090->9090/tcp
grafana           Up 30 seconds       0.0.0.0:3000->3000/tcp
```

### Step 3: Trigger Investigation

```bash
curl -X POST http://localhost:8000/incident \
  -H "Content-Type: application/json" \
  -d '{
    "alert": "Memory leak detected in auth-service",
    "severity": "critical",
    "service": "auth-service",
    "namespace": "production"
  }'

  curl -X POST http://localhost:8000/incident/run \
  -H "Content-Type: application/json" \
  -d '{"scenario": "memory_leak", "auto_approve": false}'
```

---

## 📊 Expected Output

### Complete Investigation Response

```json
{
  "investigation_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-15T10:30:00Z",
  "alert": {
    "alert": "Memory leak detected in auth-service",
    "severity": "critical",
    "service": "auth-service",
    "namespace": "production"
  },
  "workflow": {
    "commander_decision": {
      "action": "escalate_to_specialists",
      "reasoning": "Critical severity requires multi-specialist analysis",
      "delegated_to": ["SREInvestigator", "CodeAnalyst"]
    },
    "investigation": {
      "sre_findings": {
        "pod_status": "Running but high memory usage (1.8GB/2GB)",
        "recent_changes": "Deployment v2.3.0 deployed 3 hours ago",
        "metrics": {
          "memory_growth": "50MB/hour sustained",
          "restart_count": 0,
          "cpu_usage": "normal"
        },
        "diagnosis": "Probable memory leak in new deployment"
      },
      "code_analysis": {
        "log_patterns": [
          "WARNING: Connection pool size growing",
          "ERROR: Failed to close database connection"
        ],
        "code_findings": "Risky loop in auth handler - connections not being released",
        "regression_detected": true,
        "problematic_commit": "abc123 - Add connection pooling"
      }
    },
    "remediation_plan": {
      "immediate_actions": [
        {
          "action": "rollback_deployment",
          "command": "kubectl rollout undo deployment/auth-service -n production",
          "risk": "low",
          "impact": "Brief service disruption (30s)",
          "rollback": "kubectl rollout undo deployment/auth-service -n production --to-revision=2"
        }
      ],
      "long_term_fixes": [
        "Fix connection leak in auth handler",
        "Add connection pool monitoring",
        "Implement connection timeout",
        "Add memory usage alerts"
      ],
      "estimated_resolution_time": "5 minutes"
    },
    "commander_approval": {
      "approved": true,
      "reasoning": "Rollback is low risk and will resolve memory leak. Team should fix code and redeploy.",
      "conditions": [
        "Monitor service after rollback",
        "Review code fix before redeploying",
        "Add tests for connection cleanup"
      ]
    },
    "execution": {
      "status": "completed",
      "sandbox_output": {
        "command": "kubectl rollout undo deployment/auth-service -n production",
        "result": "deployment.apps/auth-service rolled back",
        "exit_code": 0,
        "duration_ms": 1234
      },
      "verification": {
        "memory_usage": "512MB (decreased from 1.8GB)",
        "pod_restarts": 1,
        "service_healthy": true
      }
    }
  },
  "metrics": {
    "total_tokens": 1847,
    "token_breakdown": {
      "commander": 423,
      "investigator": 612,
      "code_analyst": 534,
      "remediator": 278
    },
    "cost_usd": 0.03694,
    "duration_seconds": 12.3
  },
  "audit": {
    "audit_log_id": 42,
    "all_messages_logged": true,
    "compliance_met": true
  },
  "outcome": {
    "incident_resolved": true,
    "human_intervention_required": false,
    "next_steps": [
      "Code fix and testing",
      "Redeploy with fix",
      "Post-incident review"
    ]
  }
}
```

---

## 🧪 Test Scenarios

### Scenario 1: Memory Leak

```bash
curl -X POST http://localhost:8000/incident \
  -H "Content-Type: application/json" \
  -d @scenarios/memory_leak.json
```

**Expected:** Agents detect leak, recommend rollback

### Scenario 2: High CPU

```bash
curl -X POST http://localhost:8000/incident \
  -H "Content-Type: application/json" \
  -d @scenarios/cpu_spike.json
```

**Expected:** Agents scale deployment, configure HPA

### Scenario 3: CrashLoopBackOff

```bash
curl -X POST http://localhost:8000/incident \
  -H "Content-Type: application/json" \
  -d @scenarios/crashloop.json
```

**Expected:** Code analysis finds startup error, fixes configuration

### Scenario 4: Cascading Failure

```bash
curl -X POST http://localhost:8000/incident \
  -H "Content-Type: application/json" \
  -d @scenarios/cascading_failure.json
```

**Expected:** Multi-agent coordination to isolate and resolve

---

## 💰 Cost Analysis

### Development: $10-20/month

**LLM costs (4 agents):**
```
Testing: 50 investigations/day
Average tokens per investigation: 1,800
Cost: 50 × 1,800 / 1000 × $0.002 = $0.18/day
Monthly: ~$5.40

Infrastructure: Docker Compose (free locally)
Total: ~$5-10/month
```

### Production: $150-250/month

**Infrastructure:**
```
API pods (3 replicas): $20
Postgres: $15
Sandbox pool: $30
Prometheus + Grafana: $10
Total infrastructure: $75/month
```

**LLM costs (1000 investigations/day):**
```
Daily: 1,000 × 1,800 tokens = 1,800,000 tokens
Cost: 1,800 × $0.002 = $3.60/day
Monthly: $108

Total: ~$185/month
```

### Cost Optimization

**Strategies:**
1. **Smart routing**: Use GPT-3.5 for simple triage (90% cheaper)
2. **Caching**: Store common investigation patterns
3. **Early termination**: Stop investigation if duplicate
4. **Parallel execution**: Reduce total time

**Optimized:**
```
Commander (GPT-3.5): $0.50/month
Specialists (GPT-4): $70/month
Result: $145/month (22% savings)
```

---

## 🆚 FREE vs PAID Comparison

| Feature | FREE Version | PAID Version |
|---------|-------------|--------------|
| **Agents** | 2 (Commander, SRE) | 4 (Commander, SRE, Code Analyst, Remediator) |
| **Docker Sandbox** | ❌ | ✅ Secure isolated execution |
| **RBAC** | ❌ | ✅ Role-based permissions |
| **Audit Logging** | Console only | ✅ PostgreSQL with full trail |
| **Multi-stage Workflow** | Simple | ✅ Complex orchestration |
| **Approval Workflow** | ❌ | ✅ Commander approval required |
| **Code Analysis** | ❌ | ✅ Dedicated agent |
| **Safe Execution** | Simulated | ✅ Resource-limited containers |
| **Test Scenarios** | Basic | ✅ 10+ production scenarios |
| **Observability** | Basic | ✅ Prometheus + Grafana |
| **Production Ready** | Learning | ✅ Yes |

---

## 🎓 Key Learning Outcomes

### Conceptual Understanding

After completing this lab, you understand:

✅ **Enterprise Multi-Agent Systems:**
- 4+ agent orchestration
- Complex workflow coordination
- Agent specialization and delegation
- Approval and consensus patterns

✅ **Production Security:**
- Docker sandboxing for AI
- RBAC for agent permissions
- Resource limits and constraints
- Audit compliance

✅ **Advanced AutoGen:**
- Multi-agent conversations
- Conditional routing
- State management
- Error recovery

✅ **Enterprise IR Automation:**
- Multi-specialist coordination
- Code-level analysis
- Safe remediation execution
- Complete audit trails

### Technical Skills

You can now:

✅ **Build 4+ agent systems** with AutoGen
✅ **Implement Docker sandboxes** for safe AI execution
✅ **Design RBAC systems** for agent security
✅ **Create audit logging** in PostgreSQL
✅ **Orchestrate complex workflows** with multiple specialists
✅ **Test at scale** with load testing
✅ **Monitor multi-agent systems** with Prometheus

---

## 🔧 Troubleshooting

### Postgres Connection Error

**Check logs:**
```bash
docker logs postgres
```

**Verify connection:**
```bash
docker exec -it postgres psql -U aiagent -d auditdb -c "SELECT 1;"
```

### Sandbox Cannot Start

**Test sandbox:**
```bash
docker run --rm -it sandbox:latest sh
```

**Check security constraints:**
```bash
docker inspect sandbox | grep -A 20 Security
```

---

## 🧹 Cleanup

```bash
docker compose down -v
bash scripts/cleanup.sh
```

---

## 🎉 Congratulations!

You've built an enterprise multi-agent system!

### What You've Mastered:

✅ **4-Agent System** - Complex orchestration  
✅ **Docker Sandboxing** - Secure AI execution  
✅ **RBAC Implementation** - Agent permissions  
✅ **Audit Compliance** - PostgreSQL logging  
✅ **Production Workflows** - Real-world automation  

You now have enterprise AI deployment skills!

Happy learning! 🚀🤖🛡️📊🔒