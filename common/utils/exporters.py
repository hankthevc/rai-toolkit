"""Helpers for exporting decision records to markdown."""

from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone
from typing import Sequence

from jinja2 import Environment, StrictUndefined

from .policy_loader import PolicyControl, ScenarioContext
from .risk_engine import RiskAssessment, RiskInputs, check_stop_ship_triggers

# Jinja template keeps formatting consistent across UI and CLI flows.
_DECISION_TEMPLATE = """
# Frontier AI Risk Decision Record

## Metadata
- **Generated:** {{ generated_timestamp }}
- **App Commit:** {{ app_commit }}
- **Model:** {{ model_name }} (temperature={{ model_temperature }})

---

**Scenario Owner:** {{ owner }}  \
**Approver:** {{ approver }}  \
**Assessment Date:** {{ assessment_date }}  \
**Next Review Due:** {{ next_review_date }}

## Summary
- **Risk Tier:** {{ assessment.tier }}
- **Risk Score:** {{ assessment.score }}
- **Key Drivers:** {% if assessment.contributing_factors %}{{ assessment.contributing_factors | join(", ") }}{% else %}None captured{% endif %}

## Scenario Inputs
- Contains PII: {{ "Yes" if scenario.contains_pii else "No" }}
- Customer Facing: {{ "Yes" if scenario.customer_facing else "No" }}
- High Stakes: {{ "Yes" if scenario.high_stakes else "No" }}
- Autonomy Level: {{ scenario.autonomy_level }}
- Sector: {{ scenario.sector }}
- Modifiers: {% if scenario.modifiers %}{{ scenario.modifiers | join(", ") }}{% else %}None{% endif %}

## Stop-Ship Triggers Encountered
{% if stop_ship_triggers %}
**⚠️ The following deployment gates must be satisfied before launch:**

{% for trigger in stop_ship_triggers %}
{{ loop.index }}. {{ trigger }}
{% endfor %}

These are hard gates per governance methodology. Deployment is blocked until all requirements are verified and documented.
{% else %}
None
{% endif %}

## Assumptions & Unknowns
{% if unknowns %}
The following areas could not be fully assessed due to insufficient information:

{% for unknown in unknowns %}
- {{ unknown }}
{% endfor %}

If additional details are available, re-run the assessment for a more comprehensive evaluation.
{% else %}
None identified
{% endif %}

## Required Safeguards
{% if controls %}
{% for control in controls %}
### {{ control.title }} ({{ control.authority }})
- **ID:** {{ control.id }}
- **Clause:** {{ control.clause }}
- **Description:** {{ control.description }}
- **Evidence to Capture:** {{ control.evidence }}
- **Tags:** {{ control.tags | join(", ") }}
{% if control.mappings %}- **Mappings:** {% for key, values in control.mappings.items() %}{{ key }}: {{ values | join(", ") }}{% if not loop.last %}; {% endif %}{% endfor %}
{% endif %}
{% endfor %}
{% else %}
No controls matched the scenario inputs. Review policy packs for coverage gaps.
{% endif %}

---
*Illustrative governance-as-code export. Validate safeguards with legal, compliance, and security teams before implementation.*
"""

_env = Environment(undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
_template = _env.from_string(_DECISION_TEMPLATE)


def build_decision_record(
    scenario: ScenarioContext,
    assessment: RiskAssessment,
    controls: Sequence[PolicyControl],
    owner: str,
    approver: str,
    review_interval_days: int = 90,
    risk_inputs: RiskInputs | None = None,
    model_name: str = "unknown",
    model_temperature: float = 0.0,
    unknowns: list[str] | None = None,
) -> str:
    """Render a Markdown decision record for the given inputs."""

    next_review = date.today() + timedelta(days=review_interval_days)
    
    # Check stop-ship triggers if risk_inputs provided
    stop_ship_triggers = []
    if risk_inputs:
        stop_ship_triggers = check_stop_ship_triggers(risk_inputs, assessment)
    
    # Get metadata
    generated_timestamp = datetime.now(timezone.utc).isoformat()
    app_commit = os.getenv("RAI_TOOLKIT_COMMIT_SHA", "unknown")
    
    return _template.render(
        scenario=scenario,
        assessment=assessment,
        controls=controls,
        owner=owner or "Unassigned",
        approver=approver or "Pending",
        assessment_date=date.today().isoformat(),
        next_review_date=next_review.isoformat(),
        stop_ship_triggers=stop_ship_triggers,
        unknowns=unknowns or [],
        generated_timestamp=generated_timestamp,
        app_commit=app_commit,
        model_name=model_name,
        model_temperature=model_temperature,
    )
