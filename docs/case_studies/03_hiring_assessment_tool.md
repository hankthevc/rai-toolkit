# Case Study 3: AI-Powered Hiring Assessment Platform

## Scenario Narrative

GlobalTalent Inc. is launching an AI-driven candidate assessment platform that analyzes resumes, video interviews, and coding challenge submissions to rank applicants for software engineering roles. The system will be used by 200+ enterprise clients across North America and the European Union, processing approximately 100,000 candidate applications monthly.

**Key Characteristics:**
- **Processes PII**: Collects names, contact information, work history, education records, video recordings, and potentially sensitive demographic data (if candidates volunteer it)
- **Customer-facing**: Candidates interact directly with the assessment interface; rankings influence hiring decisions
- **High-stakes**: Directly impacts employment opportunities, economic livelihood, and civil rights; errors could result in discriminatory outcomes
- **Moderate autonomy (level 2)**: Automatically ranks candidates and flags "recommended" vs. "not recommended"; hiring managers can override but often defer to AI scores
- **General sector**: Not healthcare/finance, but employment is a regulated domain under EU AI Act
- **No cyber/bio modifiers**: Primary risk is fairness/bias, not security exploits

**Business Context:**
The platform promises to reduce time-to-hire by 40% and increase candidate pool diversity through "bias-free" algorithmic screening. However, algorithmic bias lawsuits, regulatory scrutiny (EU AI Act Article 5 prohibits certain social scoring), and reputational damage are significant threats. A single discrimination lawsuit could cost $500K-$2M in settlements and legal fees.

## Risk Assessment Inputs

Using the Frontier AI Risk Assessment Framework:

| Parameter | Value | Contribution |
|-----------|-------|--------------|
| Contains PII | ✓ Yes | +2 |
| Customer-facing | ✓ Yes | +2 |
| High-stakes | ✓ Yes (employment rights) | +3 |
| Autonomy level | 2 (Auto-ranks with override) | +2 |
| Sector | General | 0 |
| Modifiers | None (bias/fairness not yet modeled) | 0 |

**Total Risk Score:** 9  
**Risk Tier:** **Critical**

## Generated Decision Record

Below is the actual Decision Record export from the framework:

---

# Frontier AI Risk Decision Record

**Scenario Owner:** Marcus Thompson (Chief Product Officer)  
**Approver:** Lisa Park (CEO)  
**Assessment Date:** 2024-10-07  
**Next Review Due:** 2025-01-05

## Summary
- **Risk Tier:** Critical
- **Risk Score:** 9
- **Key Drivers:** Contains PII (+2), Customer-facing exposure (+2), High-stakes impact (+3), Autonomy level 2 (+2)

## Scenario Inputs
- Contains PII: Yes
- Customer Facing: Yes
- High Stakes: Yes
- Autonomy Level: 2
- Sector: General
- Modifiers: None

## Required Safeguards

### Document accountable owner (NIST AI RMF)
- **ID:** NIST-GOV-01
- **Clause:** Govern 1.1 (illustrative)
- **Description:** Assign a named executive accountable for the AI system's governance posture.
- **Evidence to Capture:** Risk charter naming accountable executive and approval date.
- **Tags:** governance, accountability
- **Mappings:** mitre_atlas: TA0001

### High-risk AI system registration (EU AI Act)
- **ID:** EU-AIA-ART6-01
- **Clause:** Article 6 (illustrative)
- **Description:** Register the system in the EU database for high-risk AI systems if deployed in EU markets.
- **Evidence to Capture:** Registration confirmation and system cards.
- **Tags:** compliance, transparency

### Conformity assessment (EU AI Act)
- **ID:** EU-AIA-ART43-02
- **Clause:** Article 43 (illustrative)
- **Description:** Complete third-party conformity assessment before market placement.
- **Evidence to Capture:** Assessment report from notified body.
- **Tags:** compliance, audit

### Human oversight mechanisms (EU AI Act)
- **ID:** EU-AIA-ART14-03
- **Clause:** Article 14 (illustrative)
- **Description:** Implement capability for human intervention, including stop functions and monitoring.
- **Evidence to Capture:** Oversight procedures and escalation protocols.
- **Tags:** human_oversight, safety

### AI management system documentation (ISO/IEC 42001)
- **ID:** ISO-42001-DOC-01
- **Clause:** Clause 7.5 (illustrative)
- **Description:** Establish and maintain documented AI management system procedures.
- **Evidence to Capture:** AIMS policy manual and process maps.
- **Tags:** management_system, documentation

### Risk assessment and treatment (ISO/IEC 42001)
- **ID:** ISO-42001-RISK-02
- **Clause:** Clause 6.1 (illustrative)
- **Description:** Conduct systematic AI risk assessment and document treatment decisions.
- **Evidence to Capture:** Risk register with treatment plans and ownership.
- **Tags:** risk_management, assessment

### Leadership accountability (ISO/IEC 42001)
- **ID:** ISO-42001-LEAD-03
- **Clause:** Clause 5.1 (illustrative)
- **Description:** Assign leadership commitment and accountability for AI system outcomes.
- **Evidence to Capture:** Executive charter and accountability matrix.
- **Tags:** governance, leadership

### Sensitive data guardrails (OWASP LLM Top 10)
- **ID:** OWASP-LLM04-01
- **Clause:** LLM04 (illustrative)
- **Description:** Implement filters to redact or block PII and regulated data types before model responses.
- **Evidence to Capture:** Filter configuration with testing evidence and owner approvals.
- **Tags:** data_protection, guardrails

### Abuse monitoring (OWASP LLM Top 10)
- **ID:** OWASP-LLM08-02
- **Clause:** LLM08 (illustrative)
- **Description:** Instrument analytics to detect anomalous usage patterns that could indicate misuse.
- **Evidence to Capture:** Monitoring alerts, thresholds, and incident response linkage.
- **Tags:** monitoring, abuse_detection

### Impact assessment documentation (U.S. OMB AI Policy)
- **ID:** OMB-IA-01
- **Clause:** Sec 5(b) (illustrative)
- **Description:** Complete AI impact assessment covering rights, safety, and effectiveness.
- **Evidence to Capture:** Impact assessment report with stakeholder review.
- **Tags:** compliance, impact_assessment

### Chief AI Officer review (U.S. OMB AI Policy)
- **ID:** OMB-CAIO-02
- **Clause:** Sec 7 (illustrative)
- **Description:** Obtain Chief AI Officer review and approval for rights-impacting systems.
- **Evidence to Capture:** CAIO approval memorandum with conditions.
- **Tags:** governance, oversight

---
*Illustrative governance-as-code export. Validate safeguards with legal, compliance, and security teams before implementation.*

## Analysis & Commentary

### Why This Matters

Hiring AI is one of the **highest-profile AI risk domains** due to:
- **Regulatory focus**: EU AI Act explicitly classifies employment/recruitment as high-risk (Annex III, point 4)
- **Legal precedent**: Multiple algorithmic discrimination lawsuits (e.g., Amazon scrapped ML recruiting tool in 2018 after gender bias discovered)
- **Public scrutiny**: Civil rights organizations actively monitor hiring algorithms; media coverage of bias is reputational poison

The **Critical** tier and **11 controls** reflect this elevated risk profile.

### Key Control Themes

1. **EU AI Act Compliance (3 controls)**  
   - **EU-AIA-ART6-01 (Registration)**: High-risk system must be registered in EU database before deployment
   - **EU-AIA-ART43-02 (Conformity)**: Third-party assessment required; cannot self-certify
   - **EU-AIA-ART14-03 (Human oversight)**: Hiring managers must be able to override AI recommendations and understand the basis for rankings

2. **Governance Accountability (3 controls)**  
   - **NIST-GOV-01, ISO-42001-LEAD-03, OMB-CAIO-02**: Triple redundancy on executive accountability, signaling that employment decisions are too consequential for delegation to mid-level product managers

3. **Rights Impact Assessment (2 controls)**  
   - **ISO-42001-RISK-02, OMB-IA-01**: Formal risk/impact assessments must document fairness testing, disparate impact analysis, and mitigation strategies

4. **Data Protection (1 control)**  
   - **OWASP-LLM04-01**: PII guardrails prevent leaking candidate data across assessments or exposing training data in model outputs

5. **Abuse Monitoring (1 control)**  
   - **OWASP-LLM08-02**: Detect patterns like candidates gaming the system, hiring managers using AI to auto-reject protected classes, or adversarial resume stuffing

### Implementation Priorities

**Phase 1 (Strategy & Legal - Months 1-2):**
- Executive charter with CEO as accountable owner (NIST-GOV-01, ISO-42001-LEAD-03)
- Engage EU legal counsel to confirm high-risk classification and conformity pathway (EU-AIA-ART43-02)
- Impact assessment covering EEOC, GDPR, and EU AI Act requirements (OMB-IA-01, ISO-42001-RISK-02)

**Phase 2 (Product Design - Months 3-5):**
- Design human override interface for hiring managers (EU-AIA-ART14-03)
- Build PII redaction filters (OWASP-LLM04-01)
- Define bias testing methodology (disparate impact ratios by gender, race, age)

**Phase 3 (Testing & Validation - Months 6-7):**
- Run fairness audits with synthetic candidate pools
- Third-party conformity assessment (EU markets only) (EU-AIA-ART43-02)
- CAIO review and approval sign-off (OMB-CAIO-02)

**Phase 4 (Launch & Monitoring - Month 8+):**
- Register in EU high-risk AI database (EU-AIA-ART6-01)
- Deploy abuse monitoring dashboards (OWASP-LLM08-02)
- Quarterly bias re-audits and model retraining

### Gaps & Enhancement Recommendations

The Decision Record surfaced **two critical gaps** in the current policy packs:

#### Gap 1: Fairness/Bias Modifier Missing

**Problem**: The scenario has zero modifiers despite employment bias being the primary risk. The framework treats this identically to a general-purpose chatbot with the same PII + customer-facing + high-stakes profile.

**Impact**: No specific controls for:
- Disparate impact testing (EEOC's 80% rule)
- Protected class monitoring (gender, race, age, disability)
- Explainability requirements (candidates have right to explanation under GDPR Article 22)

**Recommendation**: Add **"Fairness"** modifier to the intake form with +2 weight. Triggers should include:
- Employment, lending, housing, insurance decisions
- Systems impacting protected classes
- Scenarios subject to anti-discrimination law

New controls to author:
- `FAIRNESS-01`: Disparate impact analysis (reference EEOC guidance)
- `FAIRNESS-02`: Explainability mechanisms (GDPR Article 22, LIME/SHAP implementation)
- `FAIRNESS-03`: Regular bias audits by third party (quarterly or semi-annual)

#### Gap 2: Sector Granularity

**Problem**: "General" sector provides no signal that employment is a regulated domain. Healthcare and Finance get +1 sector bump, but hiring doesn't.

**Impact**: Tier remains Critical (9 points), but misses opportunity to trigger sector-specific controls like EEOC compliance or GDPR Article 22 (automated decision-making).

**Recommendation**: Add **"Employment"** as a sector option with +1 weight. Create `employment_ai.yaml` policy pack with controls like:
- `EMP-EEOC-01`: Adverse impact analysis per EEOC Uniform Guidelines
- `EMP-GDPR-22`: Right to explanation and human review (GDPR Article 22)
- `EMP-ADA-01`: Accessibility testing for candidates with disabilities (ADA compliance)

### Real-World Precedents

**Why these controls matter** (actual incidents):

1. **Amazon ML Recruiting Tool (2018)**  
   - *What happened*: Model trained on 10 years of resumes (mostly male) learned to penalize resumes containing "women's" (e.g., "women's chess club captain")
   - *Control that would have helped*: Fairness audits (Gap 1) and human oversight (EU-AIA-ART14-03)
   - *Outcome*: Tool scrapped; massive reputational damage

2. **HireVue Algorithmic Audit (2021)**  
   - *What happened*: NYC Local Law 144 required bias audit of video interview AI; advocates found insufficient transparency
   - *Control that would have helped*: Third-party conformity assessment (EU-AIA-ART43-02), impact assessment (OMB-IA-01)
   - *Outcome*: HireVue stopped using facial analysis; regulatory precedent set

3. **Workday Discrimination Lawsuit (2023)**  
   - *What happened*: Plaintiffs alleged AI screening tool discriminated based on age and disability
   - *Control that would have helped*: Protected class monitoring (Gap 1), leadership accountability (ISO-42001-LEAD-03)
   - *Outcome*: Litigation ongoing; chilling effect on AI hiring adoption

### Stakeholder Communication Template

**For Sales/Marketing:**
"Our AI hiring platform meets Critical tier governance standards with 11+ framework-aligned safeguards. We've completed third-party conformity assessment for EU markets and maintain executive accountability through our CEO. Quarterly bias audits and human oversight mechanisms demonstrate our commitment to responsible AI."

**For Legal/Compliance:**
"Decision Record attached. We've flagged two policy pack gaps (fairness modifier and employment sector) for v0.2 release. In the interim, we're manually tracking EEOC disparate impact analysis and GDPR Article 22 explainability as supplemental controls outside the framework."

**For Engineering:**
"Critical tier = production-blocking requirements. No launch without CAIO sign-off (OMB-CAIO-02), human override UI (EU-AIA-ART14-03), and PII filters (OWASP-LLM04-01). Bias testing must run in CI/CD before every model retrain."

## Conclusion

This case study demonstrates that **employment AI triggers maximum governance scrutiny** even without sector-specific modifiers. The 9-point score and Critical tier classification are appropriate given the legal, regulatory, and reputational risks.

However, the analysis also reveals **actionable policy pack improvements**:
- Add "Fairness" modifier (+2 weight)
- Add "Employment" sector (+1 weight)
- Author `fairness_controls.yaml` and `employment_ai.yaml` packs

These enhancements would push the score to **12 points** and unlock 5-8 additional controls—better aligning the framework with employment AI's unique risk profile.

**Next steps**: Log GitHub issues for policy pack v0.2 and use this case study as the requirements document.

