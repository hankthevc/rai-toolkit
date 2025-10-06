# Frontier AI Risk Assessment Framework

**Key Judgments**
- Streamlit workflow turns policy packs and the transparent risk heuristic into an interview-ready demo.
- Every safeguard is sourced from the governance-as-code YAML packs with traceable authorities and clauses.
- Decision Records export to Markdown so executives can review approvals alongside evidence collection plans.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run project1_risk_framework/app.py
```

> Tip: use `streamlit run ... --server.headless true` when hosting in CI or Streamlit Cloud.

## Demo Script (≈90 seconds)
1. Launch the app and point to a scenario that processes healthcare data, serves customers, and has partial autonomy.
2. Toggle the high-stakes, customer-facing, and PII switches; set autonomy to at least 2; select Healthcare and the Cyber modifier.
3. Highlight the risk tier call-out and narrate the contributing factors so reviewers see how the additive score works.
4. Expand one of the safeguards to show the authority, clause, evidence expectations, and ATLAS/OWASP mappings.
5. Enter owner and approver names, then download the Markdown Decision Record to demonstrate audit-ready exports.

## Architecture Notes
- **Form Inputs:** Streamlit widgets capture the scenario, modifiers, and accountability routing in a single form submit.
- **Risk Engine:** Reuses `common.utils.risk_engine` so the same heuristic powers tests and future CLI tooling.
- **Policy Selection:** The UI loads YAML packs through `common.utils.policy_loader` to keep logic in one place.
- **Decision Record:** `common.utils.exporters.build_decision_record` ensures consistent Markdown output across channels.

## Methods & Limits
- Additive scoring is intentionally conservative and interview-friendly; calibrate with production incident data over time.
- Policy packs are illustrative and not legal advice—validate every clause before operational use.
- Scenarios without matching controls should trigger a governance review rather than an auto-approval.

## Framework Crosswalk References
- **docs/methodology_project1.md** — Full scoring rationale, policy selection logic, and versioning workflow.
- **docs/crosswalks/** — Illustrative briefs translating safeguards into NIST AI RMF, EU AI Act, ISO/IEC 42001, U.S. OMB policy, OWASP LLM Top 10, and MITRE ATLAS language for stakeholder briefings.
- **docs/LEARNING_JOURNAL.md** — Ongoing lessons that capture why weights or pack conditions change across releases.

## How Responsible AI Teams Use This Tool
- **Risk Intake:** Product pods submit upcoming launches through the Streamlit form so governance teams can consistently capture scenario variables, autonomy levels, and modifiers tied to sector-specific threats.
- **Heuristic Triage:** The additive score highlights which launches escalate to senior review, giving TPMs and policy leads a defensible starting point while they collect deeper evidence.
- **Safeguard Mapping:** The policy packs translate the scenario into named controls across NIST AI RMF, EU AI Act, ISO/IEC 42001, OWASP LLM Top 10, and MITRE ATLAS, enabling cross-functional stakeholders to speak a common language during sign-off meetings.
- **Decision Record Export:** Owner and approver inputs flow into the Markdown report so legal, security, and product leadership can document approvals, required mitigations, and next-review dates inside existing GRC systems.
- **Feedback Loop:** Governance teams annotate the exported record with production learnings, then version the YAML packs to keep safeguards aligned with new regulations and attack patterns.

## Responsible Use
This demonstration is defensive and non-binding. Validate safeguards with legal, privacy, and security teams before launch.
