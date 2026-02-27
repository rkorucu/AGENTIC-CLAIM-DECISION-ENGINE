# AgenticClaims

**AI-powered Insurance Claim Decision Agent** — A full-stack demo that processes claim requests through deterministic fraud/coverage checks, optional LLM explanation, and reflection-based self-checking.

---

## Project Overview

AgenticClaims is a mono-repo application that demonstrates an **agentic workflow** for insurance claim decisions. The system:

1. **Runs deterministic tools** — checks policy coverage, scores fraud signals, aggregates risk
2. **Optionally uses an LLM** — generates human-readable explanations (when `OPENAI_API_KEY` is set)
3. **Runs a reflection step** — self-checks for contradictions and consistency with score/decision logic

No database, auth, or real insurance integrations are required. The demo is JSON in/out.

---

## Key Features

- **Deterministic tools**: `coverage_check`, `fraud_signal_scoring`, `risk_score_aggregation`
- **Decision policy**: `APPROVE` / `REVIEW` / `REJECT` based on flags and risk level
- **Reflection**: Optional LLM step to verify consistency and improve output
- **Fallback mode**: Works without OpenAI; uses deterministic analysis only
- **Clean demo UI**: Single-page dashboard with form, decision card, flags table, and reflection panel

---

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Frontend  │────▶│  Spring Boot    │────▶│  Agent Service   │
│  (React)    │     │  (API Gateway)  │     │  (FastAPI)       │
│  :5173     │     │  :8080          │     │  :8000           │
└─────────────┘     └─────────────────┘     └──────────────────┘
                            │                         │
                            │                         │ (optional)
                            │                         ▼
                            │                 ┌──────────────────┐
                            │                 │  OpenAI API      │
                            │                 │  (explanation +  │
                            │                 │   reflection)    │
                            │                 └──────────────────┘
```

## ReAct/Agentic Flow

```
Claim Request
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Deterministic Tools (always)                          │
│   • coverage_check(claim, policy)                             │
│   • fraud_signal_scoring(claimRequest)                        │
│   • risk_score_aggregation                                    │
│   → draft decision (decision, riskScore, riskLevel, flags)   │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: LLM Explanation (optional, if OPENAI_API_KEY set)    │
│   • Input: decision + flags + claim summary                   │
│   • Output: human-readable explanation paragraph              │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Reflection (optional, if OPENAI_API_KEY set)          │
│   • Check: decision consistent with score/flags?               │
│   • Check: riskLevel matches score thresholds?                │
│   • Check: explanation clear & not contradictory?             │
│   • Adjust fields or add reflectionNotes if issues found      │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
ClaimDecision (JSON response)
```

---

## Quick Start

### Prerequisites

- **Java 17+** (for backend)
- **Python 3.11+** (for agent-service)
- **Node.js 18+** (for frontend)
- **Docker & Docker Compose** (optional, for full stack)

### Installation

```bash
git clone <repo-url>
cd AgenticClaims
```

### Environment Variables

Copy `.env.example` to `.env` and adjust as needed:

```bash
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Optional. Set for LLM explanation + reflection. Omit for deterministic-only mode. |
| `AGENT_SERVICE_URL` | Backend → agent-service URL. Default: `http://localhost:8000` |
| `VITE_API_BASE_URL` | Frontend → backend API URL. Default: `http://localhost:8080/api` |

### Run backend

```bash
cd backend
mvn spring-boot:run
```

Or use the script:

```bash
./scripts/run-backend.sh
```

Backend runs at **http://localhost:8080**

### Run agent-service

```bash
cd agent-service
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Or:

```bash
./scripts/run-agent-service.sh
```

Agent service runs at **http://localhost:8000**

### Run frontend

```bash
cd frontend
npm install
npm run dev
```

Or:

```bash
./scripts/run-frontend.sh
```

Frontend runs at **http://localhost:5173**

### Run with Docker Compose

```bash
docker-compose up --build
```

- Backend: **http://localhost:8080**
- Agent service: **http://localhost:8000**
- Frontend: **http://localhost:5173**

---

## API Endpoints

| Service | Method | Path | Description |
|---------|--------|------|-------------|
| Agent service | GET | `/health` | Health check |
| Agent service | POST | `/analyze` | Analyze claim (ClaimRequest → ClaimDecision) |
| Backend | GET | `/actuator/health` | Health check |
| Backend | POST | `/api/claims/analyze` | Analyze claim (forwards to agent-service) |

---

## Project Structure

```
AgenticClaims/
├── backend/                    # Spring Boot API Gateway
│   ├── src/main/java/com/agent/claims/
│   │   ├── ClaimsApplication.java
│   │   ├── config/
│   │   ├── controller/
│   │   ├── model/
│   │   └── service/
│   ├── src/main/resources/application.yml
│   └── pom.xml
├── agent-service/              # Python FastAPI (agentic workflow)
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── tools.py
│   │   ├── llm.py
│   │   ├── workflow.py
│   │   └── tests/test_tools.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # React UI (Vite)
│   ├── src/
│   │   ├── api/client.js
│   │   ├── components/
│   │   ├── pages/Dashboard.jsx
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── docs/
│   ├── architecture.md
│   ├── api-contract.md
│   └── sample-payloads/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Example Interactions

### Low-risk claim (expected APPROVE)

```json
{
  "claimId": "CLM-2024-001",
  "claimant": { "fullName": "Jane Doe", "state": "CA" },
  "policy": { "policyId": "POL-12345", "coverageType": "AUTO", "coverageLimit": 25000, "deductible": 500, "active": true },
  "incident": { "type": "COLLISION", "date": "2024-01-15", "description": "Vehicle was struck from behind..." },
  "claim": { "amount": 3500, "priorClaimsCount": 0, "hasPoliceReport": true, "attachmentsCount": 5 }
}
```

### High-risk claim (expected REVIEW or REJECT)

```json
{
  "claimId": "CLM-2024-003",
  "claimant": { "fullName": "Bob Wilson", "state": "FL" },
  "policy": { "policyId": "POL-11111", "coverageType": "AUTO", "coverageLimit": 10000, "deductible": 2000, "active": true },
  "incident": { "type": "THEFT", "date": "2024-02-10", "description": "Stolen items." },
  "claim": { "amount": 12000, "priorClaimsCount": 4, "hasPoliceReport": false, "attachmentsCount": 0 }
}
```

### cURL example

```bash
curl -X POST http://localhost:8080/api/claims/analyze \
  -H "Content-Type: application/json" \
  -d @docs/sample-payloads/claim_low_risk.json
```

---

## Testing

### Python (agent-service)

```bash
cd agent-service
pip install -r requirements.txt
pytest app/tests/ -v
```

### Java (backend)

```bash
cd backend
mvn test
```

---

## License

MIT License. See LICENSE file for details.

---

## Acknowledgments

- Inspired by AgenticCalendar-style mono-repo architecture
- Built with Spring Boot, FastAPI, React, and Vite
