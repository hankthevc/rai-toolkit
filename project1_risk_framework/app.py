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

from common.utils.ai_parser import (
    format_analysis_summary,
    parse_scenario_with_ai,
)
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

    # Initialize session state for AI-parsed values
    if "ai_analysis" not in st.session_state:
        st.session_state.ai_analysis = None
    if "show_ai_preview" not in st.session_state:
        st.session_state.show_ai_preview = False

    # AI Analysis section (outside form for interactivity)
    st.subheader("🤖 AI-Powered Analysis (Experimental)")
    st.caption("Meta-governance: This tool was vibecoded with AI—now it uses AI to help *you* assess AI systems.")
    
    # Quick reference always visible
    st.info("""
    **📋 Quick Guide:** Describe what your AI does, who uses it, what data it processes, how automated it is, and what happens if it fails. 
    See detailed examples below. ⬇️
    """)
    
    # Show prompt tips prominently
    with st.expander("💡 How to Write a Good Prompt — Full Examples & Tips", expanded=False):
        st.markdown("""
        **Include these 6 elements for best AI analysis:**
        
        1. **What the AI does** — Core functionality and decision-making role
        2. **Who uses it** — Internal employees, customers, vulnerable populations, general public
        3. **What data it processes** — Personal info, health records, financial data, behavioral data
        4. **Level of automation** — Does it suggest, assist, decide with oversight, or act autonomously?
        5. **Impact domain** — What happens if it makes a mistake? (safety, rights, finances, privacy)
        6. **Context flags** — Healthcare, finance, children, cybersecurity, bio/life sciences, disinformation
        
        ---
        
        ### ✅ Example: Healthcare Chatbot (Critical Risk)
        
        *"A chatbot that helps hospital patients schedule appointments and refill prescriptions. It accesses their medical records to check medication history and insurance eligibility. Patients interact directly via web and mobile app. The system suggests appointment times but requires nurse approval for prescription refills."*
        
        **Why it's good:** Clear functionality (scheduling/prescriptions), users (patients), data (medical records), automation (suggests with nurse approval), impact (healthcare decisions), context (healthcare).
        
        ---
        
        ### ✅ Example: Code Copilot (Low Risk)
        
        *"An internal code completion tool for our engineering team. It suggests code snippets based on our proprietary codebase. Engineers review all suggestions before committing. Only used by employees with existing code access. No customer data involved."*
        
        **Why it's good:** Clear functionality (code suggestions), users (internal engineers), data (code, no customer data), automation (suggestion only), impact (low - human review), context (internal tooling).
        
        ---
        
        ### ✅ Example: Trading System (Critical Risk)
        
        *"An automated trading system that buys and sells securities based on market signals. It executes trades autonomously up to $50K per trade without human review. Larger trades escalate to compliance. Processes real-time market data and client portfolio information."*
        
        **Why it's good:** Clear functionality (automated trading), users (implicit: clients), data (portfolio + market data), automation (autonomous up to threshold), impact (financial), context (finance).
        
        ---
        
        ### ❌ Too Vague Examples
        
        - **"A chatbot for customers"** → Missing: What does it do? What data? What decisions? What stakes?
        - **"AI for hiring"** → Missing: Resume screening? Interview scheduling? Autonomous rejection? What data does it see?
        - **"Machine learning model"** → Missing: Everything! What's the use case?
        
        ---
        
        **The AI will analyze your description and suggest risk modifiers. You'll review its reasoning before accepting.**
        """)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        quick_description = st.text_area(
            "📝 Describe your AI use case (see tips above for what to include)",
            placeholder="Example: 'A chatbot that helps hospital patients schedule appointments and refill prescriptions. It accesses medical records, interacts directly with patients via web/mobile, and requires nurse approval for prescription changes.'",
            height=140,
            key="quick_desc",
            help="Include: what it does, who uses it, what data it processes, automation level, impact if it fails, and relevant context (healthcare/finance/children/etc.)"
        )
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        api_key_input = st.text_input(
            "OpenAI API Key (optional)",
            type="password",
            help="Leave blank to use OPENAI_API_KEY environment variable",
            key="api_key_input"
        )
        analyze_button = st.button("🔍 Analyze with AI", use_container_width=True, type="primary")

    # Handle AI analysis
    if analyze_button and quick_description:
        with st.spinner("Analyzing scenario with AI..."):
            try:
                import os
                api_key = api_key_input or os.getenv("OPENAI_API_KEY")
                if not api_key:
                    st.error("⚠️ OpenAI API key required. Set OPENAI_API_KEY environment variable or enter above.")
                else:
                    analysis = parse_scenario_with_ai(quick_description, api_key=api_key)
                    if analysis:
                        st.session_state.ai_analysis = analysis
                        st.session_state.show_ai_preview = True
                        st.success("✅ Analysis complete! Review suggestions below, then use them to fill the form.")
                    else:
                        st.error("Analysis failed. Check your API key and description.")
            except ImportError:
                st.error("⚠️ OpenAI package not installed. Run: `pip install openai`")
            except Exception as e:
                st.error(f"Analysis error: {e}")

    # Display AI analysis preview
    if st.session_state.show_ai_preview and st.session_state.ai_analysis:
        st.info(format_analysis_summary(st.session_state.ai_analysis))
        if st.button("👍 Use These Values", use_container_width=True):
            st.info("✅ Scroll down and use the suggested values in the form below!")

    st.markdown("---")

    # Main risk assessment form
    with st.form(key="risk_form"):
        st.subheader("Scenario Inputs")
        
        # Get suggested values from AI analysis if available
        suggested = st.session_state.ai_analysis if st.session_state.ai_analysis else None
        
        use_case = st.text_area(
            "Describe the AI use case",
            value=quick_description if quick_description else "",
            help="Summarize the scenario so the approval record captures context.",
        )
        contains_pii = st.checkbox(
            "Processes personal or sensitive data (PII)",
            value=suggested.contains_pii if suggested else False,
            help="✨ AI-suggested" if suggested else None
        )
        customer_facing = st.checkbox(
            "Customer-facing or external exposure",
            value=suggested.customer_facing if suggested else False,
            help="✨ AI-suggested" if suggested else None
        )
        high_stakes = st.checkbox(
            "High-stakes outcomes (safety, rights, finances)",
            value=suggested.high_stakes if suggested else False,
            help="✨ AI-suggested" if suggested else None
        )
        
        st.markdown("**Autonomy Level**")
        autonomy_level = st.slider(
            "Select autonomy level" + (" (✨ AI-suggested)" if suggested else ""),
            min_value=0,
            max_value=3,
            value=suggested.autonomy_level if suggested else 0,
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
        
        sector_options = ["General", "Healthcare", "Finance", "Critical Infrastructure", "Children"]
        sector_index = sector_options.index(suggested.sector) if suggested and suggested.sector in sector_options else 0
        
        sector = st.selectbox(
            "Primary sector" + (" (✨ AI-suggested)" if suggested else ""),
            options=sector_options,
            index=sector_index,
        )
        
        modifiers = st.multiselect(
            "Scenario modifiers" + (" (✨ AI-suggested)" if suggested else ""),
            options=["Bio", "Cyber", "Disinformation", "Children"],
            default=suggested.modifiers if suggested else [],
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
