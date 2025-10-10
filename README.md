# rai-toolkit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rai-toolkit.streamlit.app/)
![CI](https://github.com/hankthevc/rai-toolkit/workflows/CI/badge.svg)
![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Responsible AI governance-as-code.** A personal learning prototype demonstrating risk assessment, safeguards with policy citations, and exportable decision records—translating NIST AI RMF, EU AI Act, ISO/IEC 42001, OWASP LLM Top 10, MITRE ATLAS, and U.S. federal AI policy (OMB M-25-21) into executable Python.

**🚀 [Try the Live Demo](https://rai-toolkit.streamlit.app/)** ⏰ *App may sleep after inactivity; wakes in 30-60s*

---

## What This Is / Isn't

**This is a personal prototype for learning.** It demonstrates how governance ideas can be expressed as simple rules and exportable artifacts. It is not production-grade and is not affiliated with or endorsed by any employer. Examples are illustrative and may contain errors.

**What it demonstrates:**
- AI-powered risk assessment via conversational interview (using GPT-4o)
- Risk scoring with transparent, additive factors (16 dimensions)
- Policy-as-code with YAML-encoded governance frameworks
- Automated control selection based on risk profile
- Interactive Q&A about governance recommendations
- Exportable Decision Records and Transparency Notes

**What it is NOT:**
- ❌ Not production software
- ❌ Not legal advice  
- ❌ Not comprehensive (intentionally simplified for learning)
- ❌ Not validated for real-world deployment

**Built with AI coding assistance** (Cursor/Claude) to prioritize governance logic; test-backed and CI-gated.

---

## How It Works

### 1. Describe Your AI System

Paste a plain-language description of your AI use case. The AI interviewer (GPT-4o) will:
- Ask 3-4 clarifying questions about your scenario
- Analyze your responses against 16 risk dimensions
- Suggest risk factor values with reasoning

### 2. Review AI Analysis

The AI provides:
- Estimated risk tier (Low/Medium/High/Critical)
- Key risk factors identified
- Recommended safeguards from governance frameworks
- Framework alignment (which standards apply)
- Gaps & limitations (what couldn't be assessed)

### 3. Get Governance Recommendations

The system automatically:
- Calculates an additive risk score (0-42 points)
- Assigns a risk tier based on score thresholds
- Matches your scenario to 60+ controls from 7 policy packs
- Shows which frameworks apply (NIST, EU AI Act, ISO 42001, etc.)
- Generates owner assignments and next steps

### 4. Ask Questions & Refine

After the initial assessment:
- **Ask follow-up questions** via the built-in Q&A interface
- **Fill gaps** if you have additional details the AI couldn't assess
- **Re-analyze** with enriched context for a more comprehensive assessment

### 5. Export Documentation

Download two artifacts:
- **Decision Record** (`.md`) — Complete risk assessment with safeguards and approval routing
- **Transparency Note stub** (`.md`) — Stakeholder communication template (requires completion)

---

## Quickstart

### Local Setup

```bash
# 1. Clone and setup environment
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 2. Set OpenAI API key (required for AI analysis)
export OPENAI_API_KEY="sk-..."

# 3. Run the app
streamlit run project1_risk_framework/app.py
```

The app launches at `http://localhost:8501`.

### Live Demo

**🌐 Try it now:** https://rai-toolkit.streamlit.app/

> ⏰ **Note:** Streamlit Cloud apps sleep after inactivity. Wait 30-60 seconds if you see a "waking up" message.
> 
> 💡 **Tip:** If the demo is sleeping or you have no API key, enable **"Demo mode"** in the sidebar to explore the workflow without external API calls.

**What you can do:**
- Describe an AI scenario and get an instant risk assessment
- Answer AI interviewer questions for comprehensive analysis
- Ask questions about the governance recommendations
- Download Decision Records and Transparency Notes
- Explore the Analytics dashboard (sample data pre-loaded)

---

## Deploy Your Own

### Option 1: Streamlit Cloud (Free, 1-click)

[![Deploy to Streamlit Community Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy)

1. Fork this repository
2. Click the badge above and authenticate with GitHub
3. Select your fork: `your-username/rai-toolkit`
4. Set main file: `project1_risk_framework/app.py`
5. Add `OPENAI_API_KEY` secret in Streamlit Cloud settings
6. Deploy

### Option 2: Docker

```bash
# Build
docker build -t rai-toolkit .

# Run
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-... rai-toolkit

# Access at http://localhost:8501
```

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for Kubernetes, Heroku, AWS ECS, etc.

---

## Key Features

### AI-Powered Interview Mode

The core feature is a conversational risk assessment:

1. **Initial analysis:** AI reads your scenario description and identifies obvious risk factors
2. **Clarifying questions:** AI asks 3-4 targeted questions to fill gaps (e.g., "Where is data stored?", "Who reviews decisions?")
3. **Comprehensive assessment:** AI synthesizes all information into a detailed risk profile
4. **Gap identification:** AI explicitly notes what it couldn't assess and why

**Powered by GPT-4o** for structured output and nuanced governance reasoning.

### 16 Risk Dimensions

The toolkit assesses across:

**Core Factors:**
- Contains PII/PHI
- Customer-facing exposure
- High-stakes outcomes
- Autonomy level (0-3: suggestion → full autonomy)
- Sector sensitivity (Healthcare, Finance, Critical Infrastructure, Children)
- Risk modifiers (Bio, Cyber, Disinformation, Children)

**Technical AI/ML:**
- Model type (Traditional ML, LLM, Computer Vision, Multimodal, RL)
- Training data source (Proprietary, Public, Internet-scraped, User-generated, Third-party, Synthetic)
- Online learning (real-time model updates)

**Privacy & Governance:**
- Cross-border data transfers
- Explainability level (Interpretable → Black Box)

**Supply Chain:**
- Foundation model dependencies (No third-party, Self-hosted, External API)

**Content & Misuse:**
- Synthetic content generation
- Dual-use risk (Export controls, Weaponization)

**Rights & Equity:**
- Decision reversibility (Fully reversible → Irreversible)
- Protected populations (Children, Elderly, Low-income, etc.)

### Policy-as-Code (7 Frameworks)

Governance controls encoded as YAML with conditional matching:

- **NIST AI RMF** — Govern/Map/Measure/Manage functions
- **EU AI Act** — Annex III high-risk categories, Art. 52, Art. 13
- **ISO/IEC 42001** — AIMS documentation requirements
- **U.S. OMB M-25-21** — Federal AI inventory, impact assessment (replaces M-24-10)
- **OWASP LLM Top 10 (2025)** — Prompt injection, data leakage, supply chain
- **MITRE ATLAS** — Adversarial ML tactics
- **Extended Risk Factors** — Advanced matching on model type, data source, etc.

60+ controls automatically match based on your scenario's risk profile.

### Interactive Governance Q&A

After assessment, ask questions like:
- "Why is this flagged as high risk?"
- "What if we add human review?"
- "How do we comply with GDPR Art. 22?"

The AI provides context-aware answers based on your specific assessment.

### Gap-Driven Refinement

If the AI identifies gaps (e.g., "Data storage location unknown"), you can:
1. Provide additional details
2. Click "Re-Analyze with Additional Context"
3. Get an updated assessment with fewer gaps

---

## Testing & Quality

![Tests](https://img.shields.io/badge/tests-70%20passing-success)
![Coverage](https://img.shields.io/badge/coverage-69%25-yellow)

**CI/CD:** GitHub Actions runs on every push to `main`:
- 70 automated tests (risk scoring, policy loading, YAML validation, AI parsing, exports)
- Code coverage analysis (69% across `common/` utilities)
- Linting with Ruff and formatting with Black

**Test breakdown:**
- `test_risk_engine.py` — 30 tests for scoring logic, tier thresholds, all 16 factors
- `test_policy_loader.py` — 16 tests for YAML loading and conditional matching
- `test_ai_parser.py` — 8 tests for AI scenario parsing (1 integration test skipped in CI)
- `test_exporters.py` — 8 tests for decision record generation
- `test_edge_cases.py` — 6 tests for max/min risk scenarios, YAML integrity, export validation
- `test_policy_packs.py` — 2 tests for policy pack structure

**Run tests locally:**
```bash
pytest tests/ -v                      # All tests
pytest tests/ --cov=common            # With coverage
pytest tests/ -k "not integration"    # Skip API-requiring tests
```

---

## Data Handling

**The live demo is server-side Streamlit with no database.** Your inputs exist only during your session and are not persisted.

**When you use AI analysis:**
- Scenario descriptions → sent to OpenAI API (GPT-4o)
- Interview questions & answers → sent to OpenAI API
- Risk calculations & policy matching → happen server-side in Streamlit
- Nothing is permanently stored

**Do not paste sensitive or production data.**

**For local use:**
- Run locally to control data flow
- Review OpenAI's [Terms of Service](https://openai.com/policies/terms-of-use)
- Validate with legal/privacy teams before processing actual data

See [`SECURITY.md`](SECURITY.md) for vulnerability reporting.

---

## Documentation

### Case Studies

See [`docs/case_studies/`](docs/case_studies/) for detailed walkthroughs:

1. **[Healthcare Patient Chatbot](docs/case_studies/01_healthcare_chatbot.md)** — Critical tier with PHI, human oversight, adversarial testing
2. **[Internal Code Copilot](docs/case_studies/02_internal_code_copilot.md)** — Low tier showing appropriate de-escalation
3. **[AI-Powered Hiring Platform](docs/case_studies/03_hiring_assessment_tool.md)** — Critical tier employment AI

**Sample Artifacts:**
- [Sample Decision Record](docs/samples/sample_decision_record.md)
- [Sample Transparency Note](docs/samples/sample_transparency_note.md)

### Methodology

- **[Methodology Deep-Dive](docs/methodology_project1.md)** — Scoring rationale, stop-ship rules, governance trade-offs
- **[Framework Crosswalks](docs/crosswalks/)** — How controls map to NIST, EU AI Act, ISO 42001, OWASP, MITRE ATLAS, OMB

---

## Framework Alignment

This toolkit demonstrates **illustrative** alignment with several governance frameworks. All references are based on publicly available texts and are **not** authoritative legal interpretations.

**Policy Frameworks Included:**
- **NIST AI RMF** — Govern/Map/Measure/Manage, GenAI Profile risk areas
- **EU AI Act** — Annex III high-risk, Art. 52 (synthetic content), Art. 13 (explainability). [Official Journal L 178/2024](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)
- **ISO/IEC 42001** — AIMS documentation patterns (risk log, transparency note)
- **U.S. OMB M-25-21** — Federal AI inventory, impact assessment (replaces M-24-10, Jan 2025)
- **OWASP LLM Top 10 (2025)** — Prompt injection (LLM01), data leakage (LLM06), supply chain (LLM05). [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- **MITRE ATLAS** — Adversarial ML tactics (poisoning, evasion, exfiltration)
- **GDPR** — Art. 22 (explainability), Art. 44-50 (cross-border transfers)

**Confirm requirements with counsel or compliance before treating as canonical.**

---

## Architecture

```
rai-toolkit/
├── common/
│   ├── policy_packs/          # 7 YAML policy packs with 60+ controls
│   ├── schema/                 # JSON schema for policy pack validation
│   └── utils/
│       ├── ai_parser.py        # GPT-4o scenario analysis
│       ├── ai_interviewer.py   # Multi-turn Q&A interview logic
│       ├── risk_engine.py      # Additive risk scoring (16 factors)
│       ├── policy_loader.py    # YAML loading & conditional matching
│       ├── exporters.py        # Decision Record generation
│       └── exporters_transparency_note.py  # Transparency Note stub
├── project1_risk_framework/
│   ├── app.py                  # Main Streamlit UI
│   └── pages/
│       └── 1_📊_Analytics.py  # Multi-page analytics dashboard
├── tests/                      # 70 unit tests (pytest)
└── docs/
    ├── case_studies/           # 3 detailed scenario walkthroughs
    ├── crosswalks/             # 6 framework alignment documents
    ├── samples/                # Sample exports
    └── methodology_project1.md # Scoring rationale & stop-ship rules
```

---

## For Recruiters

**What this demonstrates:** Translating AI governance policy into executable code—risk triage, safeguard assignment, and audit-ready decision records.

**60-second tour:**
1. **[Live Demo](https://rai-toolkit.streamlit.app/)** (2 min) — Describe "healthcare chatbot" → AI asks clarifying questions → see 15+ safeguards trigger with policy citations → download Decision Record
2. **[Healthcare Case Study](docs/case_studies/01_healthcare_chatbot.md)** (3 min) — Critical-tier walkthrough with PHI protection, adversarial testing, human oversight
3. **[Code: risk_engine.py](common/utils/risk_engine.py)** (2 min) — Transparent scoring logic
4. **[Code: Policy packs](common/policy_packs/)** (2 min) — YAML-encoded safeguards with framework references

**Skills on display:**
- Python (Streamlit, pytest, Pydantic), OpenAI API integration, policy-as-code design
- AI risk knowledge: LLM threats (OWASP), adversarial ML (MITRE), supply chain, data provenance, explainability, dual-use, protected populations
- Cross-functional communication (policy ↔ engineering ↔ legal)
- CI/CD (GitHub Actions), test-driven development

---

## Contributing

This is a personal learning project, but feedback welcome:

- **Issues:** Bug reports, feature ideas, or governance suggestions
- **Security:** See `SECURITY.md` for vulnerability reporting
- **Coding standards:** Black formatting, Ruff linting, pytest (see `.github/workflows/ci.yml`)

Not accepting pull requests at this time—this is a portfolio/learning artifact, not a collaborative project.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

This is a demonstration tool for educational purposes. Not affiliated with or endorsed by NIST, EU, ISO, OWASP, MITRE, or any government or standards body.

---

## About

**Henry Appel** — AI security strategist and former White House NSC policy advisor.

I built this to demonstrate governance-as-code in practice: quick risk triage, safeguards with policy citations, and exportable decision records that bridge policy, security, and engineering teams.

**Background:** West Wing aide & intelligence policy advisor at the NSC (2023–2024); IC analyst/operator at ODNI/NCTC (2018–2025) across PRC/DPRK cyber, ransomware, spyware, and illicit tech transfers; M.A. Security Studies, Georgetown.

**Connect:** [henryappel@gmail.com](mailto:henryappel@gmail.com) | Washington, DC

---

**[📄 Full Portfolio Overview](PORTFOLIO.md)** — Detailed project walkthrough for hiring managers
