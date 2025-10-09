# rai-toolkit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rai-toolkit.streamlit.app/)
![CI](https://github.com/hankthevc/rai-toolkit/workflows/CI/badge.svg)
![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Responsible AI governance-as-code.** Risk assessment, safeguards with policy citations, and exportable approval records—translating NIST AI RMF, EU AI Act, ISO 42001, OWASP LLM Top 10, and MITRE ATLAS into executable Python.

**🚀 [Try the Live Demo](https://rai-toolkit.streamlit.app/)** — Assess AI scenarios and generate decision records in under 2 minutes.

**📄 [Portfolio Overview](PORTFOLIO.md)** — Detailed project walkthrough optimized for hiring managers and technical interviewers.

---

The **Frontier AI Risk Assessment Framework** demonstrates how policy, security, and engineering teams can run an intake, score risk, and assign safeguards inside a single workflow. Every safeguard is backed by policy pack citations so compliance reviewers and threat analysts can trace each decision. Built by a former White House NSC policy advisor to show how governance can operate as code, not just documents.

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

**For AI-Powered Analysis:** Set your OpenAI API key to enable intelligent form auto-fill:
```bash
export OPENAI_API_KEY="sk-..."  # Or enter directly in the app UI
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

Try the live app to:
- **Use AI to auto-fill** risk assessments from plain-language descriptions (NEW)
- Assess AI scenarios with the risk calculator
- View 15+ triggered safeguards for high-risk scenarios
- Download Decision Records as markdown files
- Explore governance analytics with 8+ interactive visualizations

### Deploy Your Own Instance

Fork and deploy your own instance for free in under 5 minutes:

1. Fork this repository to your GitHub account
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud) and sign up
3. Click "New app" and select:
   - Repository: `your-username/rai-toolkit`
   - Branch: `main`
   - Main file: `project1_risk_framework/app.py`
4. Click "Deploy"

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for detailed deployment guides (Docker, Heroku, AWS, etc.).

### Working from the hosted sandbox

If you are collaborating through the coding assistant's sandbox environment and want to move the repository to your own machine, follow the export instructions in [`docs/ACCESSING_SANDBOX.md`](docs/ACCESSING_SANDBOX.md). The guide walks through creating a `git bundle`, copying it out of the container, and pushing the history to your GitHub remote.

## 60-Second Tour for Recruiters

**What this demonstrates:** Translating AI governance policy into executable code—risk triage, safeguard assignment, and audit-ready decision records.

**Start here:**
1. **[Live Demo](https://rai-toolkit.streamlit.app/)** (2 min) — Enter "healthcare chatbot" scenario → see 15+ safeguards trigger with policy citations → download Decision Record
2. **[Healthcare Case Study](docs/case_studies/01_healthcare_chatbot.md)** (3 min) — Critical-tier assessment walkthrough showing PHI protection, adversarial testing, human oversight
3. **[Framework Crosswalks](docs/crosswalks/)** (1 min skim) — How safeguards map to NIST AI RMF, EU AI Act, ISO 42001, OWASP LLM Top 10, MITRE ATLAS
4. **Code deep-dive** (5 min) — [`common/utils/risk_engine.py`](common/utils/risk_engine.py) shows transparent scoring logic; [`common/policy_packs/`](common/policy_packs/) shows YAML-encoded safeguards with policy references

**Skills on display:** Python (Streamlit, pytest), policy-as-code design, threat modeling, cross-functional communication (policy ↔ engineering), CI/CD (GitHub Actions).

## Built with AI Coding Assistance

This entire project was **vibecoded**—built iteratively using AI coding assistants (Claude, Cursor) to rapidly prototype, debug, and refine. Rather than spending weeks on boilerplate, I focused on governance logic, threat modeling, and user experience while AI handled scaffolding, test generation, and documentation formatting.

**Why this matters for hiring:**
- **Experimental mindset:** I treat AI as a force-multiplier, not a replacement—using it to explore ideas faster and iterate on feedback loops
- **Maximizing frontier capabilities:** Just as I design red-team frameworks for frontier AI at 2430 Group, I leverage frontier AI for my own workflows
- **Transparent about tooling:** Modern security/governance work requires understanding AI's capabilities and limitations firsthand; building with AI teaches both
- **Outcome-focused:** 6 policy frameworks, 60+ safeguards, 3 case studies, full CI/CD—shipped in days, not months

**The workflow:** Plain-language intent → AI generates scaffolding → I refine logic/policy accuracy → AI writes tests/docs → iterate. This is how governance-as-code should operate: rapid experimentation, transparent decision logic, and continuous validation.

Now, the app uses AI to **autofill risk assessments** from plain-language descriptions—meta, but fitting.

## How Project 1 Operates

1. **AI-powered scenario parsing (NEW):** Paste a plain-language use case description → OpenAI API analyzes it → get suggested risk modifiers with reasoning → review and approve → auto-fill the form. Meta-governance: AI built this tool, now AI helps *you* assess AI.
2. **Scenario intake:** Reviewers capture a plain-language description, the autonomy level, and flags such as PII or customer-facing exposure.
3. **Risk scoring:** A transparent additive model converts the inputs into a tier (Low/Medium/High/Critical) that teams can defend in interviews and audit readouts.
4. **Policy selection:** YAML policy packs encode safeguards from recognized frameworks (e.g., NIST AI RMF, EU AI Act). Conditions inside each control determine whether it applies to the submitted scenario.
5. **Decision Record export:** The Streamlit UI and shared exporter produce a Markdown file summarizing the risk tier, selected controls, and review ownership so the outcome can be filed in a ticketing system.

Read the methodology deep dive in `docs/methodology_project1.md` for scoring rationale and governance trade-offs. A plain-language walkthrough of every file—written for early-career coders—is available in `docs/FILE_OVERVIEW.md`.

### Real-World Case Studies

See [`docs/case_studies/`](docs/case_studies/) for detailed analyses of three realistic scenarios:

1. **[Healthcare Patient Support Chatbot](docs/case_studies/01_healthcare_chatbot.md)** — Critical tier (score: 12) with 15 triggered safeguards spanning PHI protection, adversarial testing, and human oversight
2. **[Internal Code Copilot](docs/case_studies/02_internal_code_copilot.md)** — Low tier (score: 0) demonstrating appropriate de-escalation for internal, human-reviewed tooling
3. **[AI-Powered Hiring Platform](docs/case_studies/03_hiring_assessment_tool.md)** — Critical tier (score: 9) showing employment AI's unique risk profile under EU AI Act and identifying framework enhancement opportunities

## Framework Crosswalks

Stakeholders often ask how safeguards align with familiar standards. Use the illustrative briefs in `docs/crosswalks/` when tailoring communications for:

- **NIST AI RMF** — Mapping governance-as-code safeguards to the Govern/Map/Measure/Manage functions.
- **EU AI Act** — Showing how triage, documentation, and human oversight translate to Article 6 risk obligations.
- **ISO/IEC 42001** — Framing controls in management system language for audit preparation.
- **U.S. OMB AI Policy** — Explaining inventory, impact assessment, and accountability expectations for federal teams.
- **OWASP LLM Top 10** — Connecting modifiers to security mitigations for application security audiences.
- **MITRE ATLAS** — Linking safeguards to adversarial tactics for threat intelligence partners.

Each crosswalk keeps the "illustrative" caveat front-and-center; confirm requirements with counsel or compliance before treating them as canonical.

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

## About Henry

I'm an AI security strategist and former White House NSC policy advisor who translates frontier‑tech risk into executive action. I've built cross‑government coalitions (12 agencies, 30+ international partners) against spyware, run intelligence downgrades that protected U.S. elections, and now design red‑team frameworks for frontier systems at 2430 Group. 

I built this RAI Toolkit to demonstrate governance‑as‑code in practice: quick risk triage, safeguards with policy citations, and exportable decision records that bridge policy, security, and engineering teams.

**Connect:** [henryappel@gmail.com](mailto:henryappel@gmail.com) | Washington, DC

**Background:** West Wing aide & intelligence policy advisor at the NSC (2023–2024); IC analyst/operator at ODNI/NCTC (2018–2025) across PRC/DPRK cyber, ransomware, spyware, and illicit tech transfers; M.A. Security Studies, Georgetown.

## Contact

Questions about responsible use or potential improvements can be raised via issues. Sensitive disclosures should follow the contact guidance in `SECURITY.md`.
