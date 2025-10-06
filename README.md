# rai-toolkit

**Key Judgment:** Responsible AI governance-as-code. Risk assessment, safeguards with policy citations, and exportable approval records.

The Frontier AI Risk Assessment Framework (Project 1) demonstrates how policy, security, and engineering teams can run an intake, score risk, and assign safeguards inside a single workflow. Every safeguard is backed by an illustrative policy pack citation so compliance reviewers and threat analysts can trace each decision.

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

### Working from the hosted sandbox

If you are collaborating through the coding assistant’s sandbox environment and want to move the repository to your own machine, follow the export instructions in [`docs/ACCESSING_SANDBOX.md`](docs/ACCESSING_SANDBOX.md). The guide walks through creating a `git bundle`, copying it out of the container, and pushing the history to your GitHub remote.

> Screenshot placeholder: add once the Streamlit app is live.

## How Project 1 Operates

1. **Scenario intake:** Reviewers capture a plain-language description, the autonomy level, and flags such as PII or customer-facing exposure.
2. **Risk scoring:** A transparent additive model converts the inputs into a tier (Low/Medium/High/Critical) that teams can defend in interviews and audit readouts.
3. **Policy selection:** YAML policy packs encode safeguards from recognized frameworks (e.g., NIST AI RMF, EU AI Act). Conditions inside each control determine whether it applies to the submitted scenario.
4. **Decision Record export:** The Streamlit UI and shared exporter produce a Markdown file summarizing the risk tier, selected controls, and review ownership so the outcome can be filed in a ticketing system.

Read the methodology deep dive in `docs/methodology_project1.md` for scoring rationale and governance trade-offs. A plain-language walkthrough of every file—written for early-career coders—is available in `docs/FILE_OVERVIEW.md`.

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

- **Current milestone:** Project 1 — Frontier AI Risk Assessment Framework (v0.1 workstream in progress).
- **Next steps:** Finish documentation polish, capture demo artifacts, and prepare for a public tag once reviewers confirm the workflow meets responsible AI governance expectations.

## Contact

Questions about responsible use or potential improvements can be raised via issues. Sensitive disclosures should follow the contact guidance in `SECURITY.md`.
