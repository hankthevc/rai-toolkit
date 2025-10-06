"""Simple, interview-ready risk engine used by the Streamlit UI."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field

# Weights are intentionally transparent so candidates can explain the heuristic.
PII_WEIGHT = 2
CUSTOMER_FACING_WEIGHT = 2
HIGH_STAKES_WEIGHT = 3
MODIFIER_WEIGHTS: Dict[str, int] = {"Bio": 2, "Cyber": 2, "Disinformation": 1, "Children": 1}
SECTOR_BUMPS: Dict[str, int] = {
    "Healthcare": 1,
    "Finance": 1,
    "Critical Infrastructure": 1,
    "Children": 1,
}


class RiskInputs(BaseModel):
    """Scenario attributes that influence the additive risk score."""

    contains_pii: bool = False
    customer_facing: bool = False
    high_stakes: bool = False
    autonomy_level: int = Field(default=0, ge=0, le=3)
    sector: str = "General"
    modifiers: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


@dataclass
class RiskAssessment:
    """Result bundle returned to the UI and policy selector."""

    score: int
    tier: str
    contributing_factors: List[str] = field(default_factory=list)


THRESHOLDS = {
    2: "Low",
    5: "Medium",
    8: "High",
}


def calculate_risk_score(inputs: RiskInputs) -> RiskAssessment:
    """Compute an additive risk score with a transparent explanation."""

    score = 0
    factors: List[str] = []

    if inputs.contains_pii:
        score += PII_WEIGHT
        factors.append("Contains PII (+2)")

    if inputs.customer_facing:
        score += CUSTOMER_FACING_WEIGHT
        factors.append("Customer-facing exposure (+2)")

    if inputs.high_stakes:
        score += HIGH_STAKES_WEIGHT
        factors.append("High-stakes impact (+3)")

    score += inputs.autonomy_level
    if inputs.autonomy_level:
        factors.append(f"Autonomy level {inputs.autonomy_level} (+{inputs.autonomy_level})")

    for modifier in inputs.modifiers:
        weight = MODIFIER_WEIGHTS.get(modifier, 0)
        if weight:
            score += weight
            factors.append(f"Modifier {modifier} (+{weight})")

    sector_weight = SECTOR_BUMPS.get(inputs.sector, 0)
    if sector_weight:
        score += sector_weight
        factors.append(f"Sector sensitivity {inputs.sector} (+{sector_weight})")

    tier = determine_risk_tier(score)
    return RiskAssessment(score=score, tier=tier, contributing_factors=factors)


def determine_risk_tier(score: int) -> str:
    """Translate a numeric score into a Low/Medium/High/Critical tier."""

    # Thresholds intentionally mirror the interview brief to stay explainable.
    if score <= 2:
        return "Low"
    if score <= 5:
        return "Medium"
    if score <= 8:
        return "High"
    return "Critical"
