# Transparency Note

**System Name:** HealthAssist Patient Support Chatbot

**Version:** 1.0

**Last Updated:** January 10, 2025

**Contact:** healthassist-governance@example.com

---

## What is this system?

**Purpose:**  
HealthAssist is an AI-powered chatbot that helps hospital patients schedule appointments, refill prescriptions, and access general health information. It operates through web and mobile applications to provide 24/7 patient support.

**Context:**  
This system operates in the **Healthcare** sector and is assessed as **Critical risk** (score: 12/42).

---

## What can this system do?

**Capabilities:**  
- Schedule, reschedule, and cancel medical appointments
- Process prescription refill requests (requires nurse approval)
- Answer general health questions using curated medical information
- Access patient medical records to verify medication history and insurance eligibility
- Send appointment reminders and follow-up care instructions

**Example Use Cases:**  
1. A patient asks to refill their blood pressure medication → System checks medical records → Flags for nurse review → Nurse approves → Prescription sent to pharmacy
2. A patient wants to schedule a follow-up appointment → System checks provider availability → Suggests times → Patient confirms → Appointment booked
3. A patient asks about post-surgery care instructions → System retrieves personalized care plan → Provides step-by-step guidance

---

## What are this system's intended uses?

**Intended Users:**  
External users (customers, general public) - specifically registered patients of participating hospitals

**Intended Scenarios:**  
- Non-emergency appointment scheduling and prescription management
- Access to personal health information for self-service tasks
- General health education and post-care instructions
- Routine administrative tasks that don't require immediate clinician judgment

**Autonomy Level:** Human-in-the-loop - AI acts but humans review and approve before impact

---

## What are this system's limitations?

**Known Limitations:**
- Processes personal or sensitive data (PII, PHI) - HIPAA compliance controls required
- High-stakes outcomes - human review required for all prescription-related decisions
- Limited to English language; non-English speakers must contact support directly
- Cannot handle emergency medical situations - directs users to 911 for emergencies
- Requires existing patient relationship; not for new patient intake

**Out of Scope:**  
- Emergency medical advice or triage (users directed to 911)
- Initial diagnosis or treatment recommendations (requires licensed clinician)
- Controlled substance prescriptions (must go through physician directly)
- Mental health crisis support (users directed to crisis hotline)
- Pediatric medication dosing (requires pharmacist consultation)

**Human Oversight Requirements:**  
Human review required for all decisions affecting users - specifically, nurse approval required for all prescription refill requests

---

## How was this system evaluated?

**Testing & Validation:**  
- Tested on 10,000 synthetic patient interactions across 50 common scenarios
- Adversarial testing conducted for prompt injection, PII leakage, and medical misinformation
- Clinical accuracy validated against curated medical knowledge base (95% agreement with nurse reviews)
- HIPAA Security Rule controls validated by independent auditor
- Bias testing across age, gender, and socioeconomic demographics

**Identified Risk Factors:**  
- Contains PII (+2)
- Customer-facing exposure (+2)
- High-stakes impact (+3)
- Autonomy level 1 (+1)
- Sector sensitivity Healthcare (+1)
- Generative AI / LLM model type (+2)
- Uses foundation model via External API (+1)

**Governance Standards Applied:**  
EU AI Act (Illustrative), ISO/IEC 42001, MITRE ATLAS, NIST AI RMF, OWASP LLM Top 10 (2025), US OMB M-25-21

---

## What are the governance safeguards?

This system is subject to the following governance controls:

- **Adversarial evaluation** (NIST GOVERN-3.2, MEASURE-2.13)
- **Sensitive Use Disclosure Documentation** (EU AI Act Art. 13 (illustrative))
- **Transparency & Explainability in Outputs** (EU AI Act Art. 13 (illustrative))
- **Human review of consequential decisions** (NIST GOVERN-1.1, MAP-5.1)
- **Data minimization and encryption for PII/PHI** (NIST AI RMF GOVERN-5.1, MANAGE-4)
- **Access control and audit logging** (ISO/IEC 42001 8.8)
- **Red-team testing for prompt injection** (OWASP LLM01)
- **Data leakage prevention** (OWASP LLM06)
- **Third-party risk assessment** (MITRE ATLAS AML.T0010)
- **Vendor data sharing agreement** (EU AI Act Art. 25 (illustrative))
- **Model monitoring and drift detection** (NIST AI RMF MEASURE-2.7, MANAGE-1.2)
- **Incident response plan** (ISO/IEC 42001 9.1)
- **Business Associate Agreement (HIPAA compliance)** (NIST AI RMF GOVERN-5.1)
- **Cross-border data transfer safeguards** (EU AI Act Art. 10 (illustrative))
- **Pre-launch safety testing** (NIST AI RMF MEASURE-2.1, MEASURE-2.3)

**Full control documentation:** See Decision Record for complete list of 15 triggered safeguards.

---

## What data does this system use?

**Data Processing:**  
✅ Processes personal or sensitive data (PII/PHI) - protected health information including medical records, medication history, insurance information, and contact details

**Data Sources:**  
- **Training data:** Curated medical knowledge base from licensed medical publishers and hospital-approved patient education materials
- **User input:** Patient queries, appointment preferences, and refill requests (entered via chat interface)
- **Integration data:** Electronic Health Records (EHR) system via HL7 FHIR API
- **Third-party API:** OpenAI GPT-4 for natural language understanding (PHI filtered before API calls; BAA in place)

**Data Storage & Retention:**  
- PHI stored in HIPAA-compliant AWS environment (us-east-1, encrypted at rest with AES-256)
- Chat transcripts retained for 90 days for quality assurance, then automatically deleted
- Audit logs retained for 7 years per HIPAA requirements
- No training data collected from patient interactions

**Cross-Border Transfers:**  
⚠️ May involve cross-border data transfers; GDPR adequacy requirements apply - EU patient data processed in AWS Frankfurt (eu-central-1) only; data residency controls enforced

---

## How do users control their data?

**User Rights:**  
- **Access:** Patients can request full chat history via patient portal or by calling support
- **Correction:** Patients can correct factual errors in chat transcripts; medical record corrections go through standard EHR process
- **Deletion:** Patients can request deletion of chat history (audit logs retained per HIPAA requirements)
- **Export:** Patients can download chat transcripts in PDF format via patient portal

**Opt-Out Mechanisms:**  
- Patients can opt out of chatbot and use phone/in-person support instead
- Patients can opt out of chat transcript retention (system will still function with real-time-only memory)
- Patients cannot opt out of audit logging (required for HIPAA compliance and patient safety)

**Contact for Data Requests:**  
privacy@example.com | 1-800-555-HEALTH | Privacy Officer, Example Hospital System

---

## What happens if the system makes a mistake?

**Error Handling:**  
- All prescription requests require nurse review (catches medication errors)
- System includes "I'm not sure" responses for ambiguous queries rather than guessing
- Emergency keywords ("chest pain", "stroke", "suicide") immediately escalate to 911 prompt
- Appointment booking errors flagged for manual correction within 24 hours
- Real-time monitoring dashboards track response accuracy, hallucination detection, and escalation rates

**Remediation Process:**  
1. Patient or nurse flags error via "Report Issue" button in chat
2. Clinical quality team reviews within 4 business hours
3. If confirmed error: patient notified, chat transcript annotated, corrective action logged
4. If medication safety issue: immediate escalation to pharmacy and provider
5. Root cause analysis conducted for all Critical/High severity errors

**Decision Reversibility:**  
Reversible with Cost - Appointment cancellations incur no charge if done >24hr in advance; prescription refills can be cancelled before pharmacy pickup

**Appeal/Review Process:**  
Human review available upon request - patients can request nurse or provider review of any chatbot interaction via phone or patient portal

---

## How is this system monitored?

**Performance Monitoring:**  
- **Response accuracy:** Tracked against nurse review outcomes (target: 95%+ agreement)
- **Hallucination detection:** Automated checks for medical claims not in knowledge base (alert threshold: 2% of responses)
- **User satisfaction:** In-chat feedback after each interaction (target: 4.0+ out of 5.0)
- **System uptime:** 99.5% availability target
- **Dashboard:** Real-time clinical quality dashboard reviewed daily by nursing supervisor

**Fairness Monitoring:**  
Required for this system given high-stakes outcomes and/or protected populations:
- Quarterly demographic analysis of appointment wait times (by age, race, gender, zip code)
- Prescription refill approval rates monitored for disparities
- Medication recommendation accuracy tested across demographic groups
- Third-party fairness audit conducted annually

**Incident Response:**  
- **Tier 1 (Low):** Clinical quality team review within 5 business days
- **Tier 2 (Medium):** 24-hour response, clinical leadership notification
- **Tier 3 (High):** 4-hour response, system pause for specific function, provider notification
- **Tier 4 (Critical):** Immediate system shutdown, all affected patients contacted, regulatory reporting

---

## Who is responsible for this system?

**System Owner:**  
Dr. Sarah Chen, Chief Medical Information Officer (CMIO) | sarah.chen@example.com

**Governance Approval:**  
- **Product Owner:** Jane Smith, VP Digital Health | Approved: Dec 15, 2024
- **Clinical Quality:** Dr. Michael Rodriguez, Medical Director | Approved: Dec 18, 2024
- **Privacy Officer:** Lisa Park, JD | Approved: Dec 20, 2024
- **Information Security:** Tom Williams, CISO | Approved: Dec 20, 2024

**Legal/Compliance Sign-Off:**  
Required for Critical risk tier systems - **Signed:** General Counsel (John Davis) | Date: Dec 22, 2024

**Last Review Date:**  
January 5, 2025 - Full governance review post-launch

**Next Review Date:**  
July 5, 2025 - Recommend annual for High/Critical tier (6-month review for first year post-launch)

---

## Additional Resources

**Documentation:**  
- Technical Architecture Document: https://internal.example.com/docs/healthassist-architecture
- HIPAA Security Assessment: https://internal.example.com/docs/healthassist-hipaa-sar
- Clinical Knowledge Base Sources: https://internal.example.com/docs/healthassist-knowledge-sources
- API Documentation: https://internal.example.com/docs/healthassist-api

**Support:**  
- Patient Support: 1-800-555-HEALTH | support@example.com
- Technical Issues: healthassist-support@example.com
- Privacy Concerns: privacy@example.com
- Safety Incidents: safety@example.com (24/7 hotline)

**Feedback:**  
- In-chat feedback button (available after each interaction)
- Patient portal feedback form: https://patient.example.com/feedback
- Safety concerns: Report via "Flag for Review" button or call hotline

---

*This Transparency Note was generated using the RAI Toolkit (https://github.com/hankthevc/rai-toolkit) and completed by the HealthAssist governance team. Illustrative, for demo purposes; not official guidance. Review with legal, privacy, and security teams before use.*

*Last Updated: January 10, 2025 | Version 1.0*

