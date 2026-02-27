"""Pydantic models for ClaimRequest and ClaimDecision."""

from pydantic import BaseModel, Field


class Claimant(BaseModel):
    fullName: str
    state: str


class Policy(BaseModel):
    policyId: str
    coverageType: str
    coverageLimit: float
    deductible: float
    active: bool


class Incident(BaseModel):
    type: str
    date: str
    description: str


class Claim(BaseModel):
    amount: float
    priorClaimsCount: int
    hasPoliceReport: bool
    attachmentsCount: int


class ClaimRequest(BaseModel):
    claimId: str
    claimant: Claimant
    policy: Policy
    incident: Incident
    claim: Claim


class Flag(BaseModel):
    code: str
    severity: str  # LOW | MEDIUM | HIGH
    message: str


class ToolSummary(BaseModel):
    coverageCheck: dict | None = None
    fraudSignals: dict | None = None


class ClaimDecision(BaseModel):
    decision: str  # APPROVE | REVIEW | REJECT
    riskScore: int = Field(ge=0, le=100)
    riskLevel: str  # LOW | MEDIUM | HIGH
    flags: list[Flag] = Field(default_factory=list)
    explanation: str = ""
    reflectionNotes: list[str] = Field(default_factory=list)
    toolSummary: ToolSummary | None = None
