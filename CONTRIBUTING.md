# Contributing Guide

## Key Judgments
- This project treats responsible AI governance as code. Contributions should strengthen transparency, accountability, or safety.
- Maintain professional rigor: tests pass, documentation is updated, and policy references are traceable.

## Getting Started
1. Create an issue outlining the proposed change. Label it with the relevant area (e.g., `area:app`, `area:docs`).
2. Fork the repository and create a branch using the agreed convention (e.g., `feat/project-component`).
3. Set up your environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Run `pytest` before submitting a pull request.

## Pull Requests
- Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.
- Keep PRs focused. Include a “Design Notes” section summarizing decisions and tradeoffs.
- Link to the relevant issue and describe testing performed.
- Ensure governance artifacts (policy packs, decision records) remain non-actionable and defensive.

## Code Style
- Python: format with `black`, lint with `ruff`, and organize imports with `isort`.
- YAML/JSON: keep structures readable with comments noting illustrative mappings.
- Add concise comments where policy logic or scoring thresholds are defined.

## Community Expectations
- Respect privacy: do not commit sensitive data.
- Collaborate openly, cite authoritative sources, and document assumptions.

Thank you for supporting responsible AI governance-as-code.
