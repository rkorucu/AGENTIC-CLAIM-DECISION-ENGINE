# AgenticClaims Architecture

## Overview

AgenticClaims is an AI-powered Insurance Claim Decision Agent that processes claim requests through a deterministic tool pipeline, optional LLM explanation, and reflection-based self-checking.

## System Components

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
│ Step 1: Deterministic Tools (always)                        │
│   • coverage_check(claim, policy)                           │
│   • fraud_signal_scoring(claimRequest)                      │
│   • risk_score_aggregation                                   │
│   → draft decision (decision, riskScore, riskLevel, flags)   │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: LLM Explanation (optional, if OPENAI_API_KEY set)    │
│   • Input: decision + flags + claim summary                  │
│   • Output: human-readable explanation paragraph             │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Reflection (optional, if OPENAI_API_KEY set)        │
│   • Check: decision consistent with score/flags?             │
│   • Check: riskLevel matches score thresholds?              │
│   • Check: explanation clear & not contradictory?           │
│   • Adjust fields or add reflectionNotes if issues found    │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
ClaimDecision (JSON response)
```

## Data Flow

1. **Frontend** → User submits claim via form or loads sample payload
2. **Backend** → Receives POST `/api/claims/analyze`, forwards to agent-service
3. **Agent Service** → Runs workflow, returns ClaimDecision
4. **Frontend** → Displays decision, flags, explanation, reflection notes

## Fallback Mode

When `OPENAI_API_KEY` is not set:
- Steps 2 and 3 are skipped
- `explanation` = "LLM disabled. Deterministic analysis only."
- `reflectionNotes` includes note about fallback mode
