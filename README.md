# rai-toolkit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rai-toolkit.streamlit.app/)
![CI](https://github.com/hankthevc/rai-toolkit/workflows/CI/badge.svg)
![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Responsible AI governance-as-code.** A personal learning prototype demonstrating risk assessment, safeguards with policy citations, and exportable approval records—translating NIST AI RMF, EU AI Act, ISO/IEC 42001, OWASP LLM Top 10, MITRE ATLAS, and U.S. federal AI policy (OMB M-25-21) into executable Python.

**🚀 [Try the Live Demo](https://rai-toolkit.streamlit.app/)** ⏰ *App may sleep after inactivity; wakes in 30-60s*

**📄 [Portfolio Overview](PORTFOLIO.md)** — Detailed project walkthrough optimized for hiring managers and technical interviewers.

---

## What This Is / Isn't

**This is a personal prototype for learning.** It demonstrates how governance ideas can be expressed as simple rules and exportable artifacts. It is not production-grade and is not affiliated with or endorsed by any employer. Examples are illustrative and may contain errors.

**What it demonstrates:**
- Risk scoring with transparent, additive factors
- Policy-as-code with YAML-encoded governance frameworks
- Automated control selection based on risk profile
- Exportable Decision Records and Transparency Notes

**What it is NOT:**
- ❌ Not production software
- ❌ Not legal advice
- ❌ Not comprehensive (intentionally simplified for learning)
- ❌ Not validated for real-world deployment

**Built with AI coding assistance** (Cursor/Claude) to prioritize governance logic; test-backed and CI-gated.

## Quickstart

Follow these steps to stand up the Streamlit experience locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run project1_risk_framework/app.py
```

The app launches at `http://localhost:8501`. Enter a scenario, flag contextual risk modifiers, and download the generated Decision Record to test the full workflow end-to-end.

**AI Analysis (powered by OpenAI API):** The live demo uses AI to analyze scenarios and suggest risk factors. For local development, set your OpenAI API key:

```bash
export OPENAI_API_KEY="sk-..."
```

**Writing effective prompts for AI analysis:**
- ✅ **Good:** "A chatbot that helps hospital patients schedule appointments and refill prescriptions. It accesses their medical records to check medication history and insurance eligibility. Patients interact directly via web and mobile app. The system suggests appointment times but requires nurse approval for prescription refills."
- ✅ **Good:** "An internal code completion tool for our engineering team. It suggests code snippets based on our proprietary codebase. Engineers review all suggestions before committing. Only used by employees with existing code access. No customer data involved."
- ❌ **Too vague:** "A chatbot for customers" (missing: purpose, data, automation level, impact)

**For Analytics Dashboard:** Generate sample data to populate the analytics page:
```bash
python scripts/generate_sample_data.py --count 150
```

### Live Demo

**🌐 Production deployment:** https://rai-toolkit.streamlit.app/

> ⏰ **Note:** Streamlit Cloud apps may sleep after inactivity. If you see a "waking up" message, wait 30-60 seconds for the app to start. Once running, it stays active for your session.

Try the live app to:
- **Use AI to auto-fill** risk assessments from plain-language descriptions (NEW)
- Assess AI scenarios with the risk calculator
- View 15+ triggered safeguards for high-risk scenarios
- Download Decision Records as markdown files
- Explore governance analytics with 8+ interactive visualizations

### Deploy Your Own Instance

**Option 1: Streamlit Cloud (Free, 1-click deploy)**

[![Deploy to Streamlit Community Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy)

1. Fork this repository to your GitHub account
2. Click the badge above and authenticate with GitHub
3. Select your fork: `your-username/rai-toolkit`
4. Set main file path: `project1_risk_framework/app.py`
5. Add `OPENAI_API_KEY` secret in Streamlit Cloud settings (required for AI analysis)
6. Click "Deploy"

**Option 2: Docker (Local or cloud)**

```bash
# Build the image
docker build -t rai-toolkit .

# Run with OpenAI API key (required for AI analysis)
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-... rai-toolkit

# Access at http://localhost:8501
```

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for detailed deployment guides (Kubernetes, Heroku, AWS ECS, etc.).

### Working from the hosted sandbox

If you are collaborating through the coding assistant's sandbox environment and want to move the repository to your own machine, follow the export instructions in [`docs/ACCESSING_SANDBOX.md`](docs/ACCESSING_SANDBOX.md). The guide walks through creating a `git bundle`, copying it out of the container, and pushing the history to your GitHub remote.

## 60-Second Tour for Recruiters

**What this demonstrates:** Translating AI governance policy into executable code—risk triage, safeguard assignment, and audit-ready decision records.

**Start here:**
1. **[Live Demo](https://rai-toolkit.streamlit.app/)** (2 min) — Enter "healthcare chatbot" scenario → see 15+ safeguards trigger with policy citations → download Decision Record
2. **[Healthcare Case Study](docs/case_studies/01_healthcare_chatbot.md)** (3 min) — Critical-tier assessment walkthrough showing PHI protection, adversarial testing, human oversight
3. **[Framework Crosswalks](docs/crosswalks/)** (1 min skim) — How safeguards map to NIST AI RMF, EU AI Act, ISO 42001, OWASP LLM Top 10, MITRE ATLAS
4. **Code deep-dive** (5 min) — [`common/utils/risk_engine.py`](common/utils/risk_engine.py) shows transparent scoring logic; [`common/policy_packs/`](common/policy_packs/) shows YAML-encoded safeguards with policy references

**Skills on display:** 
- Python (Streamlit, pytest, Pydantic), policy-as-code design, threat modeling
- **Comprehensive AI risk knowledge:** LLM threats (OWASP), adversarial ML (MITRE ATLAS), supply chain security, data provenance, explainability (GDPR), dual-use risks (export controls), protected populations (civil rights)
- Cross-functional communication (policy ↔ engineering ↔ legal), CI/CD (GitHub Actions)

- **Outcome-focused:** 6 policy frameworks, 60+ safeguards, 3 case studies, full CI/CD—shipped in days, not months

**The workflow:** Plain-language intent → AI generates scaffolding → I refine logic/policy accuracy → AI writes tests/docs → iterate. This is how governance-as-code should operate: rapid experimentation, transparent decision logic, and continuous validation.

Now, the app uses AI to **autofill risk assessments** from plain-language descriptions—meta, but fitting.

## How Project 1 Operates

1. **AI-powered scenario parsing (NEW):** Paste a plain-language use case description → OpenAI API analyzes it against 20+ risk dimensions → get suggested values with reasoning → review and approve → auto-fill the form. Meta-governance: AI built this tool, now AI helps *you* assess AI.
2. **Comprehensive risk assessment:** 16 risk factors across 5 categories:
   - **Core:** PII, customer-facing, high-stakes, autonomy, sector, modifiers
   - **Technical AI/ML:** Model type (LLM/CV/RL), data source, online learning
   - **Privacy & governance:** Cross-border data, explainability level
   - **Supply chain:** Foundation model dependencies (OpenAI API, self-hosted, etc.)
   - **Content & misuse:** Synthetic content generation, dual-use risk
   - **Rights & equity:** Decision reversibility, protected populations
3. **Risk scoring:** A transparent additive model converts 16 inputs into a tier (Low/Medium/High/Critical) that teams can defend in interviews and audit readouts.
4. **Policy selection:** YAML policy packs encode safeguards from recognized frameworks (NIST AI RMF, EU AI Act, OWASP LLM Top 10, MITRE ATLAS). Conditions match on risk tier, model type, data source, and more.
5. **Decision Record export:** The Streamlit UI and shared exporter produce a Markdown file summarizing the risk tier, selected controls, and review ownership so the outcome can be filed in a ticketing system.

Read the methodology deep dive in `docs/methodology_project1.md` for scoring rationale and governance trade-offs. A plain-language walkthrough of every file—written for early-career coders—is available in `docs/FILE_OVERVIEW.md`.

### Real-World Case Studies

See [`docs/case_studies/`](docs/case_studies/) for detailed analyses of three realistic scenarios:

1. **[Healthcare Patient Support Chatbot](docs/case_studies/01_healthcare_chatbot.md)** — Critical tier (score: 12) with 15 triggered safeguards spanning PHI protection, adversarial testing, and human oversight
2. **[Internal Code Copilot](docs/case_studies/02_internal_code_copilot.md)** — Low tier (score: 0) demonstrating appropriate de-escalation for internal, human-reviewed tooling
3. **[AI-Powered Hiring Platform](docs/case_studies/03_hiring_assessment_tool.md)** — Critical tier (score: 9) showing employment AI's unique risk profile under EU AI Act and identifying framework enhancement opportunities

**📄 [Sample Decision Record](docs/samples/sample_decision_record.md)** — See a complete exported decision record for the healthcare chatbot scenario, including stop-ship triggers, pre-launch requirements, and approval signatures.

## Testing & Quality Assurance

![Tests Passing](https://img.shields.io/badge/tests-63%20passed-success)
![Coverage](https://img.shields.io/badge/coverage-88%25-brightgreen)

**Continuous Integration:** Every push to `main` triggers GitHub Actions CI that runs:
- **63 unit tests** across risk scoring, policy loading, YAML validation, AI parsing, and export functionality
- **Code coverage analysis** (88% coverage across `common/` utilities)
- **Linting** with Ruff and Black formatting checks

**Test categories:**
- `test_risk_engine.py` — 30 tests validating scoring logic, tier thresholds, and all 16 risk factors
- `test_policy_loader.py` — 13 tests for YAML policy pack loading and conditional matching
- `test_ai_parser.py` — 7 tests for AI-powered scenario parsing (1 integration test skipped in CI)
- `test_exporters.py` — 8 tests for decision record generation
- `test_edge_cases.py` — 6 NEW tests for maximum/minimum risk scenarios, YAML integrity, and export validation

**Running tests locally:**
```bash
pytest tests/ -v                      # All tests
pytest tests/ --cov=common            # With coverage report
pytest tests/ -k "not integration"    # Skip tests requiring API keys
```

See [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for the full CI configuration.

## Data Handling (Demo)

**The live demo runs as a server-side Streamlit session with no database persistence.** Inputs exist only for the session and are discarded when it ends.

**AI analysis (core feature):**
- Your scenario descriptions are sent to OpenAI's API (gpt-4o) for analysis
- The AI suggests risk factors, which you can review and adjust
- Risk calculations and policy matching happen server-side in the Streamlit session
- Nothing is permanently stored

**Do not paste sensitive or production data.**

**For local/production use:**
- Run locally to control data flow entirely
- Review OpenAI's terms of service before sending any data to their API
- Validate with legal/privacy teams before processing actual sensitive information

**Security.md:** See [`SECURITY.md`](SECURITY.md) for vulnerability reporting. This is a learning prototype; treat it as such.

## Framework Crosswalks

Stakeholders often ask how safeguards align with familiar standards. Use the illustrative briefs in `docs/crosswalks/` when tailoring communications for:

### Policy Frameworks

This toolkit demonstrates illustrative alignment with several governance frameworks:

- **NIST AI RMF** — Govern/Map/Measure/Manage functions. Supports MAP-1.5 (supply chain), GOVERN-1.5 (data governance), NIST GenAI Profile risk areas
- **EU AI Act** — Annex III high-risk categories, Art. 52 (synthetic content transparency), Art. 13 (explainability). See [Official Journal L 178/2024](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)
- **ISO/IEC 42001** — AIMS documentation patterns (risk log, transparency note, decision record)
- **U.S. OMB M-25-21** — Federal AI inventory, impact assessment, rights protection (replaces M-24-10 effective Jan 2025). Acquisition: M-25-22 (replaces M-24-18)
- **OWASP LLM Top 10 (2025)** — Prompt injection (LLM01), data leakage (LLM06), supply chain (LLM05). See [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- **MITRE ATLAS** — Adversarial tactics (poisoning, evasion, exfiltration) mapped to model types
- **GDPR** — Art. 22 (explainability), Art. 44-50 (cross-border transfers), right to appeal

**Important:** All framework references are illustrative examples based on publicly available texts. They are **not** authoritative legal interpretations. Confirm requirements with counsel or compliance before treating them as canonical.

## Advanced Risk Factors

The toolkit now assesses **16 risk dimensions** across AI security, privacy, supply chain, and equity domains:

**Technical AI/ML Risks:**
- Model architecture type (LLM → OWASP risks; Computer Vision → deepfakes; RL → reward hacking)
- Training data provenance (Internet-scraped → copyright/bias; User-generated → poisoning)
- Real-time learning (drift, poisoning, reproducibility loss)

**Privacy & Data Governance:**
- Cross-border data transfers (GDPR adequacy, Schrems II)
- Explainability level (Black box → GDPR Art. 22 compliance issues)

**Supply Chain & Dependencies:**
- Foundation model usage (External API → data leakage to OpenAI/Anthropic)

**Content & Misuse:**
- Synthetic content generation (Deepfakes, C2PA provenance, EU AI Act Art. 52)
- Dual-use risk (Export controls, weaponization potential)

**Rights & Equity:**
- Decision reversibility (Irreversible → mandatory human review, appeals process)
- Protected populations (Elderly, disabilities, immigrants, incarcerated → enhanced safeguards)

See `docs/PROPOSED_RISK_FACTORS.md` for detailed rationale and governance alignment.

## Architecture Sketch

```
rai-toolkit/
├── common/                   # Policy packs, schema, and reusable governance utilities
├── project1_risk_framework/  # Streamlit application wiring the intake and Decision Record export
├── docs/                     # Methodology notes, learning journal, and educational explainers
├── tests/                    # Unit tests covering pack integrity and risk tier behavior
└── .github/                  # CI pipeline and community health configuration
```

## Operational Guardrails

### Responsible Use

This repository focuses on defensive responsible AI governance. It is non-legal guidance and does not replace counsel, compliance, or threat intelligence teams.

### Not Legal Advice

The content in this repository is provided for educational and defensive research purposes only. Validate requirements with legal, privacy, and security professionals before production use.

### Security Reporting

Potential vulnerabilities should be reported privately following the instructions in `SECURITY.md` so we can triage and remediate responsibly.

## Contribution Signals

- **Issues and PRs:** Use the provided templates inside `.github/` to capture risk context, test coverage, and safety considerations.
- **Coding standards:** Format Python with Black, lint with Ruff, and sort imports with isort via the `pyproject.toml` configuration. Optional pre-commit hooks (`.pre-commit-config.yaml`) help enforce this locally.
- **Continuous integration:** GitHub Actions (`.github/workflows/ci.yml`) installs dependencies and runs `pytest -q` on every pull request to keep policy packs and scoring logic healthy.

## Project Status

- **Current milestone:** Project 1 — Frontier AI Risk Assessment Framework (v1.0 ready for production review)
- **Deployment:** Live demo running at [rai-toolkit.streamlit.app](https://rai-toolkit.streamlit.app/)
- **Documentation:** 3 case studies, 6 framework crosswalks, methodology deep-dive, and educational FILE_OVERVIEW
- **Testing:** CI/CD pipeline with automated policy pack validation and risk tier tests
- **Next steps:** Gather feedback from AI governance practitioners, explore Project 2 (continuous monitoring)

## Contact

Questions about responsible use or potential improvements can be raised via issues. Sensitive disclosures should follow the contact guidance in `SECURITY.md`.

---

## About the Author

**Henry Appel** — AI security strategist and former White House NSC policy advisor. I've built cross‑government coalitions (12 agencies, 30+ international partners) against spyware, run intelligence downgrades that protected U.S. elections, and now design red‑team frameworks for frontier systems at 2430 Group.

I built this RAI Toolkit to demonstrate governance‑as‑code in practice: quick risk triage, safeguards with policy citations, and exportable decision records that bridge policy, security, and engineering teams.

**Background:** West Wing aide & intelligence policy advisor at the NSC (2023–2024); IC analyst/operator at ODNI/NCTC (2018–2025) across PRC/DPRK cyber, ransomware, spyware, and illicit tech transfers; M.A. Security Studies, Georgetown.

**Connect:** [henryappel@gmail.com](mailto:henryappel@gmail.com) | Washington, DC
