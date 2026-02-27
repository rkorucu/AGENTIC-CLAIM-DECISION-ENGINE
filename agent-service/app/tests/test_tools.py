"""Unit tests for deterministic tools."""

import pytest
from app.models import ClaimRequest, Claimant, Policy, Incident, Claim
from app.tools import (
    coverage_check,
    fraud_signal_scoring,
    risk_score_aggregation,
    compute_decision,
)


def _make_request(
    amount=5000,
    prior_claims=0,
    has_police=True,
    attachments=3,
    policy_active=True,
    coverage_limit=10000,
    deductible=500,
    incident_type="COLLISION",
    description="A detailed incident description that is long enough to pass the vague check.",
):
    return ClaimRequest(
        claimId="CLM-TEST",
        claimant=Claimant(fullName="Test User", state="CA"),
        policy=Policy(
            policyId="POL-1",
            coverageType="AUTO",
            coverageLimit=coverage_limit,
            deductible=deductible,
            active=policy_active,
        ),
        incident=Incident(
            type=incident_type,
            date="2024-01-01",
            description=description,
        ),
        claim=Claim(
            amount=amount,
            priorClaimsCount=prior_claims,
            hasPoliceReport=has_police,
            attachmentsCount=attachments,
        ),
    )


class TestCoverageCheck:
    def test_active_policy_under_limit(self):
        flags, summary = coverage_check(
            {"amount": 5000},
            {"coverageLimit": 10000, "deductible": 500, "active": True},
        )
        assert summary["passed"] is True
        assert summary["netAmount"] == 4500
        assert not any(f.code == "POLICY_INACTIVE" for f in flags)
        assert not any(f.code == "EXCEEDS_LIMIT" for f in flags)

    def test_inactive_policy(self):
        flags, summary = coverage_check(
            {"amount": 1000},
            {"coverageLimit": 10000, "deductible": 0, "active": False},
        )
        assert any(f.code == "POLICY_INACTIVE" for f in flags)
        assert flags[0].severity == "HIGH"
        assert summary["passed"] is False

    def test_exceeds_limit(self):
        flags, summary = coverage_check(
            {"amount": 15000},
            {"coverageLimit": 10000, "deductible": 500, "active": True},
        )
        assert any(f.code == "EXCEEDS_LIMIT" for f in flags)
        assert flags[0].severity == "HIGH"
        assert summary["exceedsLimit"] is True

    def test_net_below_deductible(self):
        flags, summary = coverage_check(
            {"amount": 300},
            {"coverageLimit": 10000, "deductible": 500, "active": True},
        )
        assert any(f.code == "NET_BELOW_DEDUCTIBLE" for f in flags)
        assert summary["netAmount"] == -200


class TestFraudSignalScoring:
    def test_many_prior_claims(self):
        req = _make_request(prior_claims=4)
        score, flags, summary = fraud_signal_scoring(req)
        assert score >= 25
        assert any(f.code == "MANY_PRIOR_CLAIMS" for f in flags)

    def test_no_attachments_high_amount(self):
        req = _make_request(amount=6000, attachments=0)
        score, flags, summary = fraud_signal_scoring(req)
        assert score >= 20
        assert any(f.code == "NO_ATTACHMENTS_HIGH_AMOUNT" for f in flags)

    def test_no_police_report_theft(self):
        req = _make_request(
            incident_type="THEFT",
            has_police=False,
        )
        score, flags, summary = fraud_signal_scoring(req)
        assert score >= 15
        assert any(f.code == "NO_POLICE_REPORT" for f in flags)

    def test_vague_description(self):
        req = _make_request(
            amount=4000,
            description="Short.",
        )
        score, flags, summary = fraud_signal_scoring(req)
        assert score >= 10
        assert any(f.code == "VAGUE_DESCRIPTION" for f in flags)

    def test_clean_claim_no_flags(self):
        req = _make_request()
        score, flags, summary = fraud_signal_scoring(req)
        assert score == 0
        assert len(flags) == 0


class TestRiskScoreAggregation:
    def test_low_risk(self):
        score, level = risk_score_aggregation(10, 5, [])
        assert score == 15
        assert level == "LOW"

    def test_medium_risk(self):
        score, level = risk_score_aggregation(10, 25, [])
        assert score == 35
        assert level == "MEDIUM"

    def test_high_risk(self):
        score, level = risk_score_aggregation(10, 65, [])
        assert score == 75
        assert level == "HIGH"

    def test_exceeds_limit_penalty(self):
        from app.models import Flag
        flags = [Flag(code="EXCEEDS_LIMIT", severity="HIGH", message="x")]
        score, level = risk_score_aggregation(10, 0, flags)
        assert score == 50
        assert level == "MEDIUM"

    def test_score_capped_at_100(self):
        score, level = risk_score_aggregation(10, 200, [])
        assert score == 100


class TestComputeDecision:
    def test_reject_policy_inactive(self):
        from app.models import Flag
        flags = [Flag(code="POLICY_INACTIVE", severity="HIGH", message="x")]
        assert compute_decision("LOW", flags) == "REJECT"

    def test_reject_exceeds_limit(self):
        from app.models import Flag
        flags = [Flag(code="EXCEEDS_LIMIT", severity="HIGH", message="x")]
        assert compute_decision("LOW", flags) == "REJECT"

    def test_review_high_risk(self):
        assert compute_decision("HIGH", []) == "REVIEW"

    def test_review_medium_risk(self):
        assert compute_decision("MEDIUM", []) == "REVIEW"

    def test_approve_low_risk(self):
        assert compute_decision("LOW", []) == "APPROVE"
