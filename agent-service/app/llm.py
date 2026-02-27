"""OpenAI wrapper for explanation and reflection. Fallback when API key is missing."""

import os
from openai import OpenAI


def get_client() -> OpenAI | None:
    """Return OpenAI client if API key is set, else None."""
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        return None
    return OpenAI(api_key=key)


def generate_explanation(
    decision: str,
    risk_score: int,
    risk_level: str,
    flags: list[dict],
    claim_summary: str,
) -> str:
    """Generate a short human-readable explanation of the claim decision."""
    client = get_client()
    if not client:
        return "LLM disabled. Deterministic analysis only."

    flags_text = "\n".join(f"- [{f['severity']}] {f['code']}: {f['message']}" for f in flags)
    prompt = f"""You are an insurance claim analyst. Write a brief, professional paragraph (2-4 sentences) explaining this claim decision to a claims adjuster.

Claim summary: {claim_summary}

Decision: {decision}
Risk score: {risk_score}
Risk level: {risk_level}

Flags raised:
{flags_text}

Write a clear, non-contradictory explanation. Do not invent facts. Be concise."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "LLM error. Deterministic analysis only."


def reflect_on_decision(
    decision: str,
    risk_score: int,
    risk_level: str,
    flags: list[dict],
    explanation: str,
) -> list[str]:
    """
    Reflection step: check for consistency and issues.
    Returns list of reflection notes (or empty if all good).
    """
    client = get_client()
    if not client:
        return ["LLM disabled. Reflection skipped."]

    flags_text = "\n".join(f"- {f['code']} ({f['severity']}): {f['message']}" for f in flags)
    prompt = f"""You are a quality assurance reviewer for insurance claim decisions. Check this decision for consistency and clarity.

Decision: {decision}
Risk score: {risk_score}
Risk level: {risk_level}

Flags:
{flags_text}

Explanation: {explanation}

Rules:
- riskLevel LOW: score < 30
- riskLevel MEDIUM: 30 <= score < 70
- riskLevel HIGH: score >= 70
- REJECT should only occur when POLICY_INACTIVE or EXCEEDS_LIMIT
- Explanation should not contradict the decision or flags

List any issues found (one per line). If everything is consistent and clear, respond with exactly: OK"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        text = response.choices[0].message.content.strip()
        if text.upper() == "OK":
            return []
        lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
        return lines[:5]  # cap at 5 notes
    except Exception:
        return ["Reflection error. Proceeding with current decision."]
