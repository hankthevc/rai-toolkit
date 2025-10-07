# Building Governance-as-Code: How I Made AI Risk Assessments Auditable

*A technical deep dive into translating compliance frameworks into version-controlled policy packs*

---

## The Problem: Manual Risk Assessments Don't Scale

Six months ago, I watched a senior engineer spend three hours filling out a 47-question Word document to assess whether our new chatbot feature needed legal review. The questions were vague ("Does this use AI?" — define "AI"...), the approval chain was unclear (email the VP... or the Chief Risk Officer?), and the final decision—buried in someone's inbox—would be impossible to defend in an audit.

This wasn't an isolated incident. As AI adoption accelerates, every company faces the same bottleneck: **governance workflows are trapped in spreadsheets, email threads, and tribal knowledge.** When a regulator asks "How did you evaluate this system's compliance with the EU AI Act?", teams scramble to reconstruct decisions from Slack screenshots and meeting notes.

I decided to fix this by treating governance the same way we treat infrastructure: **as version-controlled code.**

---

## Design Principles

Before writing a line of code, I established three constraints that would make this useful beyond a portfolio piece:

### 1. **Transparency Over Black Boxes**
No ML models predicting risk scores. Every point in the risk calculation must be explainable to a non-technical executive or auditor. This ruled out fancy clustering algorithms in favor of a simple additive heuristic:

```python
score = (PII × 2) + (customer_facing × 2) + (high_stakes × 3) 
        + autonomy_level + sector_bump + Σ(modifiers)
```

An intern can defend this math. A neural network? Not so much.

### 2. **Framework Alignment, Not Invention**
Don't create a proprietary compliance standard. Map to frameworks teams already care about:
- **NIST AI RMF** (U.S. federal guidance)
- **EU AI Act** (high-stakes regulatory precedent)
- **ISO/IEC 42001** (management system standard)
- **OWASP LLM Top 10** (security practitioners)
- **MITRE ATLAS** (threat intelligence)
- **U.S. OMB AI Policy** (executive branch requirements)

This gives stakeholders a translation layer: *"Our Critical tier maps to EU AI Act high-risk classification under Article 6."*

### 3. **Audit Trails as a First-Class Feature**
Every assessment must produce a **Decision Record**—a markdown file capturing:
- Who assessed it (Scenario Owner)
- Who approved it (Approver)
- What risk tier was assigned (with score breakdown)
- Which safeguards are mandatory (with policy citations)
- When to re-assess (Next Review Date)

These records slot directly into ticketing systems (Jira, ServiceNow) and survive discovery requests years later.

---

## Architecture: YAML + Pydantic + Jinja

The core insight is that **safeguards are data, not logic.** A policy control shouldn't live in an `if/else` branch—it should be a declarative specification in a YAML file.

### Policy Pack Structure

Each framework gets a YAML file like this (`nist_ai_rmf.yaml`):

```yaml
name: "NIST AI RMF (Illustrative)"
version: "2024-01-01"
controls:
  - id: NIST-GOV-01
    title: "Document accountable owner"
    description: "Assign a named executive accountable for the AI system's governance posture."
    authority: "NIST AI RMF"
    clause: "Govern 1.1 (illustrative)"
    evidence: "Risk charter naming accountable executive and approval date."
    tags: [governance, accountability]
    when:
      tier: ["Medium", "High", "Critical"]
```

The `when` block is the magic. It's a conditional expression evaluated against the scenario's attributes. If a scenario has `tier: "High"`, this control triggers. Simple, testable, version-controllable.

### Validation with JSON Schema

To prevent typos and enforce consistency, every policy pack validates against a JSON Schema:

```json
{
  "type": "object",
  "required": ["id", "title", "description", "authority", "clause", "evidence", "tags", "when"],
  "properties": {
    "when": {
      "type": "object",
      "properties": {
        "tier": {"type": "array", "items": {"type": "string"}},
        "contains_pii": {"type": "boolean"},
        "autonomy_at_least": {"type": "integer", "minimum": 0}
      }
    }
  }
}
```

This catches errors at **authoring time** (CI fails if the YAML is malformed), not runtime (when a legal review is already overdue).

### Pydantic Models for Type Safety

Python's Pydantic library bridges YAML data to type-safe Python objects:

```python
class PolicyControl(BaseModel):
    id: str
    title: str
    description: str
    authority: str
    clause: str
    evidence: str
    tags: List[str]
    when: WhenClause

class WhenClause(BaseModel):
    tier: Sequence[str] | None = None
    contains_pii: bool | None = None
    autonomy_at_least: int | None = Field(default=None, ge=0)
```

If someone fat-fingers `autonomy_at_least: -1`, Pydantic raises a `ValidationError` immediately. No silent failures.

### Decision Record Export with Jinja2

The final piece is templating. Instead of string concatenation hell, I use Jinja2:

```jinja2
# Frontier AI Risk Decision Record

**Scenario Owner:** {{ owner }}  
**Risk Tier:** {{ assessment.tier }}

## Required Safeguards
{% for control in controls %}
### {{ control.title }} ({{ control.authority }})
- **ID:** {{ control.id }}
- **Clause:** {{ control.clause }}
- **Evidence to Capture:** {{ control.evidence }}
{% endfor %}
```

This keeps formatting consistent across UI and CLI flows, and makes it trivial to add new sections (e.g., a "Regulatory Crosswalk" table).

---

## Technical Challenges & Solutions

### Challenge 1: Control Matching Logic

**Problem:** A control with multiple conditions in the `when` clause needs clear semantics. Is it AND or OR?

**Solution:** All conditions within a single `when` block are AND-ed. If you need OR, create multiple controls or expand the `when` syntax:

```yaml
when:
  any:
    - tier: ["High", "Critical"]
    - high_stakes: true
```

This is future work—for v0.1, I kept it simple with implicit AND.

### Challenge 2: Policy Pack Versioning

**Problem:** Safeguards evolve. A control valid in Q1 might be deprecated by Q4. How do teams pin to a known baseline?

**Solution:** Git tags. Each policy pack includes a `version` field. When we finalize a release:

```bash
git tag -a v0.1 -m "Initial policy pack release"
git push --tags
```

Downstream teams can `git checkout v0.1` to freeze their compliance posture. The changelog documents why each pack was revised.

### Challenge 3: False Positives vs. False Negatives

**Problem:** An overly sensitive heuristic triggers 15 safeguards for a low-risk scenario. An overly lenient one misses a high-stakes deployment.

**Solution:** Bias toward false positives (over-escalation). The cost of a follow-up review is ~30 minutes. The cost of an under-governed launch is a lawsuit, regulatory fine, or reputational crisis. The case studies document this tradeoff explicitly:

> *"Low-risk scenarios should get zero mandatory controls. If an internal dev tool triggers governance overhead, the weights are miscalibrated."*

---

## Validation: Three Real-World Case Studies

I validated the framework against realistic scenarios spanning the risk spectrum:

### Case Study 1: Healthcare Chatbot (Critical Tier)

- **Scenario:** Patient support bot processing PHI, customer-facing, high-stakes (medical misinformation)
- **Score:** 12 (PII +2, customer +2, high-stakes +3, autonomy +2, Healthcare sector +1, Cyber modifier +2)
- **Tier:** Critical
- **Controls Triggered:** 15 (spanning NIST, EU AI Act, ISO 42001, OWASP, MITRE, OMB)

**Key Insight:** Healthcare + customer-facing creates compounding risk that requires defense-in-depth. Executive accountability (3 frameworks), adversarial testing (3 frameworks), and human oversight (EU AI Act) all mandatory.

### Case Study 2: Internal Code Copilot (Low Tier)

- **Scenario:** AI coding assistant for 12 DevOps engineers, internal-only, suggestion-based (autonomy 0)
- **Score:** 0
- **Tier:** Low
- **Controls Triggered:** 0

**Key Insight:** Zero mandatory controls is the **correct outcome.** Governance should be proportional. Internal tooling with human review doesn't need conformity assessments or third-party audits.

### Case Study 3: Hiring AI (Critical Tier + Policy Gaps)

- **Scenario:** Resume screening + video interview analysis for 200+ enterprise clients
- **Score:** 9 (PII +2, customer +2, high-stakes +3, autonomy +2)
- **Tier:** Critical
- **Controls Triggered:** 11

**Key Insight:** Employment decisions are high-risk even without healthcare/finance sector flags. **But** the analysis surfaced two gaps:

1. **Missing "Fairness" modifier:** Hiring bias is the primary risk, but the framework doesn't weight it. Need `+2` fairness modifier and new controls like disparate impact testing.

2. **No "Employment" sector:** Unlike Healthcare or Finance, hiring doesn't get a sector bump. Should add employment-specific pack with EEOC/GDPR Article 22 controls.

Both logged as GitHub issues for v0.2.

---

## Lessons Learned

### 1. Governance Teams Want Simplicity, Not Sophistication

I initially built a Bayesian network to model risk dependencies ("If PII AND customer-facing, multiply by 1.5x..."). It was elegant. It was also impossible to explain in a board meeting.

The additive model won because a VP can see `score = 2 + 2 + 3 + 2 = 9` and immediately understand why it's Critical.

### 2. "Illustrative" Is a Feature, Not a Bug

Every policy pack header says:

> *Illustrative mapping for interview-ready demos. Validate clauses with your governance and legal teams.*

This sounds like a cop-out, but it's essential. I'm not a lawyer, and companies have jurisdiction-specific obligations (GDPR vs. CCPA, EU AI Act vs. U.S. state law). The framework provides a **starting point**, not legal advice.

Trying to be "production-ready" without counsel review would be irresponsible and create liability.

### 3. The Test Suite Is Documentation

Each test file tells a story:

```python
def test_risk_score_additive_nature():
    """Test that all factors are correctly additive."""
    inputs = RiskInputs(
        contains_pii=True,  # +2
        customer_facing=True,  # +2
        high_stakes=True,  # +3
        autonomy_level=3,  # +3
        sector="Healthcare",  # +1
        modifiers=["Cyber", "Bio"],  # +2 +2
    )
    assessment = calculate_risk_score(inputs)
    
    assert assessment.score == 15
    assert assessment.tier == "Critical"
```

This test documents the scoring logic better than prose. New contributors read the tests to understand the heuristic.

### 4. Analytics Drive Policy Improvements

The analytics dashboard isn't just eye candy—it surfaces patterns:

- **Tier distribution:** If 80% of assessments are Critical, the weights are too aggressive
- **Modifier frequency:** If "Cyber" appears in 90% of scenarios, it should be a checkbox, not a modifier
- **Control coverage:** If NIST-GOV-01 (executive accountability) triggers in every Critical scenario, maybe it should auto-apply at that tier

Governance-as-code enables the same iterative improvement loop as software: ship, measure, refine.

---

## What's Next

### Short-Term (v0.2)

1. **Add "Fairness" modifier** (+2 weight) with controls for:
   - Disparate impact analysis (EEOC 80% rule)
   - Explainability mechanisms (GDPR Article 22)
   - Regular third-party bias audits

2. **Create `employment_ai.yaml` policy pack** with sector-specific controls

3. **Improve `when` clause syntax** to support OR conditions and threshold ranges

### Medium-Term (v0.3)

4. **Quantitative calibration:** Replace fixed weights with data-driven scoring using historical incidents (requires production deployment + telemetry)

5. **Evidence tracking:** Extend Decision Records to link to Jira tickets, test reports, and approval emails

6. **API layer:** Expose risk assessment as a REST API so CI/CD pipelines can gate deployments:

   ```bash
   curl -X POST /api/assess \
     -d '{"contains_pii": true, "autonomy_level": 2}' \
     | jq '.tier'
   # "High"
   ```

### Long-Term (v1.0)

7. **Dynamic policy packs:** Load controls from a database instead of YAML files, enabling governance teams to update safeguards without code changes

8. **Multi-jurisdiction support:** Different control sets for EU vs. U.S. vs. California deployments

9. **Incident feedback loop:** When an AI system causes harm, retroactively assess it to tune weights ("This Low tier scenario caused a privacy breach → increase PII weight")

---

## Why This Matters for AI Safety

Every week, I see startups ship customer-facing AI with zero governance oversight. Not because they're reckless—because **the default path is to do nothing.**

There's no "Create React App" for responsible AI. No scaffold that says "Here's a sensible risk assessment workflow, customize it for your domain."

This toolkit is a stake in the ground: **Governance can be as version-controlled, testable, and iterative as infrastructure.**

If 100 teams fork this repo, adapt the policy packs to their sectors, and commit the Decision Records alongside their code, we'll collectively raise the floor for AI safety.

And when the next regulatory audit asks "How did you know this system needed human oversight?", the answer won't be "Um, we discussed it in a meeting." It'll be:

> *"We assessed it with our governance-as-code framework. Risk tier: High. Triggered EU AI Act Article 14. Here's the Decision Record with the CAIO's approval signature and the test report showing our override mechanism works. Next review is in 90 days."*

That's the future I'm building toward.

---

## Try It Yourself

**🚀 Live Demo:** [https://rai-toolkit.streamlit.app/](https://rai-toolkit.streamlit.app/)

**GitHub:** [github.com/hankthevc/rai-toolkit](https://github.com/hankthevc/rai-toolkit)

**Case Studies:** Start with the [Healthcare Chatbot](https://github.com/hankthevc/rai-toolkit/blob/main/docs/case_studies/01_healthcare_chatbot.md) to see a full Critical-tier assessment

**Questions/Feedback:** Open an issue or reach me at [hankthevc@users.noreply.github.com](mailto:hankthevc@users.noreply.github.com)

---

## Acknowledgments

This work builds on public frameworks from NIST, EU AI Office, ISO/IEC, OWASP, MITRE, and U.S. OMB. All policy mappings are illustrative—validate with legal counsel before production use.

Special thanks to the AI safety research community for elevating governance beyond "check the box" compliance into a discipline that deserves the same rigor as security or reliability engineering.

---

*Tags: #AIGovernance #ResponsibleAI #AIEthics #GovernanceAsCode #Streamlit #Python #NIST #EUAIAct #ISO42001*

