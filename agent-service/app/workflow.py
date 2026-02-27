"""Agentic workflow: draft -> explain -> reflect."""

import os
from .models import ClaimRequest, ClaimDecision, Flag, ToolSummary
from .tools import (
    coverage_check,
    fraud_signal_scoring,
    risk_score_aggregation,
    compute_decision,
)
from .llm import generate_explanation, reflect_on_decision


def _claim_summary(req: ClaimRequest) -> str:
    return (
        f"Claim {req.claimId}: {req.incident.type} on {req.incident.date}, "
        f"amount ${req.claim.amount:,.0f}, policy {req.policy.policyId} "
        f"({req.policy.coverageType}, limit ${req.policy.coverageLimit:,.0f})."
    )


def analyze_claim(request: ClaimRequest) -> ClaimDecision:
    """
    Full workflow:
    1. Run deterministic tools -> draft decision
    2. (optional) LLM explanation
    3. (optional) Reflection step
    """
    claim_dict = request.claim.model_dump()
    policy_dict = request.policy.model_dump()

    # Step 1: Deterministic tools
    coverage_flags, coverage_summary = coverage_check(claim_dict, policy_dict)
    fraud_contrib, fraud_flags, fraud_summary = fraud_signal_scoring(request)
    all_flags = coverage_flags + fraud_flags
    risk_score, risk_level = risk_score_aggregation(10, fraud_contrib, coverage_flags)
    decision = compute_decision(risk_level, coverage_flags)

    # Initial explanation (fallback text)
    explanation = ""

    # Step 2: LLM explanation (optional)
    use_llm = bool(os.environ.get("OPENAI_API_KEY", "").strip())
    if use_llm:
        flags_for_llm = [f.model_dump() for f in all_flags]
        claim_summary = _claim_summary(request)
        explanation = generate_explanation(
            decision, risk_score, risk_level, flags_for_llm, claim_summary
        )
    else:
        explanation = "LLM disabled. Deterministic analysis only."

    # Step 3: Reflection (optional)
    reflection_notes: list[str] = []
    if use_llm:
        flags_for_llm = [f.model_dump() for f in all_flags]
        reflection_notes = reflect_on_decision(
            decision, risk_score, risk_level, flags_for_llm, explanation
        )
    else:
        reflection_notes = ["LLM disabled. Reflection skipped."]

    # Build tool summary for UI
    tool_summary = ToolSummary(
        coverageCheck=coverage_summary,
        fraudSignals=fraud_summary,
    )

    return ClaimDecision(
        decision=decision,
        riskScore=risk_score,
        riskLevel=risk_level,
        flags=all_flags,
        explanation=explanation,
        reflectionNotes=reflection_notes,
        toolSummary=tool_summary,
    )
