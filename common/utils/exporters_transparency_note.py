"""Transparency Note stub generation (illustrative template).

This module generates a structured Transparency Note template that teams can
complete for stakeholder communication. This is an illustrative example for
demonstration purposes only.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone

from common.utils.risk_engine import RiskAssessment
from common.utils.policy_loader import ScenarioContext, PolicyControl


def build_transparency_note(
    scenario: ScenarioContext,
    assessment: RiskAssessment,
    controls: list[PolicyControl],
    model_name: str = "unknown",
    model_temperature: float = 0.0,
) -> str:
    """
    Generate a Transparency Note stub for stakeholder communication.
    
    Args:
        scenario: The assessed scenario context
        assessment: Risk assessment results
        controls: List of applicable policy controls
        model_name: Model used for AI analysis
        model_temperature: Temperature parameter used
        
    Returns:
        Markdown-formatted Transparency Note stub
    """
    
    # Get metadata
    generated_timestamp = datetime.now(timezone.utc).isoformat()
    app_commit = os.getenv("RAI_TOOLKIT_COMMIT_SHA", "unknown")
    
    # Determine appropriate use limitations based on risk factors
    limitations = []
    if scenario.contains_pii:
        limitations.append("- Processes personal data; requires data minimization and access controls")
    if scenario.high_stakes:
        limitations.append("- High-stakes outcomes; human review required for consequential decisions")
    if scenario.autonomy_level >= 2:
        limitations.append("- Automated decision-making; monitoring and escalation procedures required")
    if hasattr(scenario, 'generates_synthetic_content') and scenario.generates_synthetic_content:
        limitations.append("- Generates synthetic content; disclosure to end users required")
    if hasattr(scenario, 'explainability_level') and scenario.explainability_level == "Black Box":
        limitations.append("- Limited explainability; may not be suitable for rights-impacting decisions")
    
    # Extract relevant safeguards for transparency
    key_safeguards = []
    for control in controls[:7]:  # Top 7 safeguards
        key_safeguards.append(f"- **{control.title}** ({control.authority} {control.clause})")
    
    # Build the note
    note = f"""# Transparency Note

## Metadata
- **Generated:** {generated_timestamp}
- **App Commit:** {app_commit}
- **Model:** {model_name} (temperature={model_temperature})

---

**System Name:** [TO BE COMPLETED]

**Version:** [TO BE COMPLETED]

**Last Updated:** [TO BE COMPLETED]

**Contact:** [TO BE COMPLETED]

---

## What is this system?

**Purpose:**  
[COMPLETE: Describe the intended purpose and primary use case]

**Context:**  
This system operates in the **{scenario.sector}** sector and is assessed as **{assessment.tier} risk** (score: {assessment.score}/42).

---

## What can this system do?

**Capabilities:**  
[COMPLETE: List the system's key capabilities and functions]

**Example Use Cases:**  
[COMPLETE: Provide 2-3 specific examples of how the system is used]

---

## What are this system's intended uses?

**Intended Users:**  
{"External users (customers, general public)" if scenario.customer_facing else "Internal users (employees, authorized personnel)"}

**Intended Scenarios:**  
[COMPLETE: Describe the scenarios where this system should be used]

**Autonomy Level:** {_get_autonomy_description(scenario.autonomy_level)}

---

## What are this system's limitations?

**Known Limitations:**
{chr(10).join(limitations) if limitations else "[COMPLETE: Describe technical limitations, edge cases, or scenarios where the system may not perform well]"}

**Out of Scope:**  
[COMPLETE: Explicitly state what this system should NOT be used for]

**Human Oversight Requirements:**  
{"Human review required for all decisions affecting users" if scenario.high_stakes else "Human oversight recommended for edge cases"}

---

## How was this system evaluated?

**Testing & Validation:**  
[COMPLETE: Describe testing methodology, validation datasets, and evaluation metrics]

**Identified Risk Factors:**  
{_format_risk_factors(assessment.contributing_factors)}

**Governance Standards Applied:**  
{_format_standards(controls)}

---

## What are the governance safeguards?

This system is subject to the following governance controls:

{chr(10).join(key_safeguards) if key_safeguards else "No specific safeguards triggered for this risk profile."}

**Full control documentation:** See Decision Record for complete list of {len(controls)} triggered safeguards.

---

## What data does this system use?

**Data Processing:**  
{"✅ Processes personal or sensitive data (PII/PHI)" if scenario.contains_pii else "❌ Does not process personal or sensitive data"}

**Data Sources:**  
[COMPLETE: Describe training data sources, user input data, and any third-party data]

**Data Storage & Retention:**  
[COMPLETE: Describe where data is stored, how long it's retained, and deletion policies]

**Cross-Border Transfers:**  
{"⚠️ May involve cross-border data transfers; GDPR adequacy requirements apply" if hasattr(scenario, 'international_data') and scenario.international_data else "Data processing within single jurisdiction"}

---

## How do users control their data?

**User Rights:**  
[COMPLETE: Describe how users can access, correct, delete, or export their data]

**Opt-Out Mechanisms:**  
[COMPLETE: Describe how users can opt out of data collection or automated decisions]

**Contact for Data Requests:**  
[TO BE COMPLETED]

---

## What happens if the system makes a mistake?

**Error Handling:**  
[COMPLETE: Describe error detection, logging, and alerting mechanisms]

**Remediation Process:**  
[COMPLETE: Describe how errors are corrected and users are notified]

**Decision Reversibility:**  
{_get_reversibility_note(scenario)}

**Appeal/Review Process:**  
{"Human review available upon request" if scenario.high_stakes else "[COMPLETE: Describe appeal process if applicable]"}

---

## How is this system monitored?

**Performance Monitoring:**  
[COMPLETE: Describe metrics, dashboards, and alerting thresholds]

**Fairness Monitoring:**  
{"Required for this system given high-stakes outcomes and/or protected populations" if scenario.high_stakes or (hasattr(scenario, 'protected_populations') and scenario.protected_populations) else "[COMPLETE: Describe fairness metrics if applicable]"}

**Incident Response:**  
[COMPLETE: Describe incident escalation and response procedures]

---

## Who is responsible for this system?

**System Owner:**  
[TO BE COMPLETED - Name, role, contact]

**Governance Approval:**  
[TO BE COMPLETED - Approver name, date]

**Legal/Compliance Sign-Off:**  
{"Required for {assessment.tier} risk tier systems" if assessment.tier in ["High", "Critical"] else "[TO BE COMPLETED if applicable]"}

**Last Review Date:**  
[TO BE COMPLETED]

**Next Review Date:**  
[TO BE COMPLETED - Recommend annual for High/Critical tier]

---

## Additional Resources

**Documentation:**  
[COMPLETE: Links to technical documentation, API docs, user guides]

**Support:**  
[COMPLETE: How to get help, report issues, or request features]

**Feedback:**  
[COMPLETE: How users can provide feedback or report concerns]

---

*This Transparency Note was generated using the RAI Toolkit (https://github.com/hankthevc/rai-toolkit) and should be completed by the system owner with accurate, system-specific details. Illustrative, for demo purposes; not official guidance.*
"""
    
    return note


def _get_autonomy_description(level: int) -> str:
    """Get plain-language autonomy description."""
    descriptions = {
        0: "Suggestion only - AI provides recommendations but humans make all final decisions",
        1: "Human-in-the-loop - AI acts but humans review and approve before impact",
        2: "Human oversight - AI acts autonomously but humans can intervene with defined escalation",
        3: "Full autonomy - AI makes and executes decisions without human review in normal operation"
    }
    return descriptions.get(level, "Unknown autonomy level")


def _get_reversibility_note(scenario: ScenarioContext) -> str:
    """Get decision reversibility note."""
    if hasattr(scenario, 'decision_reversible'):
        reversibility_map = {
            "Fully Reversible": "Decisions can be undone without cost or impact",
            "Reversible with Cost": "Decisions can be reversed but may incur costs or delays",
            "Difficult to Reverse": "Reversal is challenging and may not fully restore original state",
            "Irreversible": "⚠️ Decisions cannot be reversed - enhanced safeguards required"
        }
        return reversibility_map.get(scenario.decision_reversible, "[COMPLETE: Describe decision reversibility]")
    return "[COMPLETE: Describe whether and how decisions can be reversed]"


def _format_risk_factors(factors: list[str]) -> str:
    """Format risk factors as bullet list."""
    if not factors:
        return "No significant risk factors identified"
    return "\n".join([f"- {factor}" for factor in factors])


def _format_standards(controls: list[PolicyControl]) -> str:
    """Extract unique governance standards from controls."""
    if not controls:
        return "No specific standards triggered"
    
    authorities = sorted(set(control.authority for control in controls))
    return ", ".join(authorities)

