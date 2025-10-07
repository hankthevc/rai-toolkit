"""Test the decision record export functionality."""

from datetime import date, timedelta

import pytest

from common.utils.exporters import build_decision_record
from common.utils.policy_loader import PolicyControl, ScenarioContext, WhenClause
from common.utils.risk_engine import RiskAssessment


@pytest.fixture
def sample_scenario():
    return ScenarioContext(
        tier="High",
        contains_pii=True,
        customer_facing=True,
        high_stakes=True,
        autonomy_level=2,
        sector="Healthcare",
        modifiers=["Cyber"],
    )


@pytest.fixture
def sample_assessment():
    return RiskAssessment(
        score=12,
        tier="High",
        contributing_factors=[
            "Contains PII (+2)",
            "Customer-facing exposure (+2)",
            "High-stakes impact (+3)",
            "Autonomy level 2 (+2)",
            "Modifier Cyber (+2)",
            "Sector sensitivity Healthcare (+1)",
        ],
    )


@pytest.fixture
def sample_controls():
    return [
        PolicyControl(
            id="TEST-01",
            title="Test Control",
            description="A test control for validation",
            authority="Test Framework",
            clause="Section 1.1",
            evidence="Test evidence required",
            tags=["testing", "validation"],
            mappings={"nist_ai_rmf": ["GOV-1.1"], "owasp_llm_top10": ["LLM01"]},
            when=WhenClause(tier=["High", "Critical"]),
        ),
        PolicyControl(
            id="TEST-02",
            title="PII Protection",
            description="Protect personally identifiable information",
            authority="Test Framework",
            clause="Section 2.3",
            evidence="PII handling documentation",
            tags=["privacy", "data_protection"],
            mappings=None,
            when=WhenClause(contains_pii=True),
        ),
    ]


def test_build_decision_record_basic(sample_scenario, sample_assessment, sample_controls):
    """Test basic decision record generation."""
    record = build_decision_record(
        scenario=sample_scenario,
        assessment=sample_assessment,
        controls=sample_controls,
        owner="Jane Doe",
        approver="John Smith",
    )

    assert "# Frontier AI Risk Decision Record" in record
    assert "Jane Doe" in record
    assert "John Smith" in record
    assert "High" in record
    assert "TEST-01" in record
    assert "TEST-02" in record


def test_build_decision_record_contains_all_fields(
    sample_scenario, sample_assessment, sample_controls
):
    """Verify all expected sections are present."""
    record = build_decision_record(
        scenario=sample_scenario,
        assessment=sample_assessment,
        controls=sample_controls,
        owner="Test Owner",
        approver="Test Approver",
    )

    # Check required sections
    assert "## Summary" in record
    assert "## Scenario Inputs" in record
    assert "## Required Safeguards" in record

    # Check scenario details
    assert "Contains PII: Yes" in record
    assert "Customer Facing: Yes" in record
    assert "High Stakes: Yes" in record
    assert "Autonomy Level: 2" in record
    assert "Sector: Healthcare" in record
    assert "Cyber" in record

    # Check assessment details
    assert "Risk Tier:** High" in record
    assert "Risk Score:** 12" in record


def test_build_decision_record_with_empty_controls(sample_scenario, sample_assessment):
    """Test export when no controls match."""
    record = build_decision_record(
        scenario=sample_scenario,
        assessment=sample_assessment,
        controls=[],
        owner="Test Owner",
        approver="Test Approver",
    )

    assert "No controls matched the scenario inputs" in record
    assert "Review policy packs for coverage gaps" in record


def test_build_decision_record_missing_owner_approver(
    sample_scenario, sample_assessment, sample_controls
):
    """Test that missing owner/approver defaults are applied."""
    record = build_decision_record(
        scenario=sample_scenario,
        assessment=sample_assessment,
        controls=sample_controls,
        owner="",
        approver="",
    )

    assert "Unassigned" in record
    assert "Pending" in record


def test_build_decision_record_dates(sample_scenario, sample_assessment, sample_controls):
    """Verify date fields are correctly formatted."""
    record = build_decision_record(
        scenario=sample_scenario,
        assessment=sample_assessment,
        controls=sample_controls,
        owner="Test Owner",
        approver="Test Approver",
        review_interval_days=90,
    )

    today = date.today().isoformat()
    next_review = (date.today() + timedelta(days=90)).isoformat()

    assert today in record
    assert next_review in record


def test_build_decision_record_control_mappings(
    sample_scenario, sample_assessment, sample_controls
):
    """Verify control mappings are rendered correctly."""
    record = build_decision_record(
        scenario=sample_scenario,
        assessment=sample_assessment,
        controls=sample_controls,
        owner="Test Owner",
        approver="Test Approver",
    )

    assert "nist_ai_rmf" in record
    assert "GOV-1.1" in record
    assert "owasp_llm_top10" in record
    assert "LLM01" in record


def test_build_decision_record_no_modifiers():
    """Test scenario with no modifiers."""
    scenario = ScenarioContext(
        tier="Low",
        contains_pii=False,
        customer_facing=False,
        high_stakes=False,
        autonomy_level=0,
        sector="General",
        modifiers=[],
    )
    assessment = RiskAssessment(score=0, tier="Low", contributing_factors=[])

    record = build_decision_record(
        scenario=scenario,
        assessment=assessment,
        controls=[],
        owner="Test Owner",
        approver="Test Approver",
    )

    assert "Contains PII: No" in record
    assert "Customer Facing: No" in record
    assert "High Stakes: No" in record
    assert "Modifiers: None" in record
    assert "None captured" in record


def test_build_decision_record_custom_review_interval(
    sample_scenario, sample_assessment, sample_controls
):
    """Test custom review interval."""
    record = build_decision_record(
        scenario=sample_scenario,
        assessment=sample_assessment,
        controls=sample_controls,
        owner="Test Owner",
        approver="Test Approver",
        review_interval_days=180,
    )

    next_review = (date.today() + timedelta(days=180)).isoformat()
    assert next_review in record

