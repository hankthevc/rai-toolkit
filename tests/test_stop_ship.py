"""Tests for stop-ship trigger detection."""

import pytest

from common.utils.risk_engine import (
    RiskInputs,
    calculate_risk_score,
    check_stop_ship_triggers,
)


def test_critical_pii_irreversible_triggers_stop_ship():
    """Critical tier + PII + Irreversible should trigger stop-ship rule."""
    inputs = RiskInputs(
        contains_pii=True,
        customer_facing=True,
        high_stakes=True,
        autonomy_level=3,
        sector="Healthcare",
        modifiers=[],
        model_type="Traditional ML",
        data_source="Proprietary/Internal",
        learns_in_production=False,
        international_data=False,
        explainability_level="Inherently Interpretable",
        uses_foundation_model="No Third-Party",
        generates_synthetic_content=False,
        dual_use_risk="None / Low",
        decision_reversible="Irreversible",
        protected_populations=[],
    )
    
    assessment = calculate_risk_score(inputs)
    assert assessment.tier == "Critical"
    
    triggers = check_stop_ship_triggers(inputs, assessment)
    assert len(triggers) > 0
    assert any("Critical + PII + Irreversible" in trigger for trigger in triggers)


def test_synthetic_content_triggers_stop_ship_all_tiers():
    """Synthetic content generation should trigger stop-ship at any tier."""
    inputs = RiskInputs(
        contains_pii=False,
        customer_facing=False,
        high_stakes=False,
        autonomy_level=0,
        sector="General",
        modifiers=[],
        model_type="Generative AI / LLM",
        data_source="Proprietary/Internal",
        learns_in_production=False,
        international_data=False,
        explainability_level="Inherently Interpretable",
        uses_foundation_model="No Third-Party",
        generates_synthetic_content=True,
        dual_use_risk="None / Low",
        decision_reversible="Fully Reversible",
        protected_populations=[],
    )
    
    assessment = calculate_risk_score(inputs)
    # Should be low tier but still trigger stop-ship
    
    triggers = check_stop_ship_triggers(inputs, assessment)
    assert len(triggers) > 0
    assert any("Synthetic Content Generation" in trigger for trigger in triggers)


def test_protected_populations_critical_triggers_stop_ship():
    """Critical tier with children/elderly should trigger stop-ship."""
    inputs = RiskInputs(
        contains_pii=True,
        customer_facing=True,
        high_stakes=True,
        autonomy_level=3,
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
        protected_populations=["Children", "Elderly"],
    )
    
    assessment = calculate_risk_score(inputs)
    assert assessment.tier == "Critical"
    
    triggers = check_stop_ship_triggers(inputs, assessment)
    assert len(triggers) > 0
    assert any("Critical + Protected Populations" in trigger for trigger in triggers)


def test_no_stop_ship_for_low_risk():
    """Low-risk scenarios should not trigger stop-ships (except synthetic content)."""
    inputs = RiskInputs(
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
    
    assessment = calculate_risk_score(inputs)
    assert assessment.tier == "Low"
    
    triggers = check_stop_ship_triggers(inputs, assessment)
    assert len(triggers) == 0


def test_high_healthcare_triggers_stop_ship():
    """High tier + Healthcare sector should trigger stop-ship."""
    inputs = RiskInputs(
        contains_pii=True,
        customer_facing=True,
        high_stakes=False,  # Changed to False to get High tier instead of Critical
        autonomy_level=1,  # Reduced to 1
        sector="Healthcare",
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
    
    assessment = calculate_risk_score(inputs)
    # PII(2) + customer_facing(2) + healthcare_sector(1) + autonomy(1) = 6 = High tier
    assert assessment.tier == "High"
    
    triggers = check_stop_ship_triggers(inputs, assessment)
    assert len(triggers) > 0
    assert any("High + Healthcare" in trigger for trigger in triggers)

