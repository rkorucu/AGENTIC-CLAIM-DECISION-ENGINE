"""Deterministic tools for claim analysis: coverage check, fraud scoring, risk aggregation."""

from .models import ClaimRequest, Flag


def coverage_check(claim: dict, policy: dict) -> tuple[list[Flag], dict]:
    """
    Check coverage rules.
    Returns (flags, summary_dict).
    If policy.active is false -> POLICY_INACTIVE (HIGH), force REJECT.
    If claim.amount > coverageLimit -> EXCEEDS_LIMIT (HIGH).
    If net = amount - deductible <= 0 -> REVIEW (flag for low net).
    """
    flags: list[Flag] = []
    summary: dict = {"passed": True, "netAmount": None, "exceedsLimit": False}

    amount = claim.get("amount", 0)
    coverage_limit = policy.get("coverageLimit", 0)
    deductible = policy.get("deductible", 0)
    active = policy.get("active", True)

    if not active:
        flags.append(
            Flag(
                code="POLICY_INACTIVE",
                severity="HIGH",
                message="Policy is inactive. Claim cannot be processed.",
            )
        )
        summary["passed"] = False
        summary["policyActive"] = False
        return flags, summary

    summary["policyActive"] = True

    if amount > coverage_limit:
        flags.append(
            Flag(
                code="EXCEEDS_LIMIT",
                severity="HIGH",
                message=f"Claim amount ${amount:,.0f} exceeds coverage limit ${coverage_limit:,.0f}.",
            )
        )
        summary["passed"] = False
        summary["exceedsLimit"] = True

    net = amount - deductible
    summary["netAmount"] = net
    summary["amount"] = amount
    summary["deductible"] = deductible
    summary["coverageLimit"] = coverage_limit

    if net <= 0 and amount > 0:
        flags.append(
            Flag(
                code="NET_BELOW_DEDUCTIBLE",
                severity="MEDIUM",
                message=f"Net amount after deductible (${net:,.0f}) is zero or negative. Recommend REVIEW.",
            )
        )

    return flags, summary


def fraud_signal_scoring(claim_request: ClaimRequest) -> tuple[int, list[Flag], dict]:
    """
    Score fraud signals.
    Returns (fraud_score_contribution, flags, summary_dict).
    - priorClaimsCount >= 3 -> +25, MANY_PRIOR_CLAIMS (MEDIUM)
    - attachmentsCount == 0 and amount >= 5000 -> +20, NO_ATTACHMENTS_HIGH_AMOUNT (HIGH)
    - hasPoliceReport == false and incident.type in [THEFT, VANDALISM] -> +15, NO_POLICE_REPORT (MEDIUM)
    - incident.description length < 30 and amount >= 3000 -> +10, VAGUE_DESCRIPTION (LOW)
    """
    score = 0
    flags: list[Flag] = []
    summary: dict = {"contributions": []}

    claim = claim_request.claim
    incident = claim_request.incident
    amount = claim.amount
    prior = claim.priorClaimsCount
    attachments = claim.attachmentsCount
    has_report = claim.hasPoliceReport
    inc_type = incident.type.upper()
    desc_len = len(incident.description or "")

    if prior >= 3:
        score += 25
        flags.append(
            Flag(
                code="MANY_PRIOR_CLAIMS",
                severity="MEDIUM",
                message=f"Claimant has {prior} prior claims. Elevated fraud risk.",
            )
        )
        summary["contributions"].append({"rule": "priorClaimsCount>=3", "points": 25})

    if attachments == 0 and amount >= 5000:
        score += 20
        flags.append(
            Flag(
                code="NO_ATTACHMENTS_HIGH_AMOUNT",
                severity="HIGH",
                message=f"Claim amount ${amount:,.0f} with no attachments. High fraud risk.",
            )
        )
        summary["contributions"].append(
            {"rule": "noAttachmentsAndAmount>=5000", "points": 20}
        )

    if not has_report and inc_type in ("THEFT", "VANDALISM"):
        score += 15
        flags.append(
            Flag(
                code="NO_POLICE_REPORT",
                severity="MEDIUM",
                message=f"Incident type {inc_type} requires police report. None provided.",
            )
        )
        summary["contributions"].append(
            {"rule": "noPoliceReportForTheftOrVandalism", "points": 15}
        )

    if desc_len < 30 and amount >= 3000:
        score += 10
        flags.append(
            Flag(
                code="VAGUE_DESCRIPTION",
                severity="LOW",
                message=f"Incident description is brief ({desc_len} chars) for claim amount ${amount:,.0f}.",
            )
        )
        summary["contributions"].append(
            {"rule": "vagueDescriptionAndAmount>=3000", "points": 10}
        )

    summary["totalFraudContribution"] = score
    summary["flagsCount"] = len(flags)
    return score, flags, summary


def risk_score_aggregation(
    base_score: int,
    fraud_contribution: int,
    coverage_flags: list[Flag],
) -> tuple[int, str]:
    """
    Aggregate risk score and determine risk level.
    baseScore = 10, add fraud, add coverage penalties (e.g., exceed limit +40).
    Cap 0..100.
    riskLevel: <30 LOW, 30..69 MEDIUM, >=70 HIGH
    """
    score = base_score + fraud_contribution

    for f in coverage_flags:
        if f.code == "EXCEEDS_LIMIT":
            score += 40
        elif f.code == "POLICY_INACTIVE":
            score += 50  # severe
        elif f.code == "NET_BELOW_DEDUCTIBLE":
            score += 5

    score = max(0, min(100, score))

    if score < 30:
        level = "LOW"
    elif score < 70:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return score, level


def compute_decision(
    risk_level: str,
    coverage_flags: list[Flag],
) -> str:
    """
    Decision policy:
    - If any HIGH severity coverage flag (POLICY_INACTIVE or EXCEEDS_LIMIT) -> REJECT
    - Else if riskLevel HIGH -> REVIEW
    - Else if riskLevel MEDIUM -> REVIEW
    - Else -> APPROVE
    """
    high_coverage_codes = {"POLICY_INACTIVE", "EXCEEDS_LIMIT"}
    for f in coverage_flags:
        if f.severity == "HIGH" and f.code in high_coverage_codes:
            return "REJECT"

    if risk_level == "HIGH":
        return "REVIEW"
    if risk_level == "MEDIUM":
        return "REVIEW"
    return "APPROVE"
