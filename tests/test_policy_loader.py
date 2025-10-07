"""Test policy pack loading and control matching logic."""

from pathlib import Path

import pytest

from common.utils.policy_loader import (
    PolicyControl,
    ScenarioContext,
    WhenClause,
    control_matches,
    load_policy_pack,
    load_policy_packs,
    select_applicable_controls,
)


def test_control_matches_tier():
    """Test tier-based matching."""
    control = PolicyControl(
        id="TEST-01",
        title="High risk control",
        description="Only for high risk",
        authority="Test",
        clause="1.1",
        evidence="Test evidence",
        tags=["test"],
        when=WhenClause(tier=["High", "Critical"]),
    )

    scenario_high = ScenarioContext(tier="High")
    scenario_low = ScenarioContext(tier="Low")

    assert control_matches(control, scenario_high)
    assert not control_matches(control, scenario_low)


def test_control_matches_pii():
    """Test PII-based matching."""
    control = PolicyControl(
        id="TEST-02",
        title="PII control",
        description="For PII scenarios",
        authority="Test",
        clause="2.1",
        evidence="Test evidence",
        tags=["pii"],
        when=WhenClause(contains_pii=True),
    )

    scenario_with_pii = ScenarioContext(tier="Medium", contains_pii=True)
    scenario_without_pii = ScenarioContext(tier="Medium", contains_pii=False)

    assert control_matches(control, scenario_with_pii)
    assert not control_matches(control, scenario_without_pii)


def test_control_matches_customer_facing():
    """Test customer-facing matching."""
    control = PolicyControl(
        id="TEST-03",
        title="Customer control",
        description="For customer-facing",
        authority="Test",
        clause="3.1",
        evidence="Test evidence",
        tags=["customer"],
        when=WhenClause(customer_facing=True),
    )

    scenario_customer = ScenarioContext(tier="Low", customer_facing=True)
    scenario_internal = ScenarioContext(tier="Low", customer_facing=False)

    assert control_matches(control, scenario_customer)
    assert not control_matches(control, scenario_internal)


def test_control_matches_high_stakes():
    """Test high-stakes matching."""
    control = PolicyControl(
        id="TEST-04",
        title="High stakes control",
        description="For high-stakes scenarios",
        authority="Test",
        clause="4.1",
        evidence="Test evidence",
        tags=["stakes"],
        when=WhenClause(high_stakes=True),
    )

    scenario_high_stakes = ScenarioContext(tier="Medium", high_stakes=True)
    scenario_low_stakes = ScenarioContext(tier="Medium", high_stakes=False)

    assert control_matches(control, scenario_high_stakes)
    assert not control_matches(control, scenario_low_stakes)


def test_control_matches_autonomy_level():
    """Test autonomy level threshold matching."""
    control = PolicyControl(
        id="TEST-05",
        title="Autonomy control",
        description="For high autonomy",
        authority="Test",
        clause="5.1",
        evidence="Test evidence",
        tags=["autonomy"],
        when=WhenClause(autonomy_at_least=2),
    )

    scenario_high_autonomy = ScenarioContext(tier="Low", autonomy_level=3)
    scenario_medium_autonomy = ScenarioContext(tier="Low", autonomy_level=2)
    scenario_low_autonomy = ScenarioContext(tier="Low", autonomy_level=1)

    assert control_matches(control, scenario_high_autonomy)
    assert control_matches(control, scenario_medium_autonomy)
    assert not control_matches(control, scenario_low_autonomy)


def test_control_matches_sector():
    """Test sector-based matching."""
    control = PolicyControl(
        id="TEST-06",
        title="Healthcare control",
        description="For healthcare sector",
        authority="Test",
        clause="6.1",
        evidence="Test evidence",
        tags=["sector"],
        when=WhenClause(sector=["Healthcare", "Finance"]),
    )

    scenario_healthcare = ScenarioContext(tier="Low", sector="Healthcare")
    scenario_finance = ScenarioContext(tier="Low", sector="Finance")
    scenario_general = ScenarioContext(tier="Low", sector="General")

    assert control_matches(control, scenario_healthcare)
    assert control_matches(control, scenario_finance)
    assert not control_matches(control, scenario_general)


def test_control_matches_modifiers():
    """Test modifier-based matching."""
    control = PolicyControl(
        id="TEST-07",
        title="Cyber control",
        description="For cyber scenarios",
        authority="Test",
        clause="7.1",
        evidence="Test evidence",
        tags=["cyber"],
        when=WhenClause(modifiers=["Cyber", "Bio"]),
    )

    scenario_cyber = ScenarioContext(tier="Low", modifiers=["Cyber"])
    scenario_bio = ScenarioContext(tier="Low", modifiers=["Bio"])
    scenario_both = ScenarioContext(tier="Low", modifiers=["Cyber", "Bio"])
    scenario_other = ScenarioContext(tier="Low", modifiers=["Disinformation"])
    scenario_none = ScenarioContext(tier="Low", modifiers=[])

    assert control_matches(control, scenario_cyber)
    assert control_matches(control, scenario_bio)
    assert control_matches(control, scenario_both)
    assert not control_matches(control, scenario_other)
    assert not control_matches(control, scenario_none)


def test_control_matches_multiple_conditions():
    """Test control with multiple conditions (all must match)."""
    control = PolicyControl(
        id="TEST-08",
        title="Complex control",
        description="Multiple conditions",
        authority="Test",
        clause="8.1",
        evidence="Test evidence",
        tags=["complex"],
        when=WhenClause(
            tier=["High", "Critical"],
            contains_pii=True,
            customer_facing=True,
        ),
    )

    # All conditions met
    scenario_match = ScenarioContext(
        tier="High",
        contains_pii=True,
        customer_facing=True,
    )

    # Missing PII
    scenario_no_pii = ScenarioContext(
        tier="High",
        contains_pii=False,
        customer_facing=True,
    )

    # Wrong tier
    scenario_wrong_tier = ScenarioContext(
        tier="Low",
        contains_pii=True,
        customer_facing=True,
    )

    assert control_matches(control, scenario_match)
    assert not control_matches(control, scenario_no_pii)
    assert not control_matches(control, scenario_wrong_tier)


def test_control_matches_empty_when_clause():
    """Test control with no conditions (should always match)."""
    control = PolicyControl(
        id="TEST-09",
        title="Universal control",
        description="Always applies",
        authority="Test",
        clause="9.1",
        evidence="Test evidence",
        tags=["universal"],
        when=WhenClause(),
    )

    scenario_high = ScenarioContext(tier="High", contains_pii=True)
    scenario_low = ScenarioContext(tier="Low", contains_pii=False)

    assert control_matches(control, scenario_high)
    assert control_matches(control, scenario_low)


def test_load_policy_pack():
    """Test loading a single policy pack."""
    pack_path = Path("common/policy_packs/nist_ai_rmf.yaml")
    pack = load_policy_pack(pack_path)

    assert pack.name
    assert pack.version
    assert pack.description
    assert len(pack.controls) > 0


def test_load_policy_packs():
    """Test loading all policy packs from directory."""
    packs_dir = Path("common/policy_packs")
    packs = load_policy_packs(packs_dir)

    assert len(packs) >= 5
    for pack in packs:
        assert pack.name
        assert pack.controls


def test_load_policy_packs_empty_directory(tmp_path):
    """Test that loading from empty directory raises error."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    with pytest.raises(FileNotFoundError):
        load_policy_packs(empty_dir)


def test_select_applicable_controls():
    """Test selecting controls across multiple packs."""
    packs = load_policy_packs(Path("common/policy_packs"))

    # High-risk scenario should trigger multiple controls
    scenario_high_risk = ScenarioContext(
        tier="High",
        contains_pii=True,
        customer_facing=True,
        high_stakes=True,
        autonomy_level=2,
        sector="Healthcare",
        modifiers=["Cyber"],
    )

    controls = select_applicable_controls(packs, scenario_high_risk)
    assert len(controls) > 0

    # Verify all returned controls actually match
    for control in controls:
        assert control_matches(control, scenario_high_risk)


def test_select_applicable_controls_low_risk():
    """Test that low-risk scenarios get fewer controls."""
    packs = load_policy_packs(Path("common/policy_packs"))

    scenario_low_risk = ScenarioContext(
        tier="Low",
        contains_pii=False,
        customer_facing=False,
        high_stakes=False,
        autonomy_level=0,
        sector="General",
        modifiers=[],
    )

    controls = select_applicable_controls(packs, scenario_low_risk)

    # Low risk should have fewer controls than high risk
    scenario_high_risk = ScenarioContext(
        tier="Critical",
        contains_pii=True,
        customer_facing=True,
        high_stakes=True,
        autonomy_level=3,
        sector="Healthcare",
        modifiers=["Cyber", "Bio"],
    )

    high_risk_controls = select_applicable_controls(packs, scenario_high_risk)
    assert len(controls) < len(high_risk_controls)


def test_policy_control_tags_default():
    """Test that tags default to empty list if not provided."""
    control = PolicyControl(
        id="TEST-10",
        title="Test",
        description="Test",
        authority="Test",
        clause="10.1",
        evidence="Test",
        tags=None,  # Will be converted to []
        when=WhenClause(),
    )

    assert control.tags == []


def test_scenario_context_defaults():
    """Test ScenarioContext default values."""
    scenario = ScenarioContext(tier="Low")

    assert scenario.contains_pii is False
    assert scenario.customer_facing is False
    assert scenario.high_stakes is False
    assert scenario.autonomy_level == 0
    assert scenario.sector == "General"
    assert scenario.modifiers == []

