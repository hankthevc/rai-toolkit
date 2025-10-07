"""Streamlit UI for the Frontier AI Risk Assessment Framework."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    # Streamlit executes the script from its own working directory. We append the
    # repository root so the shared ``common`` package resolves without installs.
    sys.path.append(str(REPO_ROOT))

from common.utils.exporters import build_decision_record
from common.utils.policy_loader import (
    ScenarioContext,
    load_policy_packs,
    select_applicable_controls,
)
from common.utils.risk_engine import RiskInputs, calculate_risk_score

_POLICY_PACKS_DIR = REPO_ROOT / "common" / "policy_packs"


@st.cache_data(show_spinner=False)
def _load_packs():
    """Load policy packs once per session to keep the UI responsive."""

    return load_policy_packs(_POLICY_PACKS_DIR)


def _build_scenario_context(inputs: RiskInputs, tier: str) -> ScenarioContext:
    """Translate form inputs into the structure used by the selector."""

    return ScenarioContext(
        tier=tier,
        contains_pii=inputs.contains_pii,
        customer_facing=inputs.customer_facing,
        high_stakes=inputs.high_stakes,
        autonomy_level=inputs.autonomy_level,
        sector=inputs.sector,
        modifiers=list(inputs.modifiers),
    )


def main():
    st.set_page_config(
        page_title="Frontier AI Risk Assessment Framework",
        page_icon="🛡️",
        layout="wide",
    )

    st.title("Frontier AI Risk Assessment Framework")
    st.caption(
        "Governance-as-code prototype. Defensive use only; validate with legal, privacy, and security partners."
    )

    packs = _load_packs()

    with st.form(key="risk_form"):
        st.subheader("Scenario Inputs")
        use_case = st.text_area(
            "Describe the AI use case",
            help="Summarize the scenario so the approval record captures context.",
        )
        contains_pii = st.checkbox("Processes personal or sensitive data (PII)")
        customer_facing = st.checkbox("Customer-facing or external exposure")
        high_stakes = st.checkbox("High-stakes outcomes (safety, rights, finances)")
        
        st.markdown("**Autonomy Level**")
        autonomy_level = st.slider(
            "Select autonomy level",
            min_value=0,
            max_value=3,
            value=0,
            help="How much automated decision-making without human review?",
        )
        
        with st.expander("ℹ️ What do autonomy levels mean?"):
            st.markdown("""
            - **Level 0 (Suggestion only):** AI provides recommendations but humans make all final decisions
              - Example: Code completion tool, writing assistant
            - **Level 1 (Human-in-the-loop):** AI acts but humans review and approve before impact
              - Example: Resume screening with recruiter review, content moderation queue
            - **Level 2 (Human oversight):** AI acts autonomously but humans can intervene with defined escalation rules
              - Example: Chatbot that escalates complex questions, fraud detection with manual review threshold
            - **Level 3 (Full autonomy):** AI makes and executes decisions without human review in normal operation
              - Example: Automated trading system, autonomous vehicle, real-time content filtering
            """)
        sector = st.selectbox(
            "Primary sector",
            options=[
                "General",
                "Healthcare",
                "Finance",
                "Critical Infrastructure",
                "Children",
            ],
        )
        modifiers = st.multiselect(
            "Scenario modifiers",
            options=["Bio", "Cyber", "Disinformation", "Children"],
            help="Flag additional sensitivities that should raise safeguards.",
        )

        st.subheader("Approval Routing")
        owner = st.text_input("Scenario Owner", help="Person accountable for the assessment inputs.")
        approver = st.text_input("Approver", help="Leader confirming the safeguards before launch.")

        submitted = st.form_submit_button("Assess Scenario", use_container_width=True)

    if not submitted:
        st.info("Complete the form and select **Assess Scenario** to generate a decision record.")
        st.markdown("---")
        _render_about_section()
        return

    risk_inputs = RiskInputs(
        contains_pii=contains_pii,
        customer_facing=customer_facing,
        high_stakes=high_stakes,
        autonomy_level=autonomy_level,
        sector=sector,
        modifiers=list(modifiers),
    )
    assessment = calculate_risk_score(risk_inputs)
    scenario_context = _build_scenario_context(risk_inputs, assessment.tier)

    controls = select_applicable_controls(packs, scenario_context)

    st.success(
        f"Risk tier: **{assessment.tier}** (score {assessment.score})",
        icon="📊",
    )
    if assessment.contributing_factors:
        st.write("**Drivers:** " + ", ".join(assessment.contributing_factors))
    else:
        st.write("**Drivers:** No material risk drivers captured.")

    # Safeguards surface authority + clause so reviewers can trace each recommendation.
    st.subheader("Required Safeguards")
    if controls:
        for control in controls:
            with st.expander(f"{control.title} — {control.authority}", expanded=False):
                st.markdown(
                    "\n".join(
                        [
                            f"**ID:** {control.id}",
                            f"**Clause:** {control.clause}",
                            f"**Description:** {control.description}",
                            f"**Evidence:** {control.evidence}",
                            f"**Tags:** {', '.join(control.tags) if control.tags else 'None'}",
                        ]
                    )
                )
                if control.mappings:
                    mapping_lines: List[str] = []
                    for key, values in control.mappings.items():
                        mapping_lines.append(f"{key}: {', '.join(values)}")
                    st.markdown(f"**Mappings:** {', '.join(mapping_lines)}")
    else:
        st.warning(
            "No safeguards matched the scenario inputs. Review policy coverage before approving.",
            icon="⚠️",
        )

    record = build_decision_record(
        scenario=scenario_context,
        assessment=assessment,
        controls=controls,
        owner=owner,
        approver=approver,
    )

    st.download_button(
        label="Download Decision Record (.md)",
        data=record,
        file_name="frontier_ai_decision_record.md",
        mime="text/markdown",
        use_container_width=True,
    )

    if use_case:
        st.markdown("---")
        st.subheader("Scenario Narrative")
        st.write(use_case)

    st.markdown("---")
    _render_about_section()


def _render_about_section():
    """Provide concise framing for recruiters and reviewers."""

    st.caption(
        "This prototype demonstrates governance-as-code patterns. It is illustrative, non-binding, and intended for defensive risk assessments."
    )
    st.caption(
        "Policy citations reference public frameworks (NIST AI RMF, EU AI Act, ISO/IEC 42001, OWASP LLM Top 10, MITRE ATLAS, US OMB). Validate clauses with counsel before deployment."
    )


if __name__ == "__main__":
    main()
