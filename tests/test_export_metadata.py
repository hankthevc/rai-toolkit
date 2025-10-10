"""Tests for export metadata in decision records."""

import os
from common.utils.exporters import build_decision_record
from common.utils.policy_loader import ScenarioContext
from common.utils.risk_engine import RiskAssessment, RiskInputs


def test_decision_record_contains_metadata():
    """Verify decision record contains Generated, App Commit, and Model metadata."""
    
    scenario = ScenarioContext(
        tier="High",
        contains_pii=True,
        customer_facing=True,
        high_stakes=True,
        autonomy_level=2,
        sector="Healthcare",
        modifiers=["Cyber"],
        model_type="Traditional ML",
        data_source="Proprietary/Internal",
        learns_in_production=False,
        international_data=False,
        explainability_level="Post-hoc Explainable",
        uses_foundation_model="No Third-Party",
        generates_synthetic_content=False,
        dual_use_risk="None / Low",
        decision_reversible="Partially Reversible",
        protected_populations=[],
    )
    
    assessment = RiskAssessment(
        score=8,
        tier="High",
        contributing_factors=["PII", "Customer Facing", "Healthcare"]
    )
    
    risk_inputs = RiskInputs(
        contains_pii=True,
        customer_facing=True,
        high_stakes=True,
        autonomy_level=2,
        sector="Healthcare",
        modifiers=["Cyber"],
        model_type="Traditional ML",
        data_source="Proprietary/Internal",
        learns_in_production=False,
        international_data=False,
        explainability_level="Post-hoc Explainable",
        uses_foundation_model="No Third-Party",
        generates_synthetic_content=False,
        dual_use_risk="None / Low",
        decision_reversible="Partially Reversible",
        protected_populations=[],
    )
    
    record = build_decision_record(
        scenario=scenario,
        assessment=assessment,
        controls=[],
        owner="Test Owner",
        approver="Test Approver",
        risk_inputs=risk_inputs,
        model_name="gpt-4o",
        model_temperature=0.3,
        unknowns=["Data location unknown"],
    )
    
    # Verify metadata is present
    assert "Generated:" in record, "Missing 'Generated:' timestamp in metadata"
    assert "App Commit:" in record, "Missing 'App Commit:' in metadata"
    assert "Model:" in record, "Missing 'Model:' in metadata"
    
    # Verify model details
    assert "gpt-4o" in record, "Model name not found in record"
    assert "temperature=0.3" in record, "Model temperature not found in record"


def test_decision_record_contains_unknowns_section():
    """Verify decision record contains Assumptions & Unknowns section."""
    
    scenario = ScenarioContext(
        tier="Medium",
        contains_pii=False,
        customer_facing=True,
        high_stakes=False,
        autonomy_level=1,
        sector="General",
        modifiers=[],
        model_type="Traditional ML",
        data_source="Proprietary/Internal",
        learns_in_production=False,
        international_data=False,
        explainability_level="Inherently Interpretable",
        uses_foundation_model="No Third-Party",
        generates_synthetic_content=False,
        dual_use_risk="None / Low",
        decision_reversible="Fully Reversible",
        protected_populations=[],
    )
    
    assessment = RiskAssessment(
        score=3,
        tier="Medium",
        contributing_factors=["Customer Facing"]
    )
    
    unknowns = [
        "Data storage location unknown - can't assess GDPR compliance",
        "Vendor contract terms unknown - supply chain risk unclear"
    ]
    
    record = build_decision_record(
        scenario=scenario,
        assessment=assessment,
        controls=[],
        owner="Test Owner",
        approver="Test Approver",
        unknowns=unknowns,
    )
    
    # Verify unknowns section exists
    assert "## Assumptions & Unknowns" in record, "Missing 'Assumptions & Unknowns' section"
    assert "Data storage location unknown" in record, "First unknown not found"
    assert "Vendor contract terms unknown" in record, "Second unknown not found"


def test_decision_record_commit_sha_from_env():
    """Verify app commit SHA is read from environment variable."""
    
    # Set environment variable
    test_commit = "abc123def456"
    os.environ["RAI_TOOLKIT_COMMIT_SHA"] = test_commit
    
    scenario = ScenarioContext(
        tier="Low",
        contains_pii=False,
        customer_facing=False,
        high_stakes=False,
        autonomy_level=0,
        sector="General",
        modifiers=[],
        model_type="Traditional ML",
        data_source="Proprietary/Internal",
        learns_in_production=False,
        international_data=False,
        explainability_level="Inherently Interpretable",
        uses_foundation_model="No Third-Party",
        generates_synthetic_content=False,
        dual_use_risk="None / Low",
        decision_reversible="Fully Reversible",
        protected_populations=[],
    )
    
    assessment = RiskAssessment(
        score=0,
        tier="Low",
        contributing_factors=[]
    )
    
    record = build_decision_record(
        scenario=scenario,
        assessment=assessment,
        controls=[],
        owner="Test",
        approver="Test",
    )
    
    # Verify commit SHA is in record
    assert test_commit in record, "Commit SHA from environment not found in record"
    
    # Clean up
    del os.environ["RAI_TOOLKIT_COMMIT_SHA"]

