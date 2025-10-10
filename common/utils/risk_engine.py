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


def check_sensitive_use_gating(inputs: RiskInputs, assessment: RiskAssessment) -> Dict[str, any]:
    """
    Illustrative sensitive use gating heuristic (demonstrative triage logic).
    
    This is a demonstration of how to implement escalation gates for high-risk AI systems.
    Real implementations should be validated with legal, compliance, and executive leadership.
    
    Args:
        inputs: The risk input scenario
        assessment: The calculated risk assessment
        
    Returns:
        Dict with keys: requires_escalation (bool), escalation_reason (str), approval_level (str)
    """
    
    escalation_flags = []
    approval_level = "Standard Approval"
    
    # Critical tier + sensitive modifiers = Executive review
    if assessment.tier == "Critical":
        if "Bio" in inputs.modifiers or "Cyber" in inputs.modifiers:
            escalation_flags.append("Critical tier system with Bio/Cyber implications")
            approval_level = "Executive + Legal Sign-Off"
    
    # Biometric identification + real-time classification = Restricted use
    # (EU AI Act Annex III, Article 5 considerations)
    biometric_keywords = ["biometric", "facial recognition", "emotion recognition", "gait analysis"]
    if inputs.customer_facing and inputs.high_stakes:
        # Check modifiers for biometric indicators (simplified for demo)
        if any(keyword in str(inputs.modifiers).lower() for keyword in biometric_keywords):
            escalation_flags.append("Biometric identification in customer-facing, high-stakes context")
            approval_level = "Restricted Use Review + Legal Sign-Off"
    
    # Real-time behavioral monitoring of protected populations
    if inputs.protected_populations and inputs.autonomy_level >= 2:
        if "Children" in inputs.protected_populations or "Elderly" in inputs.protected_populations:
            escalation_flags.append("Automated decisions affecting protected populations (children/elderly)")
            approval_level = "Privacy + Civil Rights Review"
    
    # Irreversible decisions at high stakes
    if inputs.decision_reversible == "Irreversible" and inputs.high_stakes:
        escalation_flags.append("Irreversible high-stakes decisions (e.g., medical diagnosis, employment termination)")
        approval_level = "Executive + Legal + Ethics Review"
    
    # Dual-use risk at Critical tier
    if inputs.dual_use_risk in ["High (Weaponization)", "Export Control"]:
        if assessment.tier in ["High", "Critical"]:
            escalation_flags.append(f"Dual-use risk: {inputs.dual_use_risk}")
            approval_level = "National Security + Legal Review"
    
    # Generative AI producing synthetic content at scale
    if inputs.model_type == "Generative AI / LLM" and inputs.generates_synthetic_content:
        if inputs.customer_facing and inputs.autonomy_level >= 2:
            escalation_flags.append("Generative AI producing synthetic content for external users without human review")
            approval_level = "Misinformation Risk Review + Legal"
    
    # Determine if escalation is required
    requires_escalation = len(escalation_flags) > 0
    escalation_reason = "; ".join(escalation_flags) if escalation_flags else "No sensitive use patterns detected"
    
    return {
        "requires_escalation": requires_escalation,
        "escalation_reason": escalation_reason,
        "approval_level": approval_level,
        "escalation_flags": escalation_flags
    }


def check_stop_ship_triggers(
    inputs: RiskInputs,
    assessment: RiskAssessment,
) -> List[str]:
    """
    Check if scenario triggers any stop-ship rules.
    
    Stop-ship rules represent hard gates that halt deployment until specific safeguards
    are verified. Based on the methodology in docs/methodology_project1.md.
    
    Args:
        inputs: The risk input scenario
        assessment: The calculated risk assessment
        
    Returns:
        List of triggered stop-ship rules with required actions
    """
    triggered_rules = []
    
    # Rule 1: Critical + PII + Irreversible Decisions
    if (assessment.tier == "Critical" and 
        inputs.contains_pii and 
        inputs.decision_reversible == "Irreversible"):
        triggered_rules.append(
            "**Critical + PII + Irreversible:** Legal review, DPIA, appeals mechanism, VP sign-off required (GDPR Art. 22, EU AI Act)"
        )
    
    # Rule 2: Critical + Protected Populations
    protected_groups = ["Children", "Elderly", "People with Disabilities"]
    if assessment.tier == "Critical" and inputs.protected_populations:
        if any(group in inputs.protected_populations for group in protected_groups):
            triggered_rules.append(
                "**Critical + Protected Populations:** Accessibility audit (WCAG 2.1 AA), bias testing, civil rights consultation required (ADA, COPPA)"
            )
    
    # Rule 3: Critical + High Dual-Use Risk
    if assessment.tier == "Critical" and inputs.dual_use_risk in ["High (Weaponization)", "Export Control"]:
        triggered_rules.append(
            "**Critical + High Dual-Use:** Export control classification, red team testing, restricted access controls required (EAR/ITAR)"
        )
    
    # Rule 4: High + Healthcare/Finance Sector
    if assessment.tier == "High" and inputs.sector in ["Healthcare", "Finance"]:
        sector_reqs = "HIPAA compliance" if inputs.sector == "Healthcare" else "GLBA/SR 11-7 compliance"
        triggered_rules.append(
            f"**High + {inputs.sector}:** {sector_reqs}, sector-specific security assessment required"
        )
    
    # Rule 5: High + External API + PII
    if (assessment.tier == "High" and 
        inputs.uses_foundation_model == "External API (OpenAI/Anthropic/etc.)" and 
        inputs.contains_pii):
        triggered_rules.append(
            "**High + External API + PII:** Vendor contract review, data leakage assessment, encryption verification required"
        )
    
    # Rule 6: High + Real-Time Learning
    if assessment.tier == "High" and inputs.learns_in_production:
        triggered_rules.append(
            "**High + Real-Time Learning:** Poisoning mitigation, drift monitoring, rollback procedures required (MITRE ATLAS AML.T0018)"
        )
    
    # Rule 7: Synthetic Content Generation (all tiers)
    if inputs.generates_synthetic_content:
        triggered_rules.append(
            "**Synthetic Content Generation:** Watermarking/provenance (C2PA), user disclosure per EU AI Act Art. 52, abuse monitoring required"
        )
    
    # Rule 8: Missing ownership is handled by exporters.py with fallback values
    # We don't check it here since owner/approver aren't part of RiskInputs
    
    return triggered_rules
