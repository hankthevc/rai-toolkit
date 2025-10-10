"""AI-powered scenario parsing to autofill risk assessment forms.

This module uses OpenAI's API to analyze plain-language use case descriptions
and suggest risk modifier values, demonstrating governance-as-code meets LLM capabilities.
"""

from __future__ import annotations

import os
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class ScenarioAnalysis(BaseModel):
    """Structured output from AI scenario parsing."""
    
    model_config = ConfigDict(protected_namespaces=())

    # Original factors
    contains_pii: bool = Field(
        description="Whether the scenario processes personal or sensitive data (PII, PHI, financial records, etc.)"
    )
    customer_facing: bool = Field(
        description="Whether the AI system has customer-facing or external exposure"
    )
    high_stakes: bool = Field(
        description="Whether outcomes involve safety, rights, or financial impact"
    )
    autonomy_level: int = Field(
        ge=0,
        le=3,
        description="0=suggestion only, 1=human-in-loop, 2=human oversight, 3=full autonomy"
    )
    sector: str = Field(
        description="Primary sector: General, Healthcare, Finance, Critical Infrastructure, or Children"
    )
    modifiers: list[str] = Field(
        default_factory=list,
        description="Scenario modifiers from: Bio, Cyber, Disinformation, Children"
    )
    
    # New risk factors (all with defaults for backward compatibility)
    model_type: str = Field(
        default="Traditional ML",
        description="AI architecture: Traditional ML, Generative AI / LLM, Computer Vision, Multimodal, or Reinforcement Learning"
    )
    data_source: str = Field(
        default="Proprietary/Internal",
        description="Training data source: Proprietary/Internal, Public Datasets, Internet-Scraped, User-Generated, Third-Party/Vendor, or Synthetic"
    )
    learns_in_production: bool = Field(
        default=False,
        description="Whether the model updates/learns from production data (online learning)"
    )
    international_data: bool = Field(
        default=False,
        description="Whether the system transfers personal data across international borders"
    )
    explainability_level: str = Field(
        default="Post-hoc Explainable",
        description="Model interpretability: Inherently Interpretable, Post-hoc Explainable, Limited Explainability, or Black Box"
    )
    uses_foundation_model: str = Field(
        default="No Third-Party",
        description="Third-party model usage: No Third-Party, Self-Hosted Open Source, Self-Hosted Proprietary, External API, or Hybrid"
    )
    generates_synthetic_content: bool = Field(
        default=False,
        description="Whether the system creates synthetic text, images, audio, or video"
    )
    dual_use_risk: str = Field(
        default="None",
        description="Potential for misuse: None, Low, Moderate, or High"
    )
    decision_reversible: str = Field(
        default="Fully Reversible",
        description="Can decisions be undone: Fully Reversible, Reversible with Cost, Difficult to Reverse, or Irreversible"
    )
    protected_populations: list[str] = Field(
        default_factory=list,
        description="Vulnerable groups affected (from: Children, Elderly, People with Disabilities, Low-Income / Unbanked, Non-Native Speakers / Low Literacy, Asylum Seekers / Immigrants, Incarcerated Persons, Healthcare Vulnerable)"
    )
    
    # AI analysis outputs
    reasoning: str = Field(
        default="AI analysis in progress",
        description="Brief explanation of the analysis for transparency"
    )
    estimated_risk_tier: str = Field(
        default="Medium",
        description="AI's estimated risk tier: Low, Medium, High, or Critical"
    )
    key_risk_factors: list[str] = Field(
        default_factory=list,
        description="3-5 specific risk factors identified in this scenario"
    )
    recommended_safeguards: list[str] = Field(
        default_factory=list,
        description="5-7 specific governance controls that should apply (based on NIST AI RMF, EU AI Act, OWASP, etc.)"
    )
    framework_alignment: str = Field(
        default="General AI governance frameworks apply",
        description="Which governance frameworks are most relevant (e.g., 'EU AI Act High-Risk', 'NIST AI RMF Govern functions', 'OWASP LLM risks')"
    )
    gaps_and_limitations: list[str] = Field(
        default_factory=list,
        description="Specific regulatory/compliance areas that couldn't be fully assessed due to missing information. List what additional details would be needed for comprehensive assessment."
    )


SYSTEM_PROMPT = """You are an AI governance analyst helping assess AI system risks against established frameworks (NIST AI RMF, EU AI Act, ISO 42001, OWASP LLM Top 10, MITRE ATLAS, US OMB AI Policy).

Analyze the use case comprehensively across 20+ risk dimensions and provide governance recommendations.

**CORE RISK FACTORS:**

1. **contains_pii**: True if processes personal/sensitive data (PII, PHI, financial records, location, biometrics)

2. **customer_facing**: True if external users/customers directly interact with the system

3. **high_stakes**: True if outcomes significantly impact safety, rights, or finances
   - Safety: physical harm, medical decisions, critical infrastructure
   - Rights: employment, credit, legal proceedings, civil liberties  
   - Finances: significant monetary impact, fraud, trading

4. **autonomy_level** (0-3):
   - 0: Suggestion only (code completion, writing assistant)
   - 1: Human-in-loop (resume screening with review, content moderation queue)
   - 2: Human oversight with escalation (chatbot, fraud detection with thresholds)
   - 3: Full autonomy (automated trading, autonomous vehicles, real-time filtering)

5. **sector**: General, Healthcare, Finance, Critical Infrastructure, or Children

6. **modifiers**: Bio, Cyber, Disinformation, Children (select all that apply)

**TECHNICAL AI/ML RISKS:**

7. **model_type**: Architecture determines threat model
   - Traditional ML: classification, regression, clustering
   - Generative AI / LLM: text/code generation (OWASP LLM risks)
   - Computer Vision: image recognition (deepfakes, adversarial examples)
   - Multimodal: text+image+audio (increased attack surface)
   - Reinforcement Learning: autonomous agents (reward hacking)

8. **data_source**: Training data provenance
   - Proprietary/Internal: controlled curation
   - Public Datasets: ImageNet, Common Crawl  
   - Internet-Scraped: copyright/bias/PII risks
   - User-Generated: poisoning risk
   - Third-Party/Vendor: supply chain integrity
   - Synthetic: AI-generated training data

9. **learns_in_production**: Boolean - does it update from production data?
   - True: data poisoning, drift, loss of reproducibility
   - False: static, auditable

**PRIVACY & DATA GOVERNANCE:**

10. **international_data**: Boolean - cross-border data transfers?
    - True: GDPR adequacy, Schrems II, data sovereignty concerns

11. **explainability_level**: Model interpretability
    - Inherently Interpretable: linear models, decision trees
    - Post-hoc Explainable: SHAP, LIME, attention viz
    - Limited Explainability: complex ensembles
    - Black Box: foundation models, proprietary APIs (GDPR Art. 22 risk)

**SUPPLY CHAIN & DEPENDENCIES:**

12. **uses_foundation_model**: Third-party model usage
    - No Third-Party: fully in-house
    - Self-Hosted Open Source: Llama, Mistral on own infrastructure
    - Self-Hosted Proprietary: licensed models on-prem
    - External API: OpenAI, Anthropic, Google (data leakage risk)
    - Hybrid: RAG with external embeddings

**CONTENT & MISUSE RISKS:**

13. **generates_synthetic_content**: Boolean - creates text/images/audio/video?
    - True: deepfake risk, C2PA provenance requirements, EU AI Act Art. 52

14. **dual_use_risk**: Weaponization potential
    - None: single benign purpose
    - Low: minimal misuse potential
    - Moderate: could be adapted for harm (facial recognition → surveillance)
    - High: direct dual-use (bio research AI, cyber tools, persuasion systems)

**RIGHTS & EQUITY:**

15. **decision_reversible**: Can decisions be appealed/undone?
    - Fully Reversible: no harm to undo (recommendations)
    - Reversible with Cost: time/money to appeal (loan denial)
    - Difficult to Reverse: significant harm (reputation damage)
    - Irreversible: cannot undo (autonomous weapons, some medical interventions)

16. **protected_populations**: Vulnerable groups (select all that apply)
    - Children
    - Elderly
    - People with Disabilities
    - Low-Income / Unbanked
    - Non-Native Speakers / Low Literacy
    - Asylum Seekers / Immigrants
    - Incarcerated Persons
    - Healthcare Vulnerable

**AI ANALYSIS OUTPUTS:**

17. **reasoning**: 2-3 sentences explaining your risk tier assessment

18. **estimated_risk_tier**: Low, Medium, High, or Critical
    - Consider cumulative effect of all factors above

19. **key_risk_factors**: List 3-5 specific risks for THIS scenario

20. **recommended_safeguards**: List 5-7 controls with framework citations
    - Example: "Human oversight for prescription changes (NIST AI RMF GOVERN-1.2)"

21. **framework_alignment**: Which standards apply and why
    - EU AI Act Annex III (high-risk systems)
    - NIST AI RMF functions (GOVERN/MAP/MEASURE/MANAGE)
    - OWASP LLM Top 10 (if LLM)
    - MITRE ATLAS (if adversarial threats)
    - GDPR, ISO 42001, OMB M-24-10 as applicable

**Instructions:**
- Be conservative - err toward higher risk when uncertain
- Consider interaction effects (e.g., LLM + customer-facing + healthcare = critical)
- Your analysis will be shown alongside a traditional scoring model

**CRITICAL - Gaps & Limitations (NEW):**
This is a DEMO tool, not production assessment. The user may not have provided complete information.

**Populate `gaps_and_limitations` with specific unknowns that prevent full regulatory assessment:**

Examples of gaps to identify:
- "Data storage location unknown - can't assess GDPR/Schrems II cross-border transfer compliance"
- "No information about BAA status - can't confirm HIPAA compliance for PHI processing"
- "Vendor contract terms unknown - can't evaluate data sharing/DPA requirements"
- "Human oversight details unclear - EU AI Act Art. 14 requirements may apply"
- "Security architecture not described - can't assess MITRE ATLAS threat model applicability"
- "Model training data lineage unknown - copyright/licensing risks unclear"

**When to populate gaps_and_limitations:**
- If you had to make assumptions due to missing details
- If critical regulatory requirements can't be verified from description
- If compliance assessment would require information not provided

**IMPORTANT - Re-Analysis with Additional Context:**
If you see "Previous Assessment Gaps:" in the input, the user is providing additional context to fill those gaps.
- Review the previous gaps carefully
- Check if the "Additional Context to Address Gaps:" section resolves them
- ONLY list gaps that are still unresolved after considering the new information
- If a gap is resolved, incorporate that information into your analysis and remove it from gaps_and_limitations
- Update your risk assessment, reasoning, and recommendations based on the new information
- **In your `reasoning` field, explicitly mention which gaps were addressed** and how the new information affected your analysis (e.g., "The additional context confirms HIPAA BAA compliance, which reduces regulatory risk..." or "Knowing the data is stored in AWS us-east-1 clarifies GDPR applicability...")

**Keep it specific and actionable** - tell the user exactly what additional info would help."""


def parse_scenario_with_ai(
    use_case_description: str,
    api_key: Optional[str] = None,
    model: str = "gpt-4o",  # Using gpt-4o for better structured output support
    demo_mode: bool = False,
) -> Optional[ScenarioAnalysis]:
    """Parse a plain-language AI scenario and suggest risk assessment values.

    Args:
        use_case_description: Plain-language description of the AI use case
        api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        model: OpenAI model to use (gpt-4o-mini for cost efficiency, gpt-4o for accuracy)
        demo_mode: If True, return canned response without API call

    Returns:
        ScenarioAnalysis with suggested values, or None if parsing fails

    Example:
        >>> analysis = parse_scenario_with_ai(
        ...     "A chatbot that helps hospital patients schedule appointments and refill prescriptions"
        ... )
        >>> if analysis:
        ...     print(f"PII: {analysis.contains_pii}, Sector: {analysis.sector}")
    """
    from .openai_helpers import safe_openai_call

    if not use_case_description or not use_case_description.strip():
        return None

    api_key = api_key or os.getenv("OPENAI_API_KEY")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Analyze this AI use case and suggest risk assessment values:\n\n{use_case_description}"
        }
    ]

    result = safe_openai_call(
        messages=messages,
        model=model,
        temperature=0.3,
        response_format=ScenarioAnalysis,
        demo_mode=demo_mode,
        api_key=api_key,
    )

    if result["success"]:
        return result["data"]
    else:
        # Log error but don't crash
        print(f"AI parsing failed: {result.get('error', 'Unknown error')}")
        return None


def format_analysis_summary(analysis: ScenarioAnalysis) -> str:
    """Format the AI analysis into a human-readable summary.

    Args:
        analysis: Parsed scenario analysis

    Returns:
        Markdown-formatted summary for display in UI
    """
    autonomy_labels = {
        0: "Suggestion only",
        1: "Human-in-the-loop",
        2: "Human oversight",
        3: "Full autonomy"
    }
    
    # Format risk factors as bullet list
    risk_factors_text = "\n".join([f"- {factor}" for factor in analysis.key_risk_factors])
    
    # Format recommended safeguards as bullet list
    safeguards_text = "\n".join([f"- {safeguard}" for safeguard in analysis.recommended_safeguards])
    
    return f"""### 🤖 AI Governance Analysis

**Risk Assessment:** {analysis.estimated_risk_tier} Risk

**Reasoning:**
{analysis.reasoning}

---

**Key Risk Factors Identified:**
{risk_factors_text}

**Recommended Safeguards:**
{safeguards_text}

**Framework Alignment:**
{analysis.framework_alignment}

---

**Form Auto-Fill Values:**
- PII/Sensitive Data: {"Yes" if analysis.contains_pii else "No"}
- Customer-Facing: {"Yes" if analysis.customer_facing else "No"}
- High-Stakes: {"Yes" if analysis.high_stakes else "No"}
- Autonomy Level: {analysis.autonomy_level} ({autonomy_labels.get(analysis.autonomy_level, "Unknown")})
- Sector: {analysis.sector}
- Modifiers: {", ".join(analysis.modifiers) if analysis.modifiers else "None"}

*Review the AI's analysis above, then scroll down to the form. The suggested values will auto-fill, but you can override any of them.*
"""

