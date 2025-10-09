"""Additional test coverage for edge cases and integrity checks."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from common.utils.exporters import build_decision_record
from common.utils.policy_loader import ScenarioContext, load_policy_packs
from common.utils.risk_engine import RiskInputs, calculate_risk_score


def test_scoring_edge_case_maximum_risk():
    """Test that maximum risk configuration produces Critical tier."""
    # Absolute maximum risk: everything enabled
    inputs = RiskInputs(
        contains_pii=True,
        customer_facing=True,
        high_stakes=True,
        autonomy_level=3,  # Full autonomy
        sector="Healthcare",  # High-risk sector
        modifiers=["Bio", "Cyber", "Disinformation", "Children"],  # All modifiers
        model_type="Generative AI / LLM",
        data_source="Internet-Scraped",
        learns_in_production=True,
        international_data=True,
        explainability_level="Black Box",
        uses_foundation_model="External API",
        generates_synthetic_content=True,
        dual_use_risk="High",
        decision_reversible="Irreversible",
        protected_populations=["Children", "Elderly", "People with Disabilities"],
    )
    
    assessment = calculate_risk_score(inputs)
    
    # With all risk factors maxed out, should be Critical
    assert assessment.tier == "Critical", f"Expected Critical tier but got {assessment.tier} (score: {assessment.score})"
    assert assessment.score > 40, "Maximum risk should have a very high score (score: {assessment.score})"
    assert len(assessment.contributing_factors) >= 10, "Should have many contributing factors"


def test_scoring_edge_case_minimum_risk():
    """Test that minimum risk configuration produces Low tier."""
    # Absolute minimum risk: all defaults, no risk factors
    inputs = RiskInputs(
        contains_pii=False,
        customer_facing=False,
        high_stakes=False,
        autonomy_level=0,  # Suggestion only
        sector="General",
        modifiers=[],
        model_type="Traditional ML",
        data_source="Proprietary/Internal",
        learns_in_production=False,
        international_data=False,
        explainability_level="Inherently Interpretable",
        uses_foundation_model="No Third-Party",
        generates_synthetic_content=False,
        dual_use_risk="None",
        decision_reversible="Fully Reversible",
        protected_populations=[],
    )
    
    assessment = calculate_risk_score(inputs)
    
    # With no risk factors, should be Low
    assert assessment.tier == "Low", f"Expected Low tier but got {assessment.tier} (score: {assessment.score})"
    assert assessment.score == 0, "Minimum risk should have score of 0"
    assert len(assessment.contributing_factors) == 0, "Should have no contributing factors"


def test_yaml_integrity_all_policy_packs():
    """Test that all YAML policy packs are valid and can be loaded without errors."""
    policy_packs_dir = Path("common/policy_packs")
    
    # Should have at least 6 policy packs
    yaml_files = list(policy_packs_dir.glob("*.yaml"))
    assert len(yaml_files) >= 6, f"Expected at least 6 policy packs, found {len(yaml_files)}"
    
    # Load all policy packs (will raise exception if any are invalid)
    packs = load_policy_packs(policy_packs_dir)
    
    # Verify each pack has required structure
    for pack in packs:
        assert pack.name, "Policy pack must have a name"
        assert pack.version, "Policy pack must have a version"
        assert pack.description, "Policy pack must have a description"
        assert pack.controls, "Policy pack must have at least one control"
        
        # Verify each control has required fields
        for control in pack.controls:
            assert control.id, f"Control must have an ID in pack {pack.name}"
            assert control.title, f"Control {control.id} must have a title"
            assert control.description, f"Control {control.id} must have a description"
            assert control.authority, f"Control {control.id} must have an authority"
            assert control.clause, f"Control {control.id} must have a clause"
            assert control.evidence, f"Control {control.id} must have evidence"
            assert control.when is not None, f"Control {control.id} must have a when clause"
            
            # Tags should be a list (can be empty)
            assert isinstance(control.tags, list), f"Control {control.id} tags must be a list"


def test_yaml_no_duplicate_control_ids():
    """Test that no control IDs are duplicated across all policy packs."""
    policy_packs_dir = Path("common/policy_packs")
    packs = load_policy_packs(policy_packs_dir)
    
    # Collect all control IDs
    all_control_ids = []
    for pack in packs:
        for control in pack.controls:
            all_control_ids.append((control.id, pack.name))
    
    # Check for duplicates
    seen_ids = set()
    duplicates = []
    
    for control_id, pack_name in all_control_ids:
        if control_id in seen_ids:
            duplicates.append(f"{control_id} (in {pack_name})")
        seen_ids.add(control_id)
    
    assert len(duplicates) == 0, f"Found duplicate control IDs: {', '.join(duplicates)}"


def test_export_decision_record_contains_required_sections():
    """Test that exported decision record contains all required sections."""
    # Create a test scenario
    inputs = RiskInputs(
        contains_pii=True,
        customer_facing=True,
        high_stakes=True,
        autonomy_level=2,
        sector="Healthcare",
        modifiers=["Bio"],
    )
    
    assessment = calculate_risk_score(inputs)
    
    scenario = ScenarioContext(
        tier=assessment.tier,
        contains_pii=inputs.contains_pii,
        customer_facing=inputs.customer_facing,
        high_stakes=inputs.high_stakes,
        autonomy_level=inputs.autonomy_level,
        sector=inputs.sector,
        modifiers=inputs.modifiers,
    )
    
    # Load policy packs and get controls
    packs = load_policy_packs(Path("common/policy_packs"))
    from common.utils.policy_loader import select_applicable_controls
    controls = select_applicable_controls(packs, scenario)
    
    # Build decision record
    record = build_decision_record(
        scenario=scenario,
        assessment=assessment,
        controls=controls,
        owner="Test Owner",
        approver="Test Approver",
    )
    
    # Verify required sections are present
    required_sections = [
        "# Frontier AI Risk Decision Record",
        "## Summary",
        "**Risk Tier:**",
        "**Risk Score:**",
        "## Scenario Inputs",
        "## Required Safeguards",
    ]
    
    for section in required_sections:
        assert section in record, f"Decision record missing required section: {section}"
    
    # Verify specific values are included
    assert "Healthcare" in record, "Sector should be in decision record"
    assert assessment.tier in record, "Risk tier should be in decision record"
    assert "Test Owner" in record, "Owner should be in decision record"
    assert "Test Approver" in record, "Approver should be in decision record"
    
    # Verify it's markdown format
    assert record.strip().startswith("#"), "Decision record should be markdown format"
    
    # Verify controls are listed (if any were triggered)
    if controls:
        assert "###" in record, "Should have control subsections"


def test_export_decision_record_handles_empty_controls():
    """Test that decision record handles scenarios with no triggered controls gracefully."""
    # Minimal risk scenario that triggers no controls
    inputs = RiskInputs(
        contains_pii=False,
        customer_facing=False,
        high_stakes=False,
        autonomy_level=0,
        sector="General",
        modifiers=[],
    )
    
    assessment = calculate_risk_score(inputs)
    
    scenario = ScenarioContext(
        tier=assessment.tier,
        contains_pii=inputs.contains_pii,
        customer_facing=inputs.customer_facing,
        high_stakes=inputs.high_stakes,
        autonomy_level=inputs.autonomy_level,
        sector=inputs.sector,
        modifiers=inputs.modifiers,
    )
    
    # Build decision record with empty controls list
    record = build_decision_record(
        scenario=scenario,
        assessment=assessment,
        controls=[],  # No controls
        owner="",
        approver="",
    )
    
    # Should still produce valid markdown
    assert "# Frontier AI Risk Decision Record" in record
    assert "No controls matched" in record or "0 control" in record.lower()
    assert len(record) > 100, "Decision record should still have substantial content"

