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


SYSTEM_PROMPT = """You are an AI governance analyst helping assess AI system risks.

Given a plain-language description of an AI use case, analyze it and suggest risk assessment values.

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

7. **reasoning**: 2-3 sentences explaining your analysis

Be conservative in risk assessment—when uncertain, err toward higher risk classification."""


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
    
    return f"""**AI Analysis Summary**

{analysis.reasoning}

**Suggested Values:**
- PII/Sensitive Data: {"Yes" if analysis.contains_pii else "No"}
- Customer-Facing: {"Yes" if analysis.customer_facing else "No"}
- High-Stakes: {"Yes" if analysis.high_stakes else "No"}
- Autonomy Level: {analysis.autonomy_level} ({autonomy_labels.get(analysis.autonomy_level, "Unknown")})
- Sector: {analysis.sector}
- Modifiers: {", ".join(analysis.modifiers) if analysis.modifiers else "None"}
"""

