
# Frontier AI Risk Decision Record

**Scenario Owner:** Sarah Chen, Product Manager  **Approver:** David Martinez, VP Engineering  **Assessment Date:** 2025-10-09  **Next Review Due:** 2026-01-07

## Summary
- **Risk Tier:** Critical
- **Risk Score:** 15
- **Key Drivers:** Contains PII (+2), Customer-facing exposure (+2), High-stakes impact (+3), Autonomy level 2 (+2), Sector sensitivity Healthcare (+1), Model type Generative AI / LLM (+2), Foundation model: External API (+2), Protected population: Elderly (+1)

## Scenario Inputs
- **Use Case:** A chatbot that helps hospital patients schedule appointments and refill prescriptions. It accesses medical records to check medication history and insurance eligibility. Patients interact directly via web/mobile. The system suggests appointment times but requires nurse approval for prescription refills.
- Contains PII: Yes
- Customer Facing: Yes
- High Stakes: Yes
- Autonomy Level: 2 (Human oversight)
- Sector: Healthcare
- Modifiers: None
- Model Type: Generative AI / LLM
- Data Source: Proprietary/Internal
- Real-time Learning: No
- International Data Transfers: No
- Explainability: Post-hoc Explainable
- Foundation Model: External API (OpenAI GPT-4)
- Generates Synthetic Content: No
- Dual-Use Risk: None
- Decision Reversibility: Reversible with Cost
- Protected Populations: Elderly

## Required Safeguards

### High-risk registration (EU AI Act)
- **ID:** EU-HR-01
- **Clause:** Title III, Chapter 2 (illustrative)
- **Description:** Record the system in an internal EU AI Act high-risk inventory with conformity evidence.
- **Evidence to Capture:** Inventory entry with conformity assessment references and documentation URLs.
- **Tags:** compliance, inventory
- **Mappings:** EU_AI_Act: Annex III-5.a (Healthcare), NIST_AI_RMF: GOVERN-1.5

### HIPAA Business Associate Agreement
- **ID:** NIST-PRIVACY-01
- **Clause:** HIPAA Privacy Rule 45 CFR 164.308
- **Description:** Execute Business Associate Agreement with OpenAI covering PHI access and security requirements.
- **Evidence to Capture:** Signed BAA, data flow diagram, encryption verification
- **Tags:** privacy, healthcare
- **Mappings:** NIST_AI_RMF: GOVERN-2.1, ISO_42001: 5.3

### Human oversight for prescription decisions
- **ID:** EU-OVERSIGHT-02
- **Clause:** EU AI Act Article 14 (illustrative)
- **Description:** Ensure qualified healthcare professional reviews all prescription-related recommendations before execution.
- **Evidence to Capture:** Audit logs showing nurse approval timestamps, escalation procedures documentation
- **Tags:** human_oversight, safety
- **Mappings:** EU_AI_Act: Article 14, NIST_AI_RMF: GOVERN-1.2

### Bias testing across patient demographics
- **ID:** NIST-MEASURE-03
- **Clause:** NIST AI RMF MEASURE-2.3
- **Description:** Conduct fairness testing across age, race, gender, and disability status to ensure equitable treatment recommendations.
- **Evidence to Capture:** Testing report with disaggregated metrics, remediation plan for any disparities
- **Tags:** fairness, testing
- **Mappings:** NIST_AI_RMF: MEASURE-2.3, ISO_42001: 6.5.3

### Transparency notice for AI interaction
- **ID:** EU-TRANSP-03
- **Clause:** EU AI Act Article 52 (illustrative)
- **Description:** Provide patients with clear notice that they are interacting with an AI system and how decisions are reviewed.
- **Evidence to Capture:** Screenshot of disclosure message, user testing results
- **Tags:** transparency, user_experience
- **Mappings:** EU_AI_Act: Article 52, NIST_AI_RMF: GOVERN-4.1

### Prompt injection defenses (OWASP LLM01)
- **ID:** OWASP-LLM01-EXTENDED
- **Clause:** OWASP LLM Top 10 - LLM01 (Prompt Injection)
- **Description:** Implement input validation and sanitization to prevent prompt injection attacks that could manipulate medical recommendations.
- **Evidence to Capture:** Penetration test results, input filtering logic documentation
- **Tags:** security, llm
- **Mappings:** OWASP_LLM: LLM01, MITRE_ATLAS: AML.T0051.000

### Data leakage prevention for External API
- **ID:** SUPPLY-CHAIN-001
- **Clause:** ISO 42001 Section 5.3
- **Description:** Implement controls to prevent sensitive PHI from being used in model training by external provider.
- **Evidence to Capture:** Contract terms prohibiting training on customer data, audit of API calls
- **Tags:** supply_chain, privacy
- **Mappings:** ISO_42001: 5.3, NIST_AI_RMF: MANAGE-3.2

### Accessibility for elderly users
- **ID:** PROTECT-POP-001
- **Clause:** ADA Title III, Section 508
- **Description:** Ensure chatbot interface meets WCAG 2.1 AA standards with enhanced accommodations for elderly users (larger fonts, simplified language, voice options).
- **Evidence to Capture:** Accessibility audit report, user testing with elderly participants
- **Tags:** accessibility, vulnerable_populations
- **Mappings:** NIST_AI_RMF: GOVERN-1.4, ISO_42001: 6.5.4

## Owners & Next Steps

**System Owner:** Sarah Chen (sarah.chen@hospital.org)  
**Technical Lead:** Alex Rodriguez (alex.rodriguez@hospital.org)  
**Approver:** David Martinez (david.martinez@hospital.org)  
**Next Review:** January 7, 2026 (90 days from approval)

### Pre-Launch Requirements (Stop-Ship)
1. ✅ **Completed:** BAA executed with OpenAI (signed 2025-09-15)
2. ✅ **Completed:** Bias testing conducted across demographics (report dated 2025-09-28, no significant disparities found)
3. ⏳ **In Progress:** HIPAA Security Risk Assessment (target: 2025-10-15)
4. ⏳ **In Progress:** Penetration testing including prompt injection scenarios (scheduled: 2025-10-20)
5. ❌ **Not Started:** Accessibility audit with elderly user testing
6. ❌ **Not Started:** Privacy Impact Assessment review by Chief Privacy Officer

### Post-Launch Monitoring
- Weekly review of nurse override rates for prescription recommendations
- Monthly bias metrics dashboard review (by demographic group)
- Quarterly security assessment and prompt injection testing
- Annual comprehensive review including regulatory updates

## Risk Mitigation Summary

**Why Critical Tier?**  
This system processes Protected Health Information (PHI), makes recommendations about medications that could impact patient safety, and serves elderly patients who may be vulnerable to confusion or incorrect guidance. The combination of healthcare sector, high-stakes outcomes, and protected population triggers Critical tier classification under the EU AI Act high-risk framework.

**Key Mitigations:**
1. **Human-in-the-loop:** All prescription refills require nurse approval, preventing fully autonomous medication changes
2. **Vendor controls:** BAA with OpenAI ensures PHI is protected and not used for training
3. **Fairness testing:** Demographic analysis confirms equitable treatment across patient groups
4. **Transparency:** Patients are clearly informed they're interacting with AI
5. **Accessibility:** Interface designed for elderly users with enhanced usability features

**Residual Risks:**
- Potential for AI hallucinations providing incorrect medication information (mitigated by nurse review)
- Dependency on external API availability (mitigated by fallback to human schedulers)
- Risk of prompt injection bypassing safety guardrails (being addressed in penetration testing)

## Approval Signatures

**System Owner:** _________________________ (Sarah Chen) Date: __________

**Privacy Officer:** _________________________ (Jennifer Wu) Date: __________

**Security Lead:** _________________________ (Marcus Johnson) Date: __________

**VP Engineering (Approver):** _________________________ (David Martinez) Date: __________

---

*This is an illustrative governance-as-code export based on the RAI Toolkit demonstration. All policy citations are for educational purposes. Validate safeguards with legal, privacy, compliance, and security teams before treating this as binding approval documentation.*

**Generated by:** RAI Toolkit v1.0  
**Framework Version:** Policy Packs v0.1  
**Export Date:** 2025-10-09 16:30 UTC

