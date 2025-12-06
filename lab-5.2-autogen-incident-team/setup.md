# 🚀 Lab 5.2 — Setup Guide  
Multi-Agent AutoGen Incident Response System  
(Full Production Edition with Sandbox, RBAC, Redis, PostgreSQL)

This guide walks you step-by-step so there is **zero confusion**.  
Follow in order — don’t skip.

---

## ✅ 1️⃣ Requirements

Before starting, ensure you have:

| Requirement | Version |
|------------|----------|
| Python | 3.10 or later |
| Docker | 20+ |
| Docker Compose | v2+ |
| Internet connection | Required (OpenAI model) |

---

## ✅ 2️⃣ Create the `.env` File

Inside the project folder, create a file named:

```
.env
```

Paste this inside (replace API key):

```
OPENAI_API_KEY=your-openai-key-here
POSTGRES_USER=aiagent
POSTGRES_PASSWORD=aiagentpass
POSTGRES_DB=auditdb
REDIS_HOST=redis
```

👉 **If students don’t have OpenAI keys, they can get free trial credits.**

---

## ✅ 3️⃣ Install Python Dependencies (Optional Local Mode)

> You do **NOT** need Python installed if you will run only via Docker.

If you want to run unit tests locally first:

```
pip install -r requirements.txt
```

Run tests:

```
pytest -q
```

---

## ✅ 4️⃣ Start the Full System

Run:

```
docker-compose up --build
```

💡 First build may take 2–3 minutes.

You should see services start:

```
✔ redis
✔ postgres
✔ sandbox
✔ api
```

---

## ✅ 5️⃣ Verify the System is Running

Open a new terminal and check:

```
curl http://localhost:8000/health
```

Expected output:

```json
{"status":"ok"}
```

---

## ✅ 6️⃣ View Available Incident Scenarios

```
curl http://localhost:8000/scenarios
```

Expected:

```json
{"available_scenarios":["memory_leak","cascading_failure"]}
```

---

## ✅ 7️⃣ Run Your First Automated Investigation

```
curl -X POST http://localhost:8000/incident/run \
  -H "Content-Type: application/json" \
  -d '{"scenario": "memory_leak", "auto_approve": false}'
```

You will get a **full JSON report**, including:

- Commander decision  
- Investigator analysis  
- Code analysis  
- Recommended fix  
- Cost tracking  
- Audit reference ID  

---

## 🧪 Optional: Auto-approve Sandbox Execution

If you want the fix validated inside the secure sandbox:

```
curl -X POST http://localhost:8000/incident/run \
  -H "Content-Type: application/json" \
  -d '{"scenario": "memory_leak", "auto_approve": true}'
```

You will see:

```
"sandbox_output": "Running sandbox validation... All checks passed."
```

---

## 📊 View Logs

```
docker-compose logs -f api
docker-compose logs -f postgres
```

---

## 🗂 Database Verification (Optional Advanced)

To check audit logs:

```
docker exec -it postgres psql -U aiagent -d auditdb
```

Then run:

```sql
SELECT * FROM audit_records LIMIT 10;
```

---

## 🧹 Cleanup

Stop everything:

```
docker-compose down -v
```

Run cleanup script:

```
bash scripts/cleanup.sh
```

---

## 🎉 You're Done

You now have a **fully functional multi-agent DevOps incident response AI system** running locally with:

- AutoGen agents
- FastAPI backend
- Redis conversation caching
- PostgreSQL audit logging
- Docker sandbox for safe code execution
- RBAC and workflow approvals

---
