# File-by-File Tour of rai-toolkit

*Audience: junior-high students who are beginning to code and want a friendly walkthrough of this repository.*

## How to Use This Guide

This document is written in plain language to help you understand what every file and folder in `rai-toolkit` does. Think of the repository as a well-organized binder for a school project about keeping AI systems safe and responsible. Each tab in the binder has a job. We will move from the front cover (top-level files) to the inside sections (code, data, and tests) and finish with the automated helpers.

Along the way, you will see three ideas repeated:

- **Governance-as-code:** Important safety rules are saved as YAML files so teams can version and review them the same way they review code.
- **Transparency:** The risk engine uses simple math so anyone can explain why a scenario is labeled Low, Medium, High, or Critical.
- **Audit trails:** Every decision can be exported as a Markdown report that lists the reviewer, approver, and the safety controls they agreed to.

## Top-Level Files (The Front Cover)

- **`README.md`** – This is the welcome page. It explains the purpose of the project, how to run the Streamlit app, what the main workflow looks like, and where to find more detail. Recruiters, engineers, and compliance officers read this first to understand why the toolkit matters.
- **`LICENSE`** – A short legal note that says the code uses the MIT License. It lets other people know they can use and adapt the project while giving credit to the author.
- **`SECURITY.md`** – Instructions for reporting security issues privately. Imagine a student alerting a teacher before a classroom problem spreads—this file sets that expectation.
- **`CODE_OF_CONDUCT.md`** – Defines how contributors should behave. It keeps collaboration respectful and inclusive, much like classroom rules posted on the wall.
- **`CONTRIBUTING.md`** – A guide for anyone who wants to add code or documentation. It tells them how to set up their environment, how to run tests, and how to write good pull requests.
- **`CHANGELOG.md`** – A running list of project updates. Each entry summarizes what changed so reviewers can track progress over time.
- **`requirements.txt`** – A list of Python packages the project depends on, such as Streamlit and PyYAML. Installing these packages ensures your environment matches the one used by the project maintainers.
- **`pyproject.toml`** – Configuration for tools that format and lint the code (Black, Ruff, and isort). This file keeps the code style consistent.
- **`.pre-commit-config.yaml`** – Optional automation that runs style checks before every commit. It helps catch small issues early.
- **`.gitignore`** – Lists files and folders Git should ignore, such as virtual environments and compiled bytecode.
- **`docs/LEARNING_JOURNAL.md`** – Captures lessons learned after each pull request. It mirrors the reflection pages you might write after a science lab.
- **`docs/methodology_project1.md`** – Explains the risk scoring math, the guardrails used to select policy controls, and known limitations. It is the “Methods” chapter of the toolkit.
- **`docs/crosswalks/`** – A folder of short guides that translate the safeguards into the language of NIST AI RMF, EU AI Act, ISO/IEC 42001, U.S. OMB policy, OWASP LLM Top 10, and MITRE ATLAS. Each guide is labeled “illustrative” because lawyers and compliance officers must review the mappings.
- **`docs/FILE_OVERVIEW.md`** – This document. It guides new readers through the whole repo in everyday language.

## `.github/` Folder (Community and Automation Tab)

- **`.github/workflows/ci.yml`** – A GitHub Actions workflow that runs `pytest -q` every time someone opens a pull request. Think of it as an automatic spelling and grammar check, but for code behavior.
- **`.github/PULL_REQUEST_TEMPLATE.md`** – A form contributors fill out when proposing changes. It prompts them to confirm tests, documentation updates, and safety considerations.
- **`.github/ISSUE_TEMPLATE/bug_report.md`** – Helps reporters describe bugs clearly: what happened, what they expected, and steps to reproduce the issue.
- **`.github/ISSUE_TEMPLATE/feature_request.md`** – Captures new ideas with space for expected benefits, risk signals, and success criteria.

These templates keep the conversation structured so busy reviewers can quickly understand what is being asked and why it matters.

## `common/` Folder (Shared Building Blocks Tab)

The `common` directory holds reusable pieces that any future project in the toolkit can share.

### Subfolder: `common/policy_packs/`

Each YAML file in this folder represents a “policy pack.” A policy pack is a set of safeguards mapped to recognizable frameworks. The comment at the top of each file reminds readers that the mappings are illustrative and not legal advice.

- **`nist_ai_rmf.yaml`** – Controls inspired by the NIST AI Risk Management Framework, focusing on governance, measurement, and incident response.
- **`eu_ai_act.yaml`** – Safeguards aligned with the draft EU AI Act, such as transparency notices and conformity assessments.
- **`iso_42001.yaml`** – References the ISO/IEC 42001 management system standard for AI. It highlights documentation, monitoring, and leadership accountability.
- **`owasp_llm_top10.yaml`** – Flags security controls from the OWASP Large Language Model Top 10, emphasizing prompt injection defenses and misuse monitoring.
- **`mitre_atlas.yaml`** – Links to MITRE ATLAS adversary behaviors. It focuses on threat intelligence, red-teaming, and anomaly detection.
- **`us_omb_ai_policy.yaml`** – Illustrates U.S. Office of Management and Budget AI policy guidance, such as registration and risk review boards.

Each control inside these files includes:

- An `id`, `title`, and `description` to explain the safeguard.
- `authority` and `clause` fields showing where the requirement comes from.
- `tags` and optional mappings to frameworks like MITRE ATLAS IDs.
- A `when` section that describes the conditions for applying the control (for example, `contains_pii: true`).

### Subfolder: `common/schema/`

- **`policy_pack.schema.json`** – A JSON Schema that defines the expected structure for each policy pack. If someone accidentally forgets a field or mistypes a value, the schema will catch the mistake.

### Subfolder: `common/utils/`

- **`__init__.py`** – Marks the folder as a Python package so other modules can import from it.
- **`policy_loader.py`** – Functions that read policy packs from disk, validate them against the schema, and filter controls based on scenario inputs.
- **`risk_engine.py`** – Implements the additive scoring model. It awards points for risk factors like PII, customer exposure, high-stakes decisions, autonomy levels, and modifiers such as “Cyber” or “Bio.” The total score maps to a tier: Low (0-2), Medium (3-5), High (6-8), or Critical (9+).
- **`exporters.py`** – Uses Jinja templates to build Markdown Decision Records. These records list the scenario summary, risk tier, selected controls, and who approved the decision.

Together, these utilities form the core logic that powers the Streamlit app and any future command-line tools.

## `project1_risk_framework/` Folder (The Streamlit App Tab)

- **`app.py`** – The Streamlit application. It presents a form where reviewers enter the scenario details (description, PII, customer-facing, high-stakes, autonomy level, sector, and modifiers). When the user presses Submit, the app:
  1. Calls the risk engine to compute a score and tier.
  2. Loads policy packs and filters the controls that match the scenario.
  3. Displays the selected safeguards with their authorities and clauses.
  4. Provides a button to download the Markdown Decision Record.

  Inline comments explain key design choices, such as caching policy packs for faster loading and keeping the workflow immutable after submission.

- **`README.md`** – Project-specific documentation. It describes how to run the app, what to demo during a 90-second walkthrough, architecture notes, and responsible-use guidance. It is tailored for reviewers who want to see how Project 1 works without reading the entire repository.

## `tests/` Folder (Quality Assurance Tab)

Automated tests ensure that policy packs stay valid and the risk engine behaves as expected.

- **`tests/conftest.py`** – Provides shared fixtures for loading policy packs during tests.
- **`tests/test_policy_packs.py`** – Verifies that more than three policy packs exist and that required keys are present in each control. This keeps governance data from drifting into an unusable state.
- **`tests/test_risk_engine.py`** – Creates a clearly risky scenario (PII + customer-facing + high-stakes + high autonomy + Cyber modifier + healthcare sector). The test asserts that the risk tier is High or Critical.

## Hidden Helpers

Some files are not immediately visible but keep the project running smoothly.

- **`common/__init__.py`** – Marks the `common` directory as a package.
- **`common/utils/__init__.py`** – Makes it easy to import utilities with short paths.

These small files act like table-of-contents cards, letting Python know where to find things.

## Putting It All Together

When someone uses the toolkit, the flow looks like this:

1. They read `README.md` to understand the mission and follow the Quickstart instructions to install dependencies from `requirements.txt`.
2. They launch the Streamlit app in `project1_risk_framework/app.py`.
3. The app calls `common/utils/risk_engine.py` to compute the risk tier.
4. The app loads policy packs from `common/policy_packs/` via `common/utils/policy_loader.py`, using `common/schema/policy_pack.schema.json` to validate the data.
5. After picking the right safeguards, the app hands everything to `common/utils/exporters.py` to build a Markdown Decision Record.
6. Tests in the `tests/` folder make sure nothing breaks as the project grows.
7. GitHub Actions (`.github/workflows/ci.yml`) runs those tests automatically on every pull request to maintain trust in the toolkit.

By saving governance logic, documentation, and automation side by side, `rai-toolkit` shows that responsible AI oversight can be treated like an engineering discipline. Every file supports the same goal: helping teams explain their decisions, cite trusted frameworks, and keep the public safe.
