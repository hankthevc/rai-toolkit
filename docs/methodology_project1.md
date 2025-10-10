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
3. The changelog captures pack revisions and documents why each update occurred.
4. Every pack header reminds readers the mappings are illustrative and require counsel review.
5. Git tags (starting with `v0.1`) snapshot the state of the packs so downstream teams can pin to a known baseline.

## Feedback Loop

Governance leads should annotate exported Decision Records with observed gaps, then open issues tagged `area:docs` and `area:app`. Accepted changes lead to new policy pack versions and potential weight adjustments, keeping the framework aligned with evolving threat intelligence and regulatory expectations.

## Stop-Ship Rules

Certain risk configurations should **halt deployment** until specific safeguards are implemented and verified. The following rules represent hard gates:

### Critical Tier Stop-Ships
**Rule 1: Critical + PII + Irreversible Decisions**
- **Trigger:** Risk tier = Critical AND processes PII AND decision reversibility = Irreversible
- **Required before launch:**
  - Legal review by privacy counsel
  - Data Protection Impact Assessment (DPIA) completed
  - Appeals/redress mechanism documented and tested
  - Executive sign-off from VP-level or above
- **Rationale:** GDPR Art. 22, EU AI Act high-risk designation

**Rule 2: Critical + Protected Populations**
- **Trigger:** Risk tier = Critical AND protected_populations includes Children, Elderly, or People with Disabilities
- **Required before launch:**
  - Accessibility audit (WCAG 2.1 AA minimum for digital systems)
  - Bias testing across demographic groups with documented results
  - Civil rights stakeholder consultation
  - Enhanced consent mechanisms reviewed by legal
- **Rationale:** ADA, Fair Housing Act, COPPA (for children)

**Rule 3: Critical + High Dual-Use Risk**
- **Trigger:** Risk tier = Critical AND dual_use_risk = High
- **Required before launch:**
  - Export control classification obtained (EAR/ITAR review)
  - Adversarial testing / red team engagement
  - Restricted access controls and audit logging
  - Incident response plan reviewed
- **Rationale:** National security, Export Administration Regulations

### High Tier Stop-Ships
**Rule 4: High + Healthcare/Finance Sector**
- **Trigger:** Risk tier = High AND sector in [Healthcare, Finance]
- **Required before launch:**
  - Sector-specific compliance review (HIPAA for healthcare, GLBA for finance)
  - Model risk management documentation (SR 11-7 for finance)
  - Security assessment by sector SMEs
- **Rationale:** Sector-specific regulations, heightened regulatory scrutiny

**Rule 5: High + External API + PII**
- **Trigger:** Risk tier = High AND uses_foundation_model = External API AND contains_pii = True
- **Required before launch:**
  - Vendor contract review for AI-specific terms (data retention, training prohibitions)
  - Data leakage assessment
  - Encryption in transit and at rest verified
  - Data residency requirements documented
- **Rationale:** Supply chain security, data sovereignty

**Rule 6: High + Real-Time Learning**
- **Trigger:** Risk tier = High AND learns_in_production = True
- **Required before launch:**
  - Poisoning attack mitigation strategy documented
  - Model drift monitoring configured
  - Rollback procedures tested
  - Performance degradation thresholds defined
- **Rationale:** MITRE ATLAS AML.T0018, model integrity

### Universal Stop-Ships (All Tiers)
**Rule 7: Synthetic Content Generation**
- **Trigger:** generates_synthetic_content = True (any risk tier)
- **Required before launch:**
  - Watermarking or provenance mechanism implemented (C2PA or equivalent)
  - Disclosure to users per EU AI Act Art. 52
  - Abuse monitoring configured
- **Rationale:** EU AI Act Art. 52, deepfake risks

**Rule 8: Missing Ownership**
- **Trigger:** Owner or Approver fields empty
- **Required before launch:**
  - Assign specific individuals (not teams) as owner and approver
  - Confirm they acknowledge responsibility in writing
- **Rationale:** Accountability, audit trail

### Waiver Process
Stop-ship rules can be waived only with:
1. Written justification documenting why the risk is acceptable
2. Compensating controls that mitigate the specific concern
3. Approval from legal, privacy, security, and executive leadership
4. Documentation added to the Decision Record

## Comprehensive Scoring Table

Below is the complete scoring model including all 16 risk factors with their weights and thresholds:

| Risk Factor | Trigger Condition | Points Added | Cumulative Impact | Governance Rationale |
|-------------|-------------------|--------------|-------------------|---------------------|
| **Core Risk Factors** | | | | |
| Contains PII | `contains_pii = True` | +2 | Privacy regulations | GDPR, CCPA, OMB M-24-10 privacy requirements |
| Customer-Facing | `customer_facing = True` | +2 | External exposure | Transparency obligations, abuse surface |
| High-Stakes | `high_stakes = True` | +3 | Safety/rights impact | EU AI Act Annex III, NIST AI RMF high-risk criteria |
| Autonomy Level 0 | `autonomy_level = 0` | +0 | Suggestion only | Minimal risk - human makes all decisions |
| Autonomy Level 1 | `autonomy_level = 1` | +1 | Human-in-loop | Moderate - requires review before action |
| Autonomy Level 2 | `autonomy_level = 2` | +2 | Human oversight | High - acts with escalation paths |
| Autonomy Level 3 | `autonomy_level = 3` | +3 | Full autonomy | Critical - acts without review |
| Modifier: Bio | `"Bio" in modifiers` | +2 | Biosecurity | Biological threat amplification |
| Modifier: Cyber | `"Cyber" in modifiers` | +2 | Cybersecurity | MITRE ATLAS adversarial ML threats |
| Modifier: Disinformation | `"Disinformation" in modifiers` | +1 | Information integrity | Narrative manipulation risks |
| Modifier: Children | `"Children" in modifiers` | +1 | Child safety | COPPA, enhanced protections |
| Sector: Healthcare | `sector = "Healthcare"` | +1 | Regulated sector | HIPAA, FDA oversight |
| Sector: Finance | `sector = "Finance"` | +1 | Regulated sector | GLBA, model risk management |
| Sector: Critical Infrastructure | `sector = "Critical Infrastructure"` | +1 | National security | CISA designation, heightened review |
| **Extended Risk Factors** | | | | |
| Model Type: Traditional ML | `model_type = "Traditional ML"` | +0 | Lower complexity | Standard ML risks |
| Model Type: LLM | `model_type = "Generative AI / LLM"` | +2 | OWASP LLM Top 10 | Prompt injection, hallucination risks |
| Model Type: Computer Vision | `model_type = "Computer Vision"` | +1 | Adversarial examples | Deepfakes, mis-classification |
| Model Type: Multimodal | `model_type = "Multimodal"` | +2 | Increased attack surface | Cross-modal attacks |
| Model Type: RL | `model_type = "Reinforcement Learning"` | +1 | Reward hacking | Unintended optimization |
| Data Source: Proprietary | `data_source = "Proprietary/Internal"` | +0 | Controlled | Known provenance |
| Data Source: Internet-Scraped | `data_source = "Internet-Scraped"` | +2 | Copyright/bias | Unknown provenance, potential PII |
| Data Source: User-Generated | `data_source = "User-Generated"` | +1 | Poisoning risk | Adversarial data injection |
| Data Source: Third-Party | `data_source = "Third-Party/Vendor"` | +1 | Supply chain | Vendor risk |
| Real-Time Learning | `learns_in_production = True` | +2 | Drift/poisoning | MITRE ATLAS AML.T0018 |
| Cross-Border Data | `international_data = True` | +2 | GDPR/sovereignty | Schrems II, adequacy decisions |
| Explainability: Inherently Interpretable | `explainability_level = "Inherently Interpretable"` | +0 | Transparent | Linear models, decision trees |
| Explainability: Post-hoc | `explainability_level = "Post-hoc Explainable"` | +1 | SHAP/LIME | Moderate interpretability |
| Explainability: Limited | `explainability_level = "Limited Explainability"` | +1 | Complex ensembles | Harder to explain |
| Explainability: Black Box | `explainability_level = "Black Box"` | +2 | GDPR Art. 22 risk | Opaque decision-making |
| Foundation Model: External API | `uses_foundation_model = "External API"` | +2 | Data leakage | OpenAI, Anthropic, etc. |
| Foundation Model: Self-Hosted | `uses_foundation_model starts with "Self-Hosted"` | +1 | Vendor risk (lower) | On-premise but licensed |
| Synthetic Content | `generates_synthetic_content = True AND customer_facing = True` | +2 | EU AI Act Art. 52 | Deepfake disclosure required |
| Dual-Use: Moderate | `dual_use_risk = "Moderate"` | +2 | Weaponization potential | Export controls may apply |
| Dual-Use: High | `dual_use_risk = "High"` | +3 | Export controls | EAR/ITAR review required |
| Irreversible Decisions | `decision_reversible = "Irreversible"` | +3 | No appeals | Autonomous weapons, permanent records |
| Difficult to Reverse | `decision_reversible = "Difficult to Reverse"` | +2 | Costly appeals | Reputation damage |
| Protected Population (each) | Each population in list | +1 to +2 | Vulnerable groups | Children (+2), Elderly (+1), Disabilities (+2), etc. |

### Tier Thresholds (Updated)
- **Low Risk:** score ≤ 2 (minimal safeguards)
- **Medium Risk:** 3 ≤ score ≤ 5 (standard controls)
- **High Risk:** 6 ≤ score ≤ 8 (enhanced review, sector-specific)
- **Critical Risk:** score ≥ 9 (executive approval, stop-ship triggers)

### Example Calculations

**Example 1: Internal Code Copilot**
- Contains PII: No (+0)
- Customer-Facing: No (+0)
- High-Stakes: No (+0)
- Autonomy: Level 0 (+0)
- Sector: General (+0)
- Model Type: LLM (+2)
- **Total: 2 points → Low Risk**

**Example 2: Healthcare Chatbot**
- Contains PII: Yes (+2)
- Customer-Facing: Yes (+2)
- High-Stakes: Yes (+3)
- Autonomy: Level 2 (+2)
- Sector: Healthcare (+1)
- Model Type: LLM (+2)
- Uses External API (+2)
- Protected Population: Elderly (+1)
- **Total: 15 points → Critical Risk**

**Example 3: Automated Loan Decisioning**
- Contains PII: Yes (+2)
- Customer-Facing: Yes (+2)
- High-Stakes: Yes (+3)
- Autonomy: Level 3 (+3)
- Sector: Finance (+1)
- Explainability: Black Box (+2)
- Decision Reversible: Difficult (+2)
- **Total: 15 points → Critical Risk**

## Responsible Use Reminder

This methodology is provided for defensive, educational purposes. Validate conclusions with legal, privacy, and security partners before treating any safeguard as binding policy.
