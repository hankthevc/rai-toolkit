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
from common.utils.ai_interviewer import (
    conduct_interview,
    format_interview_questions,
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
        model_type=inputs.model_type,
        data_source=inputs.data_source,
        learns_in_production=inputs.learns_in_production,
        international_data=inputs.international_data,
        explainability_level=inputs.explainability_level,
        uses_foundation_model=inputs.uses_foundation_model,
        generates_synthetic_content=inputs.generates_synthetic_content,
        dual_use_risk=inputs.dual_use_risk,
        decision_reversible=inputs.decision_reversible,
        protected_populations=inputs.protected_populations,
    )


def _get_governance_answer(question: str, use_case: str, assessment, controls, ai_analysis, api_key: str) -> str:
    """Get context-aware governance answers using OpenAI."""
    try:
        from openai import OpenAI
    except ImportError:
        return "❌ OpenAI package not installed. This feature requires the openai package."
    
    # Build context from the assessment
    risk_factors_text = ", ".join(assessment.contributing_factors) if assessment.contributing_factors else "None"
    
    controls_text = ""
    if controls:
        for i, control in enumerate(controls[:5], 1):  # Top 5 safeguards
            controls_text += f"{i}. **{control.title}** ({control.authority} {control.clause}): {control.description}\n"
    else:
        controls_text = "No specific safeguards triggered for this risk profile."
    
    frameworks_text = ai_analysis.framework_alignment if hasattr(ai_analysis, 'framework_alignment') else "General AI governance frameworks"
    
    # Build comprehensive system prompt
    system_prompt = f"""You are an expert AI governance advisor helping teams understand their risk assessment results and implement safeguards.

**CURRENT ASSESSMENT CONTEXT:**

**Scenario:** {use_case}

**Risk Classification:**
- Tier: {assessment.tier}
- Score: {assessment.score} points
- Key Risk Factors: {risk_factors_text}

**Applicable Governance Frameworks:** {frameworks_text}

**Top Safeguards Required:**
{controls_text}

**AI Analysis Reasoning:** {ai_analysis.reasoning if hasattr(ai_analysis, 'reasoning') else 'Not available'}

---

**YOUR ROLE:**
You are a helpful governance advisor who:
- Explains WHY specific safeguards are required (citing regulations)
- Clarifies technical governance concepts in plain language
- Provides actionable implementation guidance
- Helps draft communications to legal/compliance/security teams
- References the SPECIFIC assessment details above in your answers

**GUIDELINES:**
1. **Be specific:** Always reference the actual scenario, risk tier, and safeguards from THIS assessment
2. **Be practical:** Provide concrete next steps, not just theory
3. **Cite sources:** Mention specific regulations (GDPR Art. 22, HIPAA 164.308, EU AI Act Art. 52, etc.)
4. **Be concise:** 2-3 paragraphs max unless asked for detailed explanation
5. **Caveat appropriately:** Remind users to validate with legal/compliance when making decisions

**EXAMPLE RESPONSE STYLES:**

For "Why" questions:
- Explain the specific risk factors that led to the tier/safeguard
- Connect to regulatory requirements
- Use this assessment's details

For "How" questions:
- Provide step-by-step implementation guidance
- Suggest tools/frameworks when relevant
- Include success criteria

For "Draft" requests:
- Use professional but clear language
- Include specific details from this scenario
- Provide structure (subject line, sections, next steps)

For framework questions:
- Explain the regulation in plain language
- Show how it applies to THIS scenario
- Provide compliance checklist

**IMPORTANT:** Always answer in the context of the current assessment shown above. Don't give generic governance advice - make it specific to this {assessment.tier} tier scenario with score {assessment.score}."""

    try:
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,  # Slightly higher for more conversational responses
            max_tokens=800,  # Allow detailed responses
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ Error getting response: {str(e)}\n\nPlease check your API key and try again."


def main():
    st.set_page_config(
        page_title="Frontier AI Risk Assessment Framework",
        page_icon="🛡️",
        layout="wide",
    )

    st.title("Frontier AI Risk Assessment Framework")
    
    # Framing panel
    with st.expander("ℹ️ About This Tool — Read This First", expanded=False):
        st.markdown("""
        ### What This Is
        A **small prototype** to demonstrate my reasoning approach to Responsible AI risk assessment:
        - How I **triage** AI systems based on impact and context
        - How I **score** risk using transparent, additive factors
        - How I **map** scenarios to governance standards (NIST AI RMF, EU AI Act, OWASP, etc.)
        - How I **produce** concise decision records for stakeholder review
        
        ### What This Is NOT
        - ❌ **Not production software** — Real teams should use internal frameworks, richer data, and secured pipelines
        - ❌ **Not comprehensive** — This is a demonstration, not an enterprise solution
        - ❌ **Not legal advice** — Always validate with legal, compliance, and security partners
        
        ### Assumptions & Limitations (Non-Exhaustive)
        - **Simplified scoring:** Weights are illustrative, not empirically validated
        - **Simulated data:** Policy packs are examples, not official regulatory text
        - **Placeholder mappings:** Framework citations are illustrative, not authoritative
        - **No sensitive data stored:** All processing is client-side; AI analysis sends data to OpenAI
        - **Export for demo only:** Decision records are templates, not binding approvals
        
        ### Goal
        Demonstrate **judgment under ambiguity**, not claim completeness. This shows:
        - Cross-functional thinking (policy → code → operations)
        - Structured decision-making under uncertainty
        - Ability to translate complex regulations into actionable controls
        
        Built by [Henry Appel](https://github.com/hankthevc) | Former NSC/ODNI policy advisor | AI security researcher at 2430 Group
        """)
    
    st.caption(
        "Governance-as-code prototype. Defensive use only; validate with legal, privacy, and security partners."
    )
    # Force redeploy marker: v1.0.2

    packs = _load_packs()
    
    # Sidebar: Data Handling & Privacy Information
    with st.sidebar:
        st.header("🔒 Data Handling")
        st.markdown("""
        **Your data privacy:**
        - ✅ **No data stored:** Assessments are not saved to any database
        - ✅ **Local processing:** Risk calculations run entirely in your browser session
        - ⚠️ **AI analysis:** If you use AI parsing, your scenario description is sent to OpenAI's API
        - 🔑 **API keys:** Stored only in browser session memory (not persisted)
        
        **What happens when you:**
        - **Fill the form:** Data stays in your browser
        - **Click "Analyze with AI":** Scenario text sent to OpenAI (subject to their terms)
        - **Submit assessment:** Risk score calculated locally
        - **Download record:** File generated client-side
        
        **Recommendations:**
        - Don't paste actual PII/PHI into scenario descriptions
        - Use anonymized examples instead
        - For production use, deploy locally or review vendor terms
        
        [Privacy Policy](https://streamlit.io/privacy-policy) | [Terms of Service](https://streamlit.io/terms-of-service)
        """)
        
        st.markdown("---")
        st.markdown("**📚 About This Tool**")
        st.markdown("""
        Built by [Henry Appel](https://github.com/hankthevc) to demonstrate governance-as-code patterns for AI risk assessment.
        
        [GitHub](https://github.com/hankthevc/rai-toolkit) | [Issues](https://github.com/hankthevc/rai-toolkit/issues)
        """)

    # Initialize session state for AI-parsed values
    if "ai_analysis" not in st.session_state:
        st.session_state.ai_analysis = None
    if "show_ai_preview" not in st.session_state:
        st.session_state.show_ai_preview = False
    if "governance_chat" not in st.session_state:
        st.session_state.governance_chat = []
    if "interview_mode" not in st.session_state:
        st.session_state.interview_mode = False
    if "interview_history" not in st.session_state:
        st.session_state.interview_history = []
    if "interview_questions" not in st.session_state:
        st.session_state.interview_questions = None

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
        
        col_a, col_b = st.columns(2)
        with col_a:
            interview_button = st.button("💬 Interview Mode (Recommended)", use_container_width=True, type="primary", 
                                        help="AI asks clarifying questions for comprehensive analysis")
        with col_b:
            analyze_button = st.button("⚡ Quick Analysis", use_container_width=True,
                                      help="One-shot analysis without follow-up questions")

    # Handle Interview Mode (NEW - preferred flow)
    if interview_button and quick_description:
        with st.spinner("Analyzing your description and preparing questions..."):
            try:
                import os
                # Get API key (same logic as analysis)
                api_key = None
                if api_key_input and api_key_input.strip():
                    api_key = api_key_input.strip()
                    st.info("Using API key from input field...")
                if not api_key:
                    try:
                        api_key = st.secrets.get("OPENAI_API_KEY")
                        if api_key:
                            st.info("Using API key from Streamlit Cloud secrets...")
                    except:
                        pass
                if not api_key:
                    api_key = os.getenv("OPENAI_API_KEY")
                    if api_key:
                        st.info("Using API key from environment variable...")
                
                if not api_key:
                    st.error("⚠️ OpenAI API key required for interview mode.")
                else:
                    # Conduct initial interview
                    interview_response = conduct_interview(
                        initial_description=quick_description,
                        conversation_history=st.session_state.interview_history,
                        api_key=api_key
                    )
                    
                    if interview_response:
                        if interview_response.ready_for_analysis:
                            # Enough context gathered, proceed to analysis
                            st.success("✅ Sufficient context gathered! Proceeding with comprehensive analysis...")
                            # Build enriched description from conversation
                            enriched_description = quick_description + "\n\n**Additional Context from Interview:**\n"
                            for turn in st.session_state.interview_history:
                                enriched_description += f"Q: {turn['question']}\nA: {turn['answer']}\n\n"
                            
                            analysis = parse_scenario_with_ai(enriched_description, api_key=api_key)
                            if analysis:
                                st.session_state.ai_analysis = analysis
                                st.session_state.show_ai_preview = True
                                st.session_state.interview_mode = False
                                st.session_state.interview_history = []  # Reset for next time
                        else:
                            # Need more info - show questions
                            st.session_state.interview_mode = True
                            st.session_state.interview_questions = interview_response
                            st.rerun()
            except ImportError:
                st.error("⚠️ OpenAI package not installed. Run: `pip install openai`")
            except Exception as e:
                st.error(f"❌ Interview error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
    
    # Display interview questions if in interview mode
    if st.session_state.interview_mode and st.session_state.interview_questions:
        st.markdown("---")
        st.subheader("🔍 Clarifying Questions for Comprehensive Assessment")
        
        response = st.session_state.interview_questions
        st.info(response.reasoning)
        
        st.markdown(f"**Please answer these {len(response.questions)} questions to ensure accurate risk assessment:**")
        
        # Create form for answers
        with st.form("interview_answers"):
            answers = []
            for i, q in enumerate(response.questions):
                st.markdown(f"**Question {i+1}:** {q.question}")
                st.caption(f"💡 Why this matters: {q.rationale} (*{q.framework_reference}*)")
                answer = st.text_area(
                    f"Your answer #{i+1}:",
                    key=f"interview_q_{i}",
                    height=80,
                    placeholder="Be specific - this affects the risk assessment..."
                )
                answers.append({"question": q.question, "answer": answer})
                st.markdown("---")
            
            submit_answers = st.form_submit_button("✅ Submit Answers & Continue", use_container_width=True)
        
        if submit_answers:
            # Check all answers provided
            if all(a["answer"].strip() for a in answers):
                # Add to history
                st.session_state.interview_history.extend(answers)
                
                # Get API key again
                import os
                api_key = None
                if api_key_input and api_key_input.strip():
                    api_key = api_key_input.strip()
                if not api_key:
                    try:
                        api_key = st.secrets.get("OPENAI_API_KEY")
                    except:
                        pass
                if not api_key:
                    api_key = os.getenv("OPENAI_API_KEY")
                
                # Continue interview or proceed to analysis
                with st.spinner("Processing your answers..."):
                    interview_response = conduct_interview(
                        initial_description=quick_description,
                        conversation_history=st.session_state.interview_history,
                        api_key=api_key
                    )
                    
                    if interview_response and interview_response.ready_for_analysis:
                        # Ready for final analysis
                        enriched_description = quick_description + "\n\n**Additional Context from Interview:**\n"
                        for turn in st.session_state.interview_history:
                            enriched_description += f"Q: {turn['question']}\nA: {turn['answer']}\n\n"
                        
                        analysis = parse_scenario_with_ai(enriched_description, api_key=api_key)
                        if analysis:
                            st.session_state.ai_analysis = analysis
                            st.session_state.show_ai_preview = True
                            st.session_state.interview_mode = False
                            st.session_state.interview_questions = None
                            st.success("✅ Comprehensive analysis complete based on interview!")
                            st.rerun()
                    else:
                        # More questions needed
                        st.session_state.interview_questions = interview_response
                        st.rerun()
            else:
                st.warning("⚠️ Please answer all questions to continue the assessment.")
    
    # Handle Quick Analysis (original one-shot flow)
    if analyze_button and quick_description:
        with st.spinner("Analyzing scenario with AI..."):
            try:
                import os
                # Check multiple sources for API key: input field, Streamlit secrets, env var
                # Priority: 1) User input field, 2) Streamlit secrets, 3) Environment variable
                api_key = None
                
                # Check user input field first (strip whitespace)
                if api_key_input and api_key_input.strip():
                    api_key = api_key_input.strip()
                    st.info("Using API key from input field...")
                
                # If no user input, check Streamlit secrets
                if not api_key:
                    try:
                        api_key = st.secrets.get("OPENAI_API_KEY")
                        if api_key:
                            st.info("Using API key from Streamlit Cloud secrets...")
                    except (KeyError, FileNotFoundError, AttributeError):
                        pass
                
                # If still no key, check environment variable
                if not api_key:
                    api_key = os.getenv("OPENAI_API_KEY")
                    if api_key:
                        st.info("Using API key from environment variable...")
                
                if not api_key:
                    st.error("⚠️ OpenAI API key required. Please either:\n- Enter it in the field above, OR\n- Set it in Streamlit Cloud Settings → Secrets as `OPENAI_API_KEY`")
                else:
                    analysis = parse_scenario_with_ai(quick_description, api_key=api_key)
                    if analysis:
                        st.session_state.ai_analysis = analysis
                        st.session_state.show_ai_preview = True
                        st.success("✅ Analysis complete! Review suggestions below, then use them to fill the form.")
                    else:
                        st.error("❌ Analysis failed. Please check your API key and try again.")
            except ImportError:
                st.error("⚠️ OpenAI package not installed. Run: `pip install openai`")
            except Exception as e:
                st.error(f"❌ Analysis error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    # Display AI analysis preview
    if st.session_state.show_ai_preview and st.session_state.ai_analysis:
        # Show AI's full analytical reasoning
        st.success("✅ AI Analysis Complete")
        
        analysis = st.session_state.ai_analysis
        
        # Defensive check for backward compatibility with old session state
        if not hasattr(analysis, 'estimated_risk_tier'):
            st.warning("⚠️ Analysis format outdated. Clearing cache and refreshing...")
            st.session_state.show_ai_preview = False
            st.session_state.ai_analysis = None
            st.info("Please click the 'Analyze with AI' button again to re-run the analysis with the updated format.")
            # Don't continue executing this section
        else:
            # Show AI's risk assessment prominently
            risk_tier_colors = {
                "Low": "🟢",
                "Medium": "🟡", 
                "High": "🟠",
                "Critical": "🔴"
            }
            risk_icon = risk_tier_colors.get(analysis.estimated_risk_tier, "⚪")
            
            st.markdown(f"### {risk_icon} AI Assessment: **{analysis.estimated_risk_tier} Risk**")
            
            # Show reasoning
            with st.expander("📋 AI's Reasoning & Analysis", expanded=True):
                st.markdown(f"**Why this risk tier:**\n\n{analysis.reasoning}")
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🎯 Key Risk Factors:**")
                    for factor in analysis.key_risk_factors:
                        st.markdown(f"- {factor}")
                
                with col2:
                    st.markdown("**📚 Framework Alignment:**")
                    st.markdown(analysis.framework_alignment)
            
            # Show recommended safeguards
            with st.expander("🛡️ AI-Recommended Safeguards", expanded=True):
                st.markdown("Based on the scenario analysis, these governance controls should apply:")
                for i, safeguard in enumerate(analysis.recommended_safeguards, 1):
                    st.markdown(f"{i}. {safeguard}")
                st.caption("*Note: The traditional risk engine below will also apply safeguards based on policy packs. Compare both sets of recommendations.*")
            
            # Show form values
            with st.expander("📝 Form Auto-Fill Values", expanded=False):
                autonomy_labels = {
                    0: "Suggestion only",
                    1: "Human-in-the-loop",
                    2: "Human oversight",
                    3: "Full autonomy"
                }
                st.markdown(f"""
                These values will auto-fill the form below:
                
                - **PII/Sensitive Data:** {"Yes" if analysis.contains_pii else "No"}
                - **Customer-Facing:** {"Yes" if analysis.customer_facing else "No"}
                - **High-Stakes:** {"Yes" if analysis.high_stakes else "No"}
                - **Autonomy Level:** {analysis.autonomy_level} ({autonomy_labels.get(analysis.autonomy_level, "Unknown")})
                - **Sector:** {analysis.sector}
                - **Modifiers:** {", ".join(analysis.modifiers) if analysis.modifiers else "None"}
                
                *Scroll down to review the form. You can override any suggested values.*
                """)
            
            st.info("⬇️ **Next Step:** Scroll down to review the form (values auto-filled) and submit for the traditional risk engine's assessment.")

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

        # New risk factors section
        with st.expander("🔬 Technical AI/ML Characteristics (Optional - Click to Expand)", expanded=False):
            st.caption("These factors help assess architecture-specific risks and threat models.")
            
            model_type_options = ["Traditional ML", "Generative AI / LLM", "Computer Vision", "Multimodal", "Reinforcement Learning"]
            model_type_index = model_type_options.index(suggested.model_type) if suggested and suggested.model_type in model_type_options else 0
            model_type = st.selectbox(
                "Model Architecture Type" + (" (✨ AI-suggested)" if suggested else ""),
                options=model_type_options,
                index=model_type_index,
                help="LLMs have OWASP LLM risks; Computer Vision has deepfake/adversarial risks; etc."
            )
            
            data_source_options = ["Proprietary/Internal", "Public Datasets", "Internet-Scraped", "User-Generated", "Third-Party/Vendor", "Synthetic"]
            data_source_index = data_source_options.index(suggested.data_source) if suggested and suggested.data_source in data_source_options else 0
            data_source = st.selectbox(
                "Training Data Source" + (" (✨ AI-suggested)" if suggested else ""),
                options=data_source_options,
                index=data_source_index,
                help="Internet-scraped = copyright/bias risks; User-generated = poisoning risk"
            )
            
            learns_in_production = st.checkbox(
                "Real-time learning (updates from production data)" + (" (✨ AI-suggested)" if suggested else ""),
                value=suggested.learns_in_production if suggested else False,
                help="Online learning = drift, poisoning, loss of reproducibility"
            )

        with st.expander("🌍 Privacy & Data Governance (Optional - Click to Expand)", expanded=False):
            st.caption("Data sovereignty and explainability requirements.")
            
            international_data = st.checkbox(
                "Cross-border data transfers" + (" (✨ AI-suggested)" if suggested else ""),
                value=suggested.international_data if suggested else False,
                help="GDPR adequacy decisions, Schrems II, data sovereignty concerns"
            )
            
            explainability_options = ["Inherently Interpretable", "Post-hoc Explainable", "Limited Explainability", "Black Box"]
            explainability_index = explainability_options.index(suggested.explainability_level) if suggested and suggested.explainability_level in explainability_options else 1
            explainability_level = st.selectbox(
                "Explainability Level" + (" (✨ AI-suggested)" if suggested else ""),
                options=explainability_options,
                index=explainability_index,
                help="Black Box = GDPR Art. 22 compliance issues, harder to debug"
            )

        with st.expander("🔗 Supply Chain & Dependencies (Optional - Click to Expand)", expanded=False):
            st.caption("Third-party model and data dependencies.")
            
            foundation_model_options = ["No Third-Party", "Self-Hosted Open Source", "Self-Hosted Proprietary", "External API", "Hybrid"]
            foundation_model_index = foundation_model_options.index(suggested.uses_foundation_model) if suggested and suggested.uses_foundation_model in foundation_model_options else 0
            uses_foundation_model = st.selectbox(
                "Foundation Model Usage" + (" (✨ AI-suggested)" if suggested else ""),
                options=foundation_model_options,
                index=foundation_model_index,
                help="External API = data leakage risk to OpenAI/Anthropic/etc."
            )

        with st.expander("⚠️ Content & Misuse Risks (Optional - Click to Expand)", expanded=False):
            st.caption("Synthetic content generation and dual-use potential.")
            
            generates_synthetic_content = st.checkbox(
                "Generates synthetic content (text/images/audio/video)" + (" (✨ AI-suggested)" if suggested else ""),
                value=suggested.generates_synthetic_content if suggested else False,
                help="Deepfakes, C2PA provenance requirements, EU AI Act Art. 52 transparency"
            )
            
            dual_use_options = ["None", "Low", "Moderate", "High"]
            dual_use_index = dual_use_options.index(suggested.dual_use_risk) if suggested and suggested.dual_use_risk in dual_use_options else 0
            dual_use_risk = st.selectbox(
                "Dual-Use / Weaponization Risk" + (" (✨ AI-suggested)" if suggested else ""),
                options=dual_use_options,
                index=dual_use_index,
                help="High = export controls, misuse potential (bio research AI, cyber tools)"
            )

        with st.expander("⚖️ Rights & Equity (Optional - Click to Expand)", expanded=False):
            st.caption("Decision reversibility and vulnerable populations.")
            
            reversibility_options = ["Fully Reversible", "Reversible with Cost", "Difficult to Reverse", "Irreversible"]
            reversibility_index = reversibility_options.index(suggested.decision_reversible) if suggested and suggested.decision_reversible in reversibility_options else 0
            decision_reversible = st.selectbox(
                "Decision Reversibility" + (" (✨ AI-suggested)" if suggested else ""),
                options=reversibility_options,
                index=reversibility_index,
                help="Irreversible decisions require highest safeguards (right to appeal)"
            )
            
            protected_populations = st.multiselect(
                "Protected / Vulnerable Populations" + (" (✨ AI-suggested)" if suggested else ""),
                options=["Children", "Elderly", "People with Disabilities", "Low-Income / Unbanked", 
                        "Non-Native Speakers / Low Literacy", "Asylum Seekers / Immigrants", 
                        "Incarcerated Persons", "Healthcare Vulnerable"],
                default=suggested.protected_populations if suggested else [],
                help="Civil rights obligations (ADA, Fair Housing); EU AI Act prohibited uses"
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
        model_type=model_type,
        data_source=data_source,
        learns_in_production=learns_in_production,
        international_data=international_data,
        explainability_level=explainability_level,
        uses_foundation_model=uses_foundation_model,
        generates_synthetic_content=generates_synthetic_content,
        dual_use_risk=dual_use_risk,
        decision_reversible=decision_reversible,
        protected_populations=list(protected_populations),
    )
    assessment = calculate_risk_score(risk_inputs)
    scenario_context = _build_scenario_context(risk_inputs, assessment.tier)

    controls = select_applicable_controls(packs, scenario_context)

    # Generate unified governance assessment
    st.markdown("---")
    st.subheader("📋 Governance Assessment")
    
    # Build comprehensive prose assessment
    risk_tier_icons = {
        "Low": "🟢",
        "Medium": "🟡",
        "High": "🟠",
        "Critical": "🔴"
    }
    risk_icon = risk_tier_icons.get(assessment.tier, "⚪")
    
    # Start with risk tier
    st.markdown(f"### {risk_icon} Risk Classification: **{assessment.tier}**")
    
    # Build narrative assessment combining AI and traditional analysis
    assessment_narrative = []
    
    # Include AI reasoning if available
    if st.session_state.ai_analysis and hasattr(st.session_state.ai_analysis, 'estimated_risk_tier'):
        ai_analysis = st.session_state.ai_analysis
        assessment_narrative.append(f"**Analysis:** {ai_analysis.reasoning}")
        
        # Note if AI and traditional engine differ
        if ai_analysis.estimated_risk_tier != assessment.tier:
            assessment_narrative.append(f"\n*Note: Initial AI assessment suggested {ai_analysis.estimated_risk_tier} risk tier based on scenario description, while the formal scoring model yielded {assessment.tier} (score: {assessment.score}). This variance may indicate nuances worth reviewing with legal/compliance.*")
    else:
        # Traditional assessment only
        assessment_narrative.append(f"**Risk Score:** {assessment.score} points across {len(assessment.contributing_factors)} factors.")
    
    # Contributing factors
    if assessment.contributing_factors:
        factors_text = ", ".join(assessment.contributing_factors)
        assessment_narrative.append(f"\n**Key Risk Drivers:** {factors_text}")
    
    # Framework alignment (from AI if available)
    if st.session_state.ai_analysis and hasattr(st.session_state.ai_analysis, 'framework_alignment'):
        assessment_narrative.append(f"\n**Regulatory Frameworks Implicated:** {st.session_state.ai_analysis.framework_alignment}")
    
    # Key risk factors (from AI if available)
    if st.session_state.ai_analysis and hasattr(st.session_state.ai_analysis, 'key_risk_factors') and st.session_state.ai_analysis.key_risk_factors:
        risks_bullets = "\n".join([f"- {risk}" for risk in st.session_state.ai_analysis.key_risk_factors])
        assessment_narrative.append(f"\n**Specific Risks Identified:**\n{risks_bullets}")
    
    # Render the full narrative
    st.markdown("\n\n".join(assessment_narrative))
    
    # Recommended safeguards section
    if st.session_state.ai_analysis and hasattr(st.session_state.ai_analysis, 'recommended_safeguards') and st.session_state.ai_analysis.recommended_safeguards:
        st.markdown("\n**Recommended Governance Controls:**")
        for i, safeguard in enumerate(st.session_state.ai_analysis.recommended_safeguards, 1):
            st.markdown(f"{i}. {safeguard}")
        st.caption("*These recommendations are derived from AI analysis of the scenario against established governance frameworks. Review the policy pack controls below for formal requirements.*")

    # Standards tags
    st.markdown("---")
    st.markdown("**📚 Governance Standards Applied:**")
    
    # Collect unique authorities from triggered controls
    authorities = set()
    for control in controls:
        authorities.add(control.authority)
    
    # Display as badges/tags
    if authorities:
        # Create color-coded badges for different standards
        standard_colors = {
            "NIST AI RMF": "#0066cc",
            "EU AI Act": "#003399",
            "ISO/IEC 42001": "#006600",
            "OWASP LLM Top 10": "#cc0000",
            "MITRE ATLAS": "#990000",
            "US OMB M-24-10": "#4d4d4d"
        }
        
        badge_html = " ".join([
            f'<span style="background-color: {standard_colors.get(auth, "#666666")}; color: white; padding: 4px 12px; border-radius: 12px; margin: 4px; display: inline-block; font-size: 0.85em;">{auth}</span>'
            for auth in sorted(authorities)
        ])
        st.markdown(badge_html, unsafe_allow_html=True)
    else:
        st.caption("No specific standards triggered for this risk profile.")
    
    # Safeguards surface authority + clause so reviewers can trace each recommendation.
    st.markdown("---")
    st.subheader("Required Safeguards from Policy Packs")
    st.caption("These safeguards are triggered by the traditional risk engine based on YAML policy packs.")
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
    
    # Owners & Next Steps
    st.markdown("---")
    st.subheader("👥 Owners & Next Steps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**System Owner:** {owner if owner else 'Not specified'}")
        st.markdown(f"**Approver:** {approver if approver else 'Not specified'}")
        st.caption("These roles are responsible for implementing and monitoring safeguards")
    
    with col2:
        review_interval_days = 90  # Default from exporters.py
        st.markdown(f"**Next Review:** {review_interval_days} days from approval")
        st.markdown(f"**Risk Tier:** {assessment.tier}")
        st.caption("Higher-risk systems should be reviewed more frequently")
    
    st.markdown("**📋 Recommended Next Steps:**")
    
    # Generate context-aware next steps
    next_steps = []
    
    if assessment.tier in ["High", "Critical"]:
        next_steps.append("1. **Immediate:** Schedule review with legal, privacy, and security teams before deployment")
        next_steps.append("2. **Pre-launch:** Conduct bias/fairness testing across demographic groups")
        next_steps.append("3. **Pre-launch:** Establish monitoring dashboards for model performance and drift")
    else:
        next_steps.append("1. **Pre-launch:** Review safeguards with compliance team")
        next_steps.append("2. **Pre-launch:** Document baseline performance metrics")
    
    if contains_pii:
        next_steps.append(f"4. **Pre-launch:** Complete Privacy Impact Assessment (PIA) or Data Protection Impact Assessment (DPIA)")
    
    if sector in ["Healthcare", "Finance"]:
        next_steps.append(f"5. **Pre-launch:** Obtain {sector} compliance team sign-off")
    
    if uses_foundation_model != "No Third-Party":
        next_steps.append("6. **Pre-launch:** Review vendor contracts for AI-specific terms (data retention, training prohibitions)")
    
    if autonomy_level >= 2:
        next_steps.append("7. **Post-launch:** Implement human oversight escalation procedures")
    
    next_steps.append(f"8. **Post-launch:** Schedule first review in {review_interval_days} days")
    next_steps.append("9. **Ongoing:** Monitor for model drift, bias, and performance degradation")
    
    for step in next_steps:
        st.markdown(step)
    
    st.info("💡 **Tip:** Assign specific owners to each next step and track completion in your project management system")

    # Interactive Governance Q&A (NEW)
    if st.session_state.ai_analysis and hasattr(st.session_state.ai_analysis, 'estimated_risk_tier'):
        st.markdown("---")
        st.subheader("💬 Ask Questions About This Assessment")
        st.caption("Get instant answers about safeguards, frameworks, implementation steps, or draft stakeholder communications")
        
        # Initialize chat history
        if "governance_chat" not in st.session_state:
            st.session_state.governance_chat = []
        
        # Suggested questions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("❓ Why this risk tier?", use_container_width=True):
                st.session_state.pending_question = f"Why did this assessment result in {assessment.tier} tier? Explain the specific factors."
        with col2:
            if st.button("📋 Explain safeguards", use_container_width=True):
                st.session_state.pending_question = "Explain the most critical safeguards and why they're required for this scenario."
        with col3:
            if st.button("✉️ Draft email to legal", use_container_width=True):
                st.session_state.pending_question = "Draft a concise email to our legal team explaining why we need their review before launch."
        
        # Display chat history
        for msg in st.session_state.governance_chat:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        # Handle pending question from button clicks
        if "pending_question" in st.session_state:
            question = st.session_state.pending_question
            del st.session_state.pending_question
            
            # Process the question
            st.session_state.governance_chat.append({"role": "user", "content": question})
            
            # Get AI response
            with st.spinner("Thinking..."):
                try:
                    import os
                    # Use same API key source as main AI analysis
                    api_key = None
                    if api_key_input and api_key_input.strip():
                        api_key = api_key_input.strip()
                    if not api_key:
                        try:
                            api_key = st.secrets.get("OPENAI_API_KEY")
                        except:
                            pass
                    if not api_key:
                        api_key = os.getenv("OPENAI_API_KEY")
                    
                    if api_key:
                        response = _get_governance_answer(
                            question=question,
                            use_case=use_case,
                            assessment=assessment,
                            controls=controls,
                            ai_analysis=st.session_state.ai_analysis,
                            api_key=api_key
                        )
                        st.session_state.governance_chat.append({"role": "assistant", "content": response})
                    else:
                        st.session_state.governance_chat.append({
                            "role": "assistant",
                            "content": "⚠️ OpenAI API key required for Q&A. Please enter your API key in the field above or set OPENAI_API_KEY environment variable."
                        })
                except Exception as e:
                    st.session_state.governance_chat.append({
                        "role": "assistant", 
                        "content": f"❌ Error getting response: {str(e)}"
                    })
            
            st.rerun()
        
        # Chat input
        if question := st.chat_input("Ask about frameworks, safeguards, implementation steps, or request a draft..."):
            # Add user message
            st.session_state.governance_chat.append({"role": "user", "content": question})
            
            # Get AI response
            with st.spinner("Thinking..."):
                try:
                    import os
                    # Use same API key source as main AI analysis
                    api_key = None
                    if api_key_input and api_key_input.strip():
                        api_key = api_key_input.strip()
                    if not api_key:
                        try:
                            api_key = st.secrets.get("OPENAI_API_KEY")
                        except:
                            pass
                    if not api_key:
                        api_key = os.getenv("OPENAI_API_KEY")
                    
                    if api_key:
                        response = _get_governance_answer(
                            question=question,
                            use_case=use_case,
                            assessment=assessment,
                            controls=controls,
                            ai_analysis=st.session_state.ai_analysis,
                            api_key=api_key
                        )
                        st.session_state.governance_chat.append({"role": "assistant", "content": response})
                    else:
                        st.session_state.governance_chat.append({
                            "role": "assistant",
                            "content": "⚠️ OpenAI API key required for Q&A. Please enter your API key in the field above or set OPENAI_API_KEY environment variable."
                        })
                except Exception as e:
                    st.session_state.governance_chat.append({
                        "role": "assistant", 
                        "content": f"❌ Error getting response: {str(e)}"
                    })
            
            st.rerun()
        
        # Export chat history
        if st.session_state.governance_chat:
            chat_export = "# Governance Q&A Session\n\n"
            chat_export += f"**Scenario:** {use_case}\n\n"
            chat_export += f"**Risk Tier:** {assessment.tier} (score: {assessment.score})\n\n"
            chat_export += "---\n\n"
            
            for msg in st.session_state.governance_chat:
                role = "**You:**" if msg["role"] == "user" else "**Governance Advisor:**"
                chat_export += f"{role}\n{msg['content']}\n\n"
            
            st.download_button(
                label="📥 Export Q&A Session",
                data=chat_export,
                file_name="governance_qa_session.md",
                mime="text/markdown",
                use_container_width=True
            )
    
    if use_case:
        st.markdown("---")
        st.subheader("📝 Governance Summary & Additional Context")
        st.caption("Document the specific risks, regulations, and open questions that require legal/compliance review")
        
        # Generate a governance-focused summary
        summary_sections = []
        
        # Original use case
        summary_sections.append(f"**Use Case:** {use_case}")
        
        # Regulatory frameworks implicated
        if st.session_state.ai_analysis and hasattr(st.session_state.ai_analysis, 'framework_alignment'):
            summary_sections.append(f"\n**Frameworks Implicated:** {st.session_state.ai_analysis.framework_alignment}")
        
        # Key risks from both analyses
        all_risks = set()
        if st.session_state.ai_analysis and hasattr(st.session_state.ai_analysis, 'key_risk_factors'):
            all_risks.update(st.session_state.ai_analysis.key_risk_factors)
        if assessment.contributing_factors:
            all_risks.update(assessment.contributing_factors)
        
        if all_risks:
            risks_text = "\n".join([f"- {risk}" for risk in sorted(all_risks)])
            summary_sections.append(f"\n**Risk Factors:**\n{risks_text}")
        
        # Sector-specific considerations
        sector_considerations = {
            "Healthcare": "HIPAA compliance, FDA medical device classification, patient safety protocols",
            "Finance": "GLBA privacy requirements, fair lending (ECOA), model risk management (SR 11-7)",
            "Critical Infrastructure": "CISA critical infrastructure designation, sector-specific regulations, supply chain security",
            "Children": "COPPA compliance, enhanced consent mechanisms, age verification"
        }
        if sector in sector_considerations:
            summary_sections.append(f"\n**Sector-Specific Considerations:** {sector_considerations[sector]}")
        
        # Questions for clarification
        clarification_questions = []
        
        if contains_pii and international_data:
            clarification_questions.append("- What data transfer mechanisms are used for international flows? (Standard Contractual Clauses, Adequacy Decisions, Binding Corporate Rules?)")
        
        if high_stakes and autonomy_level >= 2:
            clarification_questions.append("- What human oversight mechanisms exist for high-stakes automated decisions?")
            clarification_questions.append("- Is there an appeals process for affected individuals?")
        
        if uses_foundation_model != "No Third-Party":
            clarification_questions.append("- What data is sent to external model providers? How is it protected?")
            clarification_questions.append("- Do vendor contracts include AI-specific terms (data retention, model training prohibitions)?")
        
        if generates_synthetic_content:
            clarification_questions.append("- Are synthetic outputs watermarked or labeled per EU AI Act Article 52 transparency requirements?")
        
        if sector == "Healthcare" or sector == "Finance":
            clarification_questions.append(f"- Has this been reviewed by {sector} compliance team for sector-specific regulations?")
        
        if dual_use_risk in ["Moderate", "High"]:
            clarification_questions.append("- Has export control classification been obtained? (EAR/ITAR applicability)")
        
        if protected_populations:
            pop_text = ", ".join(protected_populations)
            clarification_questions.append(f"- What accessibility accommodations exist for {pop_text}?")
        
        # Always ask about testing
        clarification_questions.append("- Has bias/fairness testing been conducted? What metrics were used?")
        clarification_questions.append("- What is the model performance baseline and monitoring plan?")
        
        if clarification_questions:
            questions_text = "\n".join(clarification_questions)
            summary_sections.append(f"\n**Questions for Legal/Compliance Review:**\n{questions_text}")
        
        # Render the complete summary
        st.markdown("\n\n".join(summary_sections))
        
        st.info("💡 **Tip:** Use this summary to structure conversations with legal, privacy, security, and compliance partners before deployment.")

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
