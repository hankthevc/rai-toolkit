"""Exercise the risk engine scoring heuristic."""

from pathlib import Path

from common.utils.policy_loader import ScenarioContext, load_policy_packs, select_applicable_controls
from common.utils.risk_engine import RiskInputs, calculate_risk_score


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
