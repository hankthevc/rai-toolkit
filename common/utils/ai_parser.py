"""AI-powered scenario parsing to autofill risk assessment forms.

This module uses OpenAI's API to analyze plain-language use case descriptions
and suggest risk modifier values, demonstrating governance-as-code meets LLM capabilities.
"""

from __future__ import annotations

import os
from typing import Optional

from pydantic import BaseModel, Field

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class ScenarioAnalysis(BaseModel):
    """Structured output from AI scenario parsing."""

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
    reasoning: str = Field(
        description="Brief explanation of the analysis for transparency"
    )
    estimated_risk_tier: str = Field(
        description="AI's estimated risk tier: Low, Medium, High, or Critical"
    )
    key_risk_factors: list[str] = Field(
        description="3-5 specific risk factors identified in this scenario"
    )
    recommended_safeguards: list[str] = Field(
        description="5-7 specific governance controls that should apply (based on NIST AI RMF, EU AI Act, OWASP, etc.)"
    )
    framework_alignment: str = Field(
        description="Which governance frameworks are most relevant (e.g., 'EU AI Act High-Risk', 'NIST AI RMF Govern functions', 'OWASP LLM risks')"
    )


SYSTEM_PROMPT = """You are an AI governance analyst helping assess AI system risks against established frameworks (NIST AI RMF, EU AI Act, ISO 42001, OWASP LLM Top 10, MITRE ATLAS, US OMB AI Policy).

Given a plain-language description of an AI use case, analyze it comprehensively and provide risk assessment values plus governance recommendations.

**Field Definitions:**

1. **contains_pii**: True if the system processes personal/sensitive data (PII, PHI, financial records, location data, etc.)

2. **customer_facing**: True if external users/customers directly interact with the AI system

3. **high_stakes**: True if outcomes significantly impact safety, rights, or finances
   - Safety: physical harm, medical decisions, critical infrastructure
   - Rights: employment, credit, legal proceedings, civil liberties
   - Finances: significant monetary impact, fraud prevention, trading

4. **autonomy_level** (0-3):
   - 0 (Suggestion only): AI provides recommendations, humans make all decisions (code completion, writing assistant)
   - 1 (Human-in-loop): AI acts but humans review/approve before impact (resume screening with review, content moderation queue)
   - 2 (Human oversight): AI acts autonomously with defined escalation rules (chatbot with escalation, fraud detection with thresholds)
   - 3 (Full autonomy): AI makes and executes decisions without routine human review (automated trading, autonomous vehicles, real-time content filtering)

5. **sector**: Choose most relevant: General, Healthcare, Finance, Critical Infrastructure, Children

6. **modifiers**: Select applicable flags from: Bio, Cyber, Disinformation, Children
   - Bio: biological/health applications, pandemic response, biosecurity
   - Cyber: cybersecurity operations, threat detection, vulnerability assessment
   - Disinformation: content moderation, election integrity, synthetic media detection
   - Children: systems primarily used by or affecting minors

7. **reasoning**: 2-3 sentences explaining your risk analysis

8. **estimated_risk_tier**: Your assessment: Low, Medium, High, or Critical
   - Low (0-2 points): Internal tools, suggestion-only, no PII, human review
   - Medium (3-5 points): Some PII or customer-facing, human oversight present
   - High (6-8 points): Sensitive data + customer-facing, or automated decisions affecting rights/finances
   - Critical (9+ points): High-stakes autonomous decisions, healthcare/finance with PII, children's safety

9. **key_risk_factors**: List 3-5 specific risks (e.g., "Automated medical decisions without physician review", "Processes PHI for vulnerable patients", "Model outputs could influence treatment plans")

10. **recommended_safeguards**: List 5-7 specific controls that should apply, citing frameworks:
    - Examples: "Human oversight for all prescription changes (NIST AI RMF GOVERN-1.2)", "Adversarial testing for prompt injection (OWASP LLM01)", "HIPAA compliance controls for PHI (EU AI Act Art. 10)", "Explainability for medical recommendations (ISO 42001)"

11. **framework_alignment**: Identify which governance frameworks are most relevant and why
    - EU AI Act: Mention if High-Risk (Annex III: healthcare, employment, critical infrastructure, children)
    - NIST AI RMF: Note which functions apply (GOVERN, MAP, MEASURE, MANAGE)
    - OWASP LLM Top 10: Flag relevant vulnerabilities (prompt injection, data leakage, etc.)
    - MITRE ATLAS: Note adversarial threats if applicable

Be conservative in risk assessment—when uncertain, err toward higher risk classification. Your analysis will be shown to users alongside the traditional scoring model."""


def parse_scenario_with_ai(
    use_case_description: str,
    api_key: Optional[str] = None,
    model: str = "gpt-4o-mini",
) -> Optional[ScenarioAnalysis]:
    """Parse a plain-language AI scenario and suggest risk assessment values.

    Args:
        use_case_description: Plain-language description of the AI use case
        api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        model: OpenAI model to use (gpt-4o-mini for cost efficiency, gpt-4o for accuracy)

    Returns:
        ScenarioAnalysis with suggested values, or None if parsing fails

    Example:
        >>> analysis = parse_scenario_with_ai(
        ...     "A chatbot that helps hospital patients schedule appointments and refill prescriptions"
        ... )
        >>> if analysis:
        ...     print(f"PII: {analysis.contains_pii}, Sector: {analysis.sector}")
    """
    if OpenAI is None:
        raise ImportError(
            "openai package not installed. Run: pip install openai"
        )

    if not use_case_description or not use_case_description.strip():
        return None

    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key required. Set OPENAI_API_KEY environment variable "
            "or pass api_key parameter."
        )

    try:
        client = OpenAI(api_key=api_key)
        
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Analyze this AI use case and suggest risk assessment values:\n\n{use_case_description}"
                }
            ],
            response_format=ScenarioAnalysis,
            temperature=0.3,  # Lower temperature for more consistent risk assessment
        )

        return completion.choices[0].message.parsed

    except Exception as e:
        # Log the error but don't crash the app
        print(f"AI parsing failed: {e}")
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

