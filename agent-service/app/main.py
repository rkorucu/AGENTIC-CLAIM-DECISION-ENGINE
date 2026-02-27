"""FastAPI app: /health and /analyze endpoints."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import ClaimRequest, ClaimDecision
from .workflow import analyze_claim

app = FastAPI(
    title="AgenticClaims Agent Service",
    description="AI-powered Insurance Claim Decision Agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "agent-service"}


@app.post("/analyze", response_model=ClaimDecision)
def analyze(req: ClaimRequest) -> ClaimDecision:
    """Analyze a claim and return decision with flags, explanation, and reflection notes."""
    try:
        return analyze_claim(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
