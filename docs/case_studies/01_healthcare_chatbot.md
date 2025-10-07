# Case Study 1: Healthcare Patient Support Chatbot

## Scenario Narrative

MedCare Health Systems is developing an AI-powered chatbot to help patients schedule appointments, review lab results, and receive medication reminders. The chatbot will be accessible through the patient portal and a mobile app, handling approximately 50,000 patient interactions monthly.

**Key Characteristics:**
- Processes protected health information (PHI) including names, dates of birth, medical record numbers, and clinical data
- Customer-facing interface with direct patient exposure
- High-stakes due to potential for medical misinformation or privacy breaches
- Moderate autonomy: can book appointments and send reminders without human review, but escalates clinical questions to medical staff
- Healthcare sector with strict HIPAA compliance requirements
- Cyber risk modifier due to PHI exposure and potential for social engineering attacks

**Business Context:**
The system aims to reduce call center volume by 30% while improving patient satisfaction scores. However, a breach or safety incident could result in HIPAA fines ($100-$50,000 per violation), reputational damage, and potential patient harm if incorrect medical guidance is provided.

## Risk Assessment Inputs

Using the Frontier AI Risk Assessment Framework:

| Parameter | Value | Contribution |
|-----------|-------|--------------|
| Contains PII | ✓ Yes (PHI) | +2 |
| Customer-facing | ✓ Yes | +2 |
| High-stakes | ✓ Yes | +3 |
| Autonomy level | 2 (Can act with escalation rules) | +2 |
| Sector | Healthcare | +1 |
| Modifiers | Cyber | +2 |

**Total Risk Score:** 12  
**Risk Tier:** **Critical**

## Generated Decision Record

Below is the actual Decision Record export from the framework:

---

# Frontier AI Risk Decision Record

**Scenario Owner:** Dr. Sarah Chen (Chief Medical Information Officer)  
**Approver:** James Rodriguez (VP of Digital Health)  
**Assessment Date:** 2024-10-07  
**Next Review Due:** 2025-01-05

## Summary
- **Risk Tier:** Critical
- **Risk Score:** 12
- **Key Drivers:** Contains PII (+2), Customer-facing exposure (+2), High-stakes impact (+3), Autonomy level 2 (+2), Sector sensitivity Healthcare (+1), Modifier Cyber (+2)

## Scenario Inputs
- Contains PII: Yes
- Customer Facing: Yes
- High Stakes: Yes
- Autonomy Level: 2
- Sector: Healthcare
- Modifiers: Cyber

## Required Safeguards

### Document accountable owner (NIST AI RMF)
- **ID:** NIST-GOV-01
- **Clause:** Govern 1.1 (illustrative)
- **Description:** Assign a named executive accountable for the AI system's governance posture.
- **Evidence to Capture:** Risk charter naming accountable executive and approval date.
- **Tags:** governance, accountability
- **Mappings:** mitre_atlas: TA0001

### Adversarial robustness testing (NIST AI RMF)
- **ID:** NIST-MEASURE-05
- **Clause:** Measure 4.1 (illustrative)
- **Description:** Run documented adversarial test suites targeting prompt injection and insecure outputs.
- **Evidence to Capture:** Test reports with coverage metrics and mitigation owners.
- **Tags:** security, testing
- **Mappings:** owasp_llm_top10: LLM01, LLM05; mitre_atlas: TA0007

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

### Prompt injection test coverage (OWASP LLM Top 10)
- **ID:** OWASP-LLM01-LOG
- **Clause:** LLM01 (illustrative)
- **Description:** Execute adversarial prompt suites covering jailbreak, data exfiltration, and tool abuse.
- **Evidence to Capture:** Security test report with blocked payload catalog.
- **Tags:** security, prompt_injection
- **Mappings:** mitre_atlas: TA0007

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

### Adversarial testing coverage (MITRE ATLAS)
- **ID:** ATLAS-ML-EVAL-01
- **Clause:** AML.T0043 (illustrative)
- **Description:** Execute documented adversarial test cases aligned with ATLAS threat taxonomy.
- **Evidence to Capture:** Test execution logs with ATLAS tactic/technique mappings.
- **Tags:** security, red_team
- **Mappings:** atlas_tactics: TA0043

### Anomaly detection monitoring (MITRE ATLAS)
- **ID:** ATLAS-ML-MONITOR-02
- **Clause:** AML.T0020 (illustrative)
- **Description:** Deploy runtime monitoring to detect inference attacks and model extraction attempts.
- **Evidence to Capture:** SIEM integration and detection rule coverage.
- **Tags:** monitoring, threat_detection
- **Mappings:** atlas_tactics: TA0020

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

This scenario triggered **Critical** tier classification and **15 distinct safeguards** spanning six frameworks. The combination of PHI, customer exposure, and healthcare context creates compounding risk that requires defense-in-depth.

### Key Control Themes

1. **Governance & Accountability** (NIST-GOV-01, ISO-42001-LEAD-03, OMB-CAIO-02): Three frameworks require named executive ownership, reflecting the principle that high-stakes AI demands C-suite accountability.

2. **Technical Security** (OWASP-LLM01-LOG, NIST-MEASURE-05, ATLAS-ML-EVAL-01): Multiple controls mandate adversarial testing, recognizing that healthcare chatbots are attractive targets for prompt injection attacks seeking PHI exfiltration.

3. **Human Oversight** (EU-AIA-ART14-03): EU AI Act requires "stop functions" and monitoring, aligning with medical best practice that AI should augment—not replace—clinical judgment.

4. **Privacy Engineering** (OWASP-LLM04-01): Guardrails must prevent the model from regurgitating PHI from training data or exposing one patient's information to another.

### Implementation Priorities

**Phase 1 (Pre-Development):**
- Executive charter (NIST-GOV-01, ISO-42001-LEAD-03)
- Impact assessment (OMB-IA-01)
- Risk register initialization (ISO-42001-RISK-02)

**Phase 2 (Development & Testing):**
- Adversarial test suites (OWASP-LLM01-LOG, NIST-MEASURE-05)
- PII redaction filters (OWASP-LLM04-01)
- Escalation logic for clinical questions (EU-AIA-ART14-03)

**Phase 3 (Pre-Launch):**
- Conformity assessment if EU deployment (EU-AIA-ART43-02)
- CAIO review (OMB-CAIO-02)
- Anomaly monitoring deployment (ATLAS-ML-MONITOR-02)

**Phase 4 (Post-Launch):**
- Quarterly risk review (ISO-42001-RISK-02)
- Continuous abuse monitoring (OWASP-LLM08-02)

### Lessons for Similar Scenarios

- **Autonomy calibration**: Setting autonomy to level 2 (vs. 3) reflects the escalation logic for clinical questions. If the chatbot provided medical advice without human review, autonomy level 3 would add +1 to the score.
  
- **Modifier selection**: "Cyber" was chosen over "Bio" because the primary threat is data exfiltration, not biological misuse. A chatbot providing treatment protocols might warrant "Bio" instead.

- **Sector alignment**: Healthcare sector adds only +1, but unlocks sector-specific controls like EU AI Act high-risk classification. The framework rewards domain context.

### Red Flags Identified

During assessment, the team identified two gaps:

1. **Model provenance**: Decision Record doesn't capture training data sources. Future pack revision should add control for data lineage in high-risk scenarios.

2. **Explainability**: No controls mandate explanation mechanisms. ISO 42001 rev could add clause requiring model transparency for patient-facing systems.

Both gaps logged as enhancement requests for policy pack v0.2.

