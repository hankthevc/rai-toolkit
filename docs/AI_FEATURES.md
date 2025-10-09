# AI Features in the RAI Toolkit

## Meta-Governance: AI Assessing AI

This project demonstrates two layers of AI integration:

1. **Built with AI** (vibecoding) — The entire toolkit was developed using AI coding assistants
2. **Uses AI** (intelligent parsing) — The app now uses OpenAI's API to help users assess AI systems

---

## 🤖 AI-Powered Scenario Parsing

### What It Does

Paste a plain-language description of your AI use case, and GPT-4o analyzes it to suggest:
- PII/sensitive data handling
- Customer-facing status
- High-stakes impact assessment
- Autonomy level (0-3)
- Primary sector
- Risk modifiers (Bio, Cyber, Disinformation, Children)

You review the AI's reasoning before accepting the suggestions, then the form auto-fills.

### Why This Matters for Hiring

This feature demonstrates:
- **LLM integration skills** — OpenAI API with structured outputs via Pydantic models
- **Prompt engineering** — Carefully designed system prompts for consistent risk assessment
- **Human-in-the-loop design** — AI suggests, humans approve, maintaining governance integrity
- **Transparency** — AI reasoning is always shown, never hidden
- **Meta-awareness** — Using AI to govern AI shows practical understanding of the technology

### How to Use

1. **Set API Key** (one-time setup):
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```
   Or enter directly in the app UI

2. **Write a Good Prompt**:
   ```
   A chatbot that helps hospital patients schedule appointments and 
   refill prescriptions. It accesses their medical records to check 
   medication history and insurance eligibility. Patients interact 
   directly via web and mobile app. The system suggests appointment 
   times but requires nurse approval for prescription refills.
   ```

3. **Click "Analyze with AI"** → Review the suggestions → Scroll down to see the form pre-filled

### Prompt Engineering Tips

**Include these 6 elements:**

1. **What the AI does** — Core functionality and decision-making role
2. **Who uses it** — Internal vs. external, vulnerable populations
3. **What data it processes** — Personal info, health records, financial data
4. **Level of automation** — Suggests, assists, decides with oversight, or acts autonomously
5. **Impact domain** — What happens if it makes a mistake? (safety, rights, finances)
6. **Context flags** — Healthcare, finance, children, cybersecurity, bio, disinformation

**Examples:**

✅ **Good:** "An automated trading system that buys and sells securities based on market signals. It executes trades autonomously up to $50K per trade without human review. Larger trades escalate to compliance. Processes real-time market data and client portfolio information."

❌ **Too vague:** "AI for trading" (missing: autonomy level, data, thresholds, oversight)

---

## 🛠️ Built with AI Coding Assistance (Vibecoding)

### The Development Approach

This entire toolkit—risk engine, policy packs, Streamlit UI, tests, documentation—was built iteratively using AI coding assistants (Claude, Cursor). Instead of spending weeks on boilerplate, I focused on:

- **Governance logic accuracy** — Ensuring risk tiers align with real frameworks
- **Policy fidelity** — Validating citations match NIST AI RMF, EU AI Act, etc.
- **Threat modeling** — Designing safeguard triggers based on security experience
- **User experience** — Making governance accessible to non-lawyers

AI handled:
- **Scaffolding** — Project structure, imports, type hints
- **Test generation** — pytest suites with edge case coverage
- **Documentation formatting** — Markdown, docstrings, READMEs
- **Debugging** — Linter errors, import issues, UI quirks

### The Workflow

```
Plain-language intent
    ↓
AI generates scaffolding
    ↓
Human refines logic/policy accuracy
    ↓
AI writes tests & docs
    ↓
Iterate based on results
```

### Why This Matters for Recruiters

**Experimental mindset:**
- I treat AI as a force-multiplier, not a replacement
- Rapid prototyping to test governance concepts in days, not months

**Maximizing frontier capabilities:**
- As someone who designs red-team frameworks for frontier AI systems at 2430 Group, I leverage those same frontier capabilities for my own workflows
- Building *with* AI teaches its capabilities and limitations firsthand

**Outcome-focused:**
- 6 policy frameworks, 60+ safeguards, 3 case studies, full CI/CD pipeline
- Shipped in days while maintaining quality and test coverage

**Transparent about tooling:**
- Modern AI governance work requires hands-on understanding of AI
- I'm upfront about using AI assistance—it's a feature, not something to hide

### Evidence of Vibecoding

**Code quality maintained:**
- Full pytest test suite (90%+ coverage)
- Clean linter output (Black, Ruff, isort)
- Type hints throughout
- Modular, maintainable architecture

**Documentation polish:**
- 6 framework crosswalk documents
- 3 detailed case studies
- Educational `FILE_OVERVIEW.md` for early-career developers
- Learning journal showing iterative refinement

**Rapid iteration:**
- Entire project from concept to production in < 2 weeks
- Live demo deployed on Streamlit Cloud
- CI/CD pipeline with GitHub Actions

---

## Technical Implementation

### AI Parser Architecture

**File:** `common/utils/ai_parser.py`

```python
from openai import OpenAI
from pydantic import BaseModel, Field

class ScenarioAnalysis(BaseModel):
    contains_pii: bool
    customer_facing: bool
    high_stakes: bool
    autonomy_level: int = Field(ge=0, le=3)
    sector: str
    modifiers: list[str]
    reasoning: str  # Shown to user for transparency

def parse_scenario_with_ai(description: str, api_key: str) -> ScenarioAnalysis:
    """Use OpenAI's structured output to parse scenarios."""
    client = OpenAI(api_key=api_key)
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[...],
        response_format=ScenarioAnalysis,
        temperature=0.3  # Lower for consistent risk assessment
    )
    return completion.choices[0].message.parsed
```

**Key design decisions:**
- **Structured outputs** via Pydantic — Type-safe, validated responses
- **Low temperature** (0.3) — Consistent risk assessment, not creative writing
- **Reasoning field** — Transparency for governance decisions
- **Human review** — Suggestions pre-fill the form but user can override

### Integration with Streamlit

**Session state management:**
```python
if "ai_analysis" not in st.session_state:
    st.session_state.ai_analysis = None

# Parse scenario
analysis = parse_scenario_with_ai(description)
st.session_state.ai_analysis = analysis

# Pre-fill form with suggested values
contains_pii = st.checkbox(
    "Processes PII",
    value=suggested.contains_pii if suggested else False,
    help="✨ AI-suggested" if suggested else None
)
```

**Benefits:**
- Non-blocking — AI parsing happens outside the form
- Reviewable — Users see reasoning before accepting
- Overridable — Human always has final say

---

## For Interviewers

### Questions This Project Answers

**"How do you integrate LLMs into production workflows?"**
→ Walk through the OpenAI API integration with structured outputs, error handling, and human-in-the-loop design

**"How do you approach prompt engineering?"**
→ Show the system prompt in `ai_parser.py` — detailed field definitions, examples, conservative risk bias

**"How do you build with AI coding assistance?"**
→ Discuss the vibecoding workflow: intent → scaffolding → refinement → testing

**"How do you ensure governance integrity when using AI?"**
→ Explain transparency (reasoning shown), human review (suggestions, not decisions), and validation (tests verify policy accuracy)

### Skills Demonstrated

- ✅ OpenAI API integration (structured outputs, error handling)
- ✅ Prompt engineering for consistent governance decisions
- ✅ Pydantic models for type-safe LLM outputs
- ✅ Human-in-the-loop UX design
- ✅ AI-assisted development (vibecoding)
- ✅ Testing LLM features (mocks, integration tests)

---

## Future Enhancements

Potential extensions to demonstrate advanced capabilities:

1. **Multi-model comparison** — Compare GPT-4o vs Claude vs Gemini suggestions
2. **Adversarial testing** — Use AI to generate edge cases for the risk engine
3. **Policy pack generation** — AI helps draft new safeguards from regulatory text
4. **Continuous learning** — Track which AI suggestions users override, refine prompts
5. **Explainability** — Highlight which words in the description triggered which modifiers

---

*This document demonstrates both the technical implementation and the strategic thinking behind using AI in governance workflows.*

