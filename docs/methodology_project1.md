# Frontier AI Risk Assessment Methodology

**Key Judgments**
- The additive heuristic intentionally over-weights high-stakes, customer-facing, and safety-critical modifiers so governance teams bias toward escalation when uncertainty exists.
- YAML policy packs act as the single source of truth for safeguards; scenario metadata simply toggles which clauses become mandatory for the review packet.
- Decision Records serve as the feedback loop—annotated exports inform future weight adjustments and pack revisions so the framework matures with real incidents.

## Methods

### Intake Variables
The Streamlit form captures seven variables that map to the policy logic:

| Variable | Description | Values | Governance Rationale |
| --- | --- | --- | --- |
| Scenario | Plain-language description of the use case | Text | Anchors human review and supports incident tagging later |
| Contains PII | Whether the system processes personally identifiable information | Checkbox | Privacy regulations (GDPR/OMB) elevate review expectations |
| Customer-facing | Exposure to external users or customers | Checkbox | Triggers transparency, notice, and abuse-prevention controls |
| High-stakes | Potential to materially harm safety, rights, or critical services | Checkbox | Aligns with EU AI Act / NIST AI RMF "high-risk" thresholds |
| Autonomy Level | Degree of automated decision-making (0–3) | Slider | Higher autonomy demands human-in-the-loop safeguards |
| Sector | Domain classification | Dropdown | Sector-specific compliance (healthcare, finance, critical infrastructure) |
| Modifiers | Threat amplifiers (Bio, Cyber, Disinformation, Children) | Multiselect | Maps to MITRE ATLAS / OWASP controls for specialized hardening |
| Owner / Approver | Accountability routing | Text inputs | Required for auditability and decision sign-off |

### Risk Scoring Heuristic

The risk engine converts the form data into a numeric score, then maps that score to a tier.

```
score = 0
if contains_pii: score += 2
if customer_facing: score += 2
if high_stakes: score += 3
score += autonomy_level (0-3)
for modifier in modifiers:
    if modifier in {"Bio", "Cyber"}: score += 2
    elif modifier in {"Disinformation", "Children"}: score += 1
if sector in {"Healthcare", "Finance", "Critical Infrastructure"}: score += 1
```

Tier thresholds:

- **Low:** score ≤ 2
- **Medium:** 3 ≤ score ≤ 5
- **High:** 6 ≤ score ≤ 8
- **Critical:** score ≥ 9

**Why this works:** the model is explainable in interviews, prioritizes known high-risk vectors, and gives policy leads a defensible triage signal within minutes. The additive weights also align with public regulatory narratives—e.g., EU AI Act Article 6 and NIST AI RMF Core "Govern" and "Map" functions emphasize data sensitivity, autonomy, and safety impact.

### Policy Pack Selection

Each YAML control lists the frameworks it represents, the expected evidence, and a `when` block. During scoring, the loader evaluates the control conditions against the scenario metadata and the derived tier. For example:

```yaml
when:
  any:
    - high_stakes: true
    - tier_in: ["High", "Critical"]
    - modifiers_contains: "Cyber"
```

A control fires when *any* of the listed criteria match. Condition keys supported today include:

- `high_stakes`, `customer_facing`, `contains_pii`
- `autonomy_at_least`
- `tier_in`
- `sector_in`
- `modifiers_contains`

This approach keeps policy intent encoded in data instead of Python logic, enabling non-engineering governance owners to update safeguards through pull requests.

### Decision Record Export

When reviewers click **Download Decision Record (.md)** the exporter builds a Markdown file containing:

1. Scenario summary and submission timestamp
2. Risk score, tier, and contributing factors
3. Structured table of safeguards with authority, clause, and evidence notes
4. Owner, approver, and next-review date placeholders
5. Safety reminder noting the illustrative nature of mappings

The record gives GRC teams an auditable artifact ready for ticketing systems or executive briefings.

## False Positives vs. False Negatives

- **False Positives (over-escalation):** Likely when the scenario is customer-facing but low autonomy. The team accepts this cost because follow-up reviews are cheaper than remediating an under-governed launch. Reviewers can waive controls with a documented justification in the Decision Record.
- **False Negatives (missed risk):** Most plausible when the scenario is internal-only yet leverages sensitive training data. Mitigation: add future modifiers for model provenance, red-team coverage, and data residency once those packs are authored.

## Limits & Planned Improvements

- **Regulatory freshness:** Pack clauses are illustrative. Before production deployment, integrate an approval workflow requiring legal/privacy validation of every reference.
- **Quantitative calibration:** Replace fixed weights with data-driven scoring using historical incidents and post-incident reviews once available.
- **Context depth:** Support richer scenario metadata (model architecture, deployment geography, user cohort) to unlock finer-grained controls.
- **Dynamic evidence tracking:** Extend the exporter to ingest evidence links or checklist statuses so Decision Records double as readiness trackers.

## Policy Pack Versioning

1. Packs live in `common/policy_packs/` and must conform to `common/schema/policy_pack.schema.json`.
2. Updates proceed via pull requests referencing the relevant incident, regulation, or audit finding.
3. The changelog captures pack revisions, and `docs/LEARNING_JOURNAL.md` logs why the update occurred.
4. Every pack header reminds readers the mappings are illustrative and require counsel review.
5. Git tags (starting with `v0.1`) snapshot the state of the packs so downstream teams can pin to a known baseline.

## Feedback Loop

Governance leads should annotate exported Decision Records with observed gaps, then open issues tagged `area:docs` and `area:app`. Accepted changes lead to new policy pack versions and potential weight adjustments, keeping the framework aligned with evolving threat intelligence and regulatory expectations.

## Responsible Use Reminder

This methodology is provided for defensive, educational purposes. Validate conclusions with legal, privacy, and security partners before treating any safeguard as binding policy.
