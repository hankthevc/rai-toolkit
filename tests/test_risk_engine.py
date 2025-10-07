"""Exercise the risk engine scoring heuristic."""

from pathlib import Path

import pytest

from common.utils.policy_loader import ScenarioContext, load_policy_packs, select_applicable_controls
from common.utils.risk_engine import (
    RiskInputs,
    calculate_risk_score,
    determine_risk_tier,
)


def test_high_risk_scenario_triggers_controls():
    inputs = RiskInputs(
        contains_pii=True,
        customer_facing=True,
        high_stakes=True,
        autonomy_level=2,
        sector="Healthcare",
        modifiers=["Cyber"],
    )
    assessment = calculate_risk_score(inputs)
    assert assessment.tier in {"High", "Critical"}

    scenario = ScenarioContext(
        tier=assessment.tier,
        contains_pii=inputs.contains_pii,
        customer_facing=inputs.customer_facing,
        high_stakes=inputs.high_stakes,
        autonomy_level=inputs.autonomy_level,
        sector=inputs.sector,
        modifiers=inputs.modifiers,
    )

    packs = load_policy_packs(Path("common/policy_packs"))
    controls = select_applicable_controls(packs, scenario)
    assert controls, "High-risk scenario should surface applicable safeguards"


@pytest.mark.parametrize(
    "inputs,expected_tier",
    [
        # Low tier scenarios (score 0-2)
        (RiskInputs(), "Low"),
        (RiskInputs(contains_pii=True), "Low"),
        (RiskInputs(customer_facing=True), "Low"),
        (RiskInputs(autonomy_level=1), "Low"),
        # Medium tier scenarios (score 3-5)
        (RiskInputs(contains_pii=True, customer_facing=True), "Medium"),
        (RiskInputs(high_stakes=True), "Medium"),
        (RiskInputs(contains_pii=True, autonomy_level=2), "Medium"),
        (RiskInputs(modifiers=["Cyber", "Bio"]), "Medium"),
        # High tier scenarios (score 6-8)
        (
            RiskInputs(contains_pii=True, customer_facing=True, high_stakes=True),
            "High",
        ),
        (
            RiskInputs(high_stakes=True, autonomy_level=3),
            "High",
        ),
        (
            RiskInputs(
                contains_pii=True,
                customer_facing=True,
                autonomy_level=2,
                sector="Healthcare",
            ),
            "High",
        ),
        # Critical tier scenarios (score 9+)
        (
            RiskInputs(
                contains_pii=True,
                customer_facing=True,
                high_stakes=True,
                autonomy_level=3,
            ),
            "Critical",
        ),
        (
            RiskInputs(
                contains_pii=True,
                customer_facing=True,
                high_stakes=True,
                modifiers=["Cyber", "Bio"],
            ),
            "Critical",
        ),
        (
            RiskInputs(
                contains_pii=True,
                customer_facing=True,
                high_stakes=True,
                autonomy_level=2,
                sector="Healthcare",
                modifiers=["Cyber"],
            ),
            "Critical",
        ),
    ],
)
def test_risk_tier_calculation(inputs, expected_tier):
    """Test various input combinations produce expected tiers."""
    assessment = calculate_risk_score(inputs)
    assert assessment.tier == expected_tier


def test_risk_score_zero_baseline():
    """Test that empty inputs produce zero score and Low tier."""
    inputs = RiskInputs()
    assessment = calculate_risk_score(inputs)

    assert assessment.score == 0
    assert assessment.tier == "Low"
    assert assessment.contributing_factors == []


def test_risk_score_pii_weight():
    """Test PII contributes correct weight."""
    inputs = RiskInputs(contains_pii=True)
    assessment = calculate_risk_score(inputs)

    assert assessment.score == 2
    assert "Contains PII (+2)" in assessment.contributing_factors


def test_risk_score_customer_facing_weight():
    """Test customer-facing contributes correct weight."""
    inputs = RiskInputs(customer_facing=True)
    assessment = calculate_risk_score(inputs)

    assert assessment.score == 2
    assert "Customer-facing exposure (+2)" in assessment.contributing_factors


def test_risk_score_high_stakes_weight():
    """Test high-stakes contributes correct weight."""
    inputs = RiskInputs(high_stakes=True)
    assessment = calculate_risk_score(inputs)

    assert assessment.score == 3
    assert "High-stakes impact (+3)" in assessment.contributing_factors


def test_risk_score_autonomy_levels():
    """Test autonomy level progression."""
    for level in range(4):
        inputs = RiskInputs(autonomy_level=level)
        assessment = calculate_risk_score(inputs)

        if level > 0:
            assert assessment.score == level
            assert f"Autonomy level {level} (+{level})" in assessment.contributing_factors
        else:
            assert assessment.score == 0


def test_risk_score_modifiers():
    """Test individual modifiers contribute correctly."""
    # High-weight modifiers
    for modifier in ["Cyber", "Bio"]:
        inputs = RiskInputs(modifiers=[modifier])
        assessment = calculate_risk_score(inputs)
        assert assessment.score == 2
        assert f"Modifier {modifier} (+2)" in assessment.contributing_factors

    # Lower-weight modifiers
    for modifier in ["Disinformation", "Children"]:
        inputs = RiskInputs(modifiers=[modifier])
        assessment = calculate_risk_score(inputs)
        assert assessment.score == 1
        assert f"Modifier {modifier} (+1)" in assessment.contributing_factors


def test_risk_score_multiple_modifiers():
    """Test multiple modifiers stack correctly."""
    inputs = RiskInputs(modifiers=["Cyber", "Bio", "Disinformation", "Children"])
    assessment = calculate_risk_score(inputs)

    # Cyber (2) + Bio (2) + Disinformation (1) + Children (1) = 6
    assert assessment.score == 6


def test_risk_score_sector_bumps():
    """Test sector sensitivity adds weight."""
    for sector in ["Healthcare", "Finance", "Critical Infrastructure", "Children"]:
        inputs = RiskInputs(sector=sector)
        assessment = calculate_risk_score(inputs)

        assert assessment.score == 1
        assert f"Sector sensitivity {sector} (+1)" in assessment.contributing_factors


def test_risk_score_general_sector_no_bump():
    """Test general sector adds no weight."""
    inputs = RiskInputs(sector="General")
    assessment = calculate_risk_score(inputs)

    assert assessment.score == 0
    assert not any("Sector" in factor for factor in assessment.contributing_factors)


def test_risk_score_additive_nature():
    """Test that all factors are correctly additive."""
    inputs = RiskInputs(
        contains_pii=True,  # +2
        customer_facing=True,  # +2
        high_stakes=True,  # +3
        autonomy_level=3,  # +3
        sector="Healthcare",  # +1
        modifiers=["Cyber", "Bio"],  # +2 +2
    )
    assessment = calculate_risk_score(inputs)

    # Total: 2 + 2 + 3 + 3 + 1 + 2 + 2 = 15
    assert assessment.score == 15
    assert assessment.tier == "Critical"
    # 7 factors: PII, customer-facing, high-stakes, autonomy, Cyber, Bio, Healthcare sector
    assert len(assessment.contributing_factors) == 7


def test_determine_risk_tier_thresholds():
    """Test tier boundaries are correct."""
    assert determine_risk_tier(0) == "Low"
    assert determine_risk_tier(1) == "Low"
    assert determine_risk_tier(2) == "Low"

    assert determine_risk_tier(3) == "Medium"
    assert determine_risk_tier(4) == "Medium"
    assert determine_risk_tier(5) == "Medium"

    assert determine_risk_tier(6) == "High"
    assert determine_risk_tier(7) == "High"
    assert determine_risk_tier(8) == "High"

    assert determine_risk_tier(9) == "Critical"
    assert determine_risk_tier(10) == "Critical"
    assert determine_risk_tier(100) == "Critical"


def test_risk_inputs_validation():
    """Test that RiskInputs validates autonomy level range."""
    # Valid autonomy levels
    for level in range(4):
        inputs = RiskInputs(autonomy_level=level)
        assert inputs.autonomy_level == level

    # Invalid autonomy levels should raise validation error
    with pytest.raises(Exception):  # Pydantic ValidationError
        RiskInputs(autonomy_level=-1)

    with pytest.raises(Exception):
        RiskInputs(autonomy_level=4)


def test_risk_inputs_defaults():
    """Test RiskInputs default values."""
    inputs = RiskInputs()

    assert inputs.contains_pii is False
    assert inputs.customer_facing is False
    assert inputs.high_stakes is False
    assert inputs.autonomy_level == 0
    assert inputs.sector == "General"
    assert inputs.modifiers == []


def test_risk_inputs_forbids_extra_fields():
    """Test that RiskInputs rejects unknown fields."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        RiskInputs(unknown_field="value")


def test_contributing_factors_completeness():
    """Ensure all contributing factors are captured in output."""
    inputs = RiskInputs(
        contains_pii=True,
        customer_facing=True,
        high_stakes=True,
        autonomy_level=2,
        sector="Finance",
        modifiers=["Cyber"],
    )
    assessment = calculate_risk_score(inputs)

    # Should have 6 factors
    assert len(assessment.contributing_factors) == 6
    assert any("PII" in f for f in assessment.contributing_factors)
    assert any("Customer-facing" in f for f in assessment.contributing_factors)
    assert any("High-stakes" in f for f in assessment.contributing_factors)
    assert any("Autonomy" in f for f in assessment.contributing_factors)
    assert any("Sector" in f for f in assessment.contributing_factors)
    assert any("Modifier" in f for f in assessment.contributing_factors)
