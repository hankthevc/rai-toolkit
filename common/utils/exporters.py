"""Helpers for exporting decision records to markdown."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Sequence

from jinja2 import Environment, StrictUndefined

from .policy_loader import PolicyControl, ScenarioContext
from .risk_engine import RiskAssessment

# Jinja template keeps formatting consistent across UI and CLI flows.
_DECISION_TEMPLATE = """
# Frontier AI Risk Decision Record

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
) -> str:
    """Render a Markdown decision record for the given inputs."""

    next_review = date.today() + timedelta(days=review_interval_days)
    return _template.render(
        scenario=scenario,
        assessment=assessment,
        controls=controls,
        owner=owner or "Unassigned",
        approver=approver or "Pending",
        assessment_date=date.today().isoformat(),
        next_review_date=next_review.isoformat(),
    )
