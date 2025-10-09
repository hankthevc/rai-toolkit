"""Simple, interview-ready risk engine used by the Streamlit UI."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field

# Weights are intentionally transparent so candidates can explain the heuristic.
# Original weights
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

# New factor weights
MODEL_TYPE_WEIGHTS: Dict[str, int] = {
    "Traditional ML": 0,
    "Generative AI / LLM": 2,  # Prompt injection, hallucinations, data leakage
    "Computer Vision": 1,  # Deepfakes, adversarial examples
    "Multimodal": 2,  # Increased attack surface
    "Reinforcement Learning": 2,  # Reward hacking, emergent behavior
}

DATA_SOURCE_WEIGHTS: Dict[str, int] = {
    "Proprietary/Internal": 0,
    "Public Datasets": 0,
    "Internet-Scraped": 2,  # Copyright, bias, PII contamination
    "User-Generated": 1,  # Poisoning risk
    "Third-Party/Vendor": 1,  # Supply chain integrity
    "Synthetic": 1,  # Quality concerns
}

EXPLAINABILITY_WEIGHTS: Dict[str, int] = {
    "Inherently Interpretable": 0,
    "Post-hoc Explainable": 0,
    "Limited Explainability": 1,
    "Black Box": 2,  # Regulatory compliance, debugging difficulty
}

FOUNDATION_MODEL_WEIGHTS: Dict[str, int] = {
    "No Third-Party": 0,
    "Self-Hosted Open Source": 1,  # Supply chain, maintenance
    "Self-Hosted Proprietary": 1,
    "External API": 2,  # Data leakage, vendor dependency
    "Hybrid": 1,
}

DUAL_USE_WEIGHTS: Dict[str, int] = {
    "None": 0,
    "Low": 0,
    "Moderate": 1,
    "High": 3,  # Export controls, misuse potential
}

REVERSIBILITY_WEIGHTS: Dict[str, int] = {
    "Fully Reversible": 0,
    "Reversible with Cost": 1,
    "Difficult to Reverse": 2,
    "Irreversible": 3,  # Requires highest safeguards
}

PROTECTED_POPULATION_WEIGHTS: Dict[str, int] = {
    "Children": 2,
    "Elderly": 1,
    "People with Disabilities": 2,
    "Low-Income / Unbanked": 1,
    "Non-Native Speakers / Low Literacy": 1,
    "Asylum Seekers / Immigrants": 2,
    "Incarcerated Persons": 2,
    "Healthcare Vulnerable": 2,
}


class RiskInputs(BaseModel):
    """Scenario attributes that influence the additive risk score."""

    # Original risk factors
    contains_pii: bool = False
    customer_facing: bool = False
    high_stakes: bool = False
    autonomy_level: int = Field(default=0, ge=0, le=3)
    sector: str = "General"
    modifiers: List[str] = Field(default_factory=list)
    
    # Technical AI/ML risks
    model_type: str = "Traditional ML"
    data_source: str = "Proprietary/Internal"
    learns_in_production: bool = False
    
    # Privacy & data governance
    international_data: bool = False
    explainability_level: str = "Post-hoc Explainable"
    
    # Supply chain & dependencies
    uses_foundation_model: str = "No Third-Party"
    
    # Content & misuse risks
    generates_synthetic_content: bool = False
    dual_use_risk: str = "None"
    
    # Rights & equity
    decision_reversible: str = "Fully Reversible"
    protected_populations: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid", protected_namespaces=())


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

    # Original risk factors
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

    # New risk factors
    model_weight = MODEL_TYPE_WEIGHTS.get(inputs.model_type, 0)
    if model_weight:
        score += model_weight
        factors.append(f"Model type {inputs.model_type} (+{model_weight})")

    data_weight = DATA_SOURCE_WEIGHTS.get(inputs.data_source, 0)
    if data_weight:
        score += data_weight
        factors.append(f"Data source {inputs.data_source} (+{data_weight})")

    if inputs.learns_in_production:
        score += 2
        factors.append("Real-time learning (+2)")

    if inputs.international_data:
        score += 2
        factors.append("Cross-border data transfers (+2)")

    explain_weight = EXPLAINABILITY_WEIGHTS.get(inputs.explainability_level, 0)
    if explain_weight:
        score += explain_weight
        factors.append(f"Explainability: {inputs.explainability_level} (+{explain_weight})")

    foundation_weight = FOUNDATION_MODEL_WEIGHTS.get(inputs.uses_foundation_model, 0)
    if foundation_weight:
        score += foundation_weight
        factors.append(f"Foundation model: {inputs.uses_foundation_model} (+{foundation_weight})")

    if inputs.generates_synthetic_content:
        base_weight = 1
        # Higher risk if customer-facing synthetic content
        if inputs.customer_facing:
            base_weight = 2
            factors.append("Customer-facing synthetic content (+2)")
        else:
            factors.append("Generates synthetic content (+1)")
        score += base_weight

    dual_use_weight = DUAL_USE_WEIGHTS.get(inputs.dual_use_risk, 0)
    if dual_use_weight:
        score += dual_use_weight
        factors.append(f"Dual-use risk: {inputs.dual_use_risk} (+{dual_use_weight})")

    reversibility_weight = REVERSIBILITY_WEIGHTS.get(inputs.decision_reversible, 0)
    if reversibility_weight:
        score += reversibility_weight
        factors.append(f"Decision reversibility: {inputs.decision_reversible} (+{reversibility_weight})")

    for population in inputs.protected_populations:
        weight = PROTECTED_POPULATION_WEIGHTS.get(population, 1)
        score += weight
        factors.append(f"Protected population: {population} (+{weight})")

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
