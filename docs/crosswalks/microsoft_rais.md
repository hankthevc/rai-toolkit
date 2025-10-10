# Microsoft Responsible AI Standard (RAIS) Crosswalk

**Status:** Illustrative alignment based on [publicly available RAIS documentation](https://www.microsoft.com/en-us/ai/responsible-ai)  
**Last Updated:** January 2025

---

## Overview

This crosswalk demonstrates how the RAI Toolkit's assessment workflow aligns with Microsoft's Responsible AI Standard (RAIS) goals and artifact requirements. **This is an illustrative example for demonstration purposes**—it does not replicate Microsoft's internal assessment processes or checklists.

All mappings are based on the [published RAIS goals](https://www.microsoft.com/en-us/ai/responsible-ai) and publicly available documentation.

---

## RAIS Goals Mapping

### A1: Impact Assessment

**RAIS Goal:** "We will conduct Impact Assessments for AI systems that may significantly affect consequential decisions or outcomes for people."

**RAI Toolkit Support:**
- ✅ **Risk scoring across 16 dimensions** → Structured impact assessment covering fairness, privacy, security, transparency
- ✅ **High-stakes outcome detection** → Flags safety-critical, rights-impacting, and financially significant decisions
- ✅ **Sector-specific considerations** → Healthcare (HIPAA), Finance (Fair Lending), Children (COPPA)
- ✅ **Protected populations screening** → Identifies impacts on vulnerable groups (children, elderly, low-income, etc.)

**Generated Artifacts:**
- Decision Record with risk tier, contributing factors, and impact summary
- Risk assessment JSON for integration with impact assessment workflows

**Tool → RAIS Workflow:**
1. User describes AI system → Tool assesses high-stakes outcomes, sector, populations
2. Risk tier (Low/Medium/High/Critical) maps to impact assessment trigger threshold
3. Critical-tier systems automatically flag for formal Impact Assessment
4. Decision Record provides structured input for IA documentation

---

### A2: Sensitive or Restricted Use Triage

**RAIS Goal:** "We will identify and triage Sensitive or Restricted Uses that require additional governance."

**RAI Toolkit Support:**
- ✅ **Sensitive use detection** → Flags biometric ID, real-time classification, emotion recognition, behavioral monitoring
- ✅ **High-risk category screening** → EU AI Act Annex III alignment (employment, education, law enforcement, critical infrastructure)
- ✅ **Dual-use risk assessment** → Identifies systems with weaponization, surveillance, or export control implications
- ✅ **Escalation gating** → Critical-tier + specific modifiers trigger "Requires Executive Review" flag

**Illustrative Gating Example:**
```python
# Demonstrative sensitive use gate (not Microsoft's actual criteria)
if (risk_tier == "Critical" and 
    (biometric_id or real_time_classification) and
    (customer_facing or high_stakes)):
    flag_sensitive_use = True
    escalation_required = "Executive Review + Legal Sign-Off"
```

**Generated Artifacts:**
- Decision Record with "Stop-Ship" or "Escalation Required" labels
- Sensitive use flags in assessment metadata

---

### A3: Fit for Purpose

**RAIS Goal:** "We will ensure AI systems are fit for their intended purpose through testing, validation, and monitoring."

**RAI Toolkit Support:**
- ✅ **Autonomy level assessment** → Evaluates human oversight (suggestion-only → full autonomy)
- ✅ **Explainability requirements** → Flags black-box models for high-stakes decisions
- ✅ **Decision reversibility** → Identifies irreversible decisions requiring enhanced controls
- ✅ **Failure mode considerations** → Captures "what happens if it's wrong" in assessment

**Generated Artifacts:**
- Safeguards requiring adversarial testing, human oversight, and monitoring
- Decision Record section: "Pre-Launch Testing Requirements"

**Tool → RAIS Workflow:**
1. Autonomy level 3 (full autonomy) + high-stakes → triggers human oversight requirements
2. Black-box explainability + rights-impacting → triggers explainability controls
3. Irreversible decisions → triggers audit logging, appeal mechanisms

---

### T2: Transparency and Communication to Stakeholders

**RAIS Goal:** "We will communicate transparently with stakeholders about AI system capabilities, limitations, and appropriate use."

**RAI Toolkit Support:**
- ✅ **Transparency Note generation** → Exports stakeholder-facing documentation
- ✅ **Framework citations** → Every safeguard includes policy reference (NIST, EU AI Act, ISO 42001)
- ✅ **Risk reasoning transparency** → AI analysis explains why specific risks apply
- ✅ **Stakeholder communication artifacts** → Decision Record formatted for non-technical reviewers

**Generated Artifacts:**
- **Transparency Note** (stub with structured fields for completion)
- Decision Record with plain-language risk summary
- Governance Q&A chat export for stakeholder briefings

**Tool → RAIS Workflow:**
1. Risk assessment complete → Generate Transparency Note stub
2. Populate system description, intended use, limitations, contact info
3. Include risk tier, safeguards, and known limitations
4. Export as markdown for review/publication

---

### PS1: Privacy

**RAIS Goal:** "We will implement privacy protections appropriate to the data processed and the risks posed."

**RAI Toolkit Support:**
- ✅ **PII/PHI detection** → Flags personal data processing
- ✅ **Cross-border data transfer screening** → Identifies GDPR/Schrems II implications
- ✅ **Data provenance tracking** → Assesses training data sources (public, scraped, user-generated)
- ✅ **Vendor data sharing** → Flags external API usage (OpenAI, Azure OpenAI, etc.)

**Generated Artifacts:**
- Privacy-specific safeguards (data minimization, access controls, encryption)
- Decision Record section: "Data Handling & Privacy Controls"
- Policy pack controls citing GDPR Art. 5, HIPAA §164.308, ISO 27701

---

### PS2: Security

**RAIS Goal:** "We will implement security measures appropriate to the threats posed to the AI system."

**RAI Toolkit Support:**
- ✅ **Adversarial threat screening** → Model type (LLM, CV, RL) maps to MITRE ATLAS tactics
- ✅ **Supply chain risk** → Foundation model dependencies, third-party APIs
- ✅ **Online learning risk** → Flags data poisoning, model drift concerns
- ✅ **Dual-use risk** → Export controls, weaponization potential

**Generated Artifacts:**
- Security-specific safeguards (adversarial testing, input validation, model monitoring)
- MITRE ATLAS tactic references
- Policy pack controls citing OWASP LLM Top 10, NIST Cybersecurity Framework

---

## Artifact Generation Summary

| RAIS Requirement | RAI Toolkit Artifact | Export Format |
|------------------|---------------------|---------------|
| A1: Impact Assessment | Decision Record with risk tier, factors, impact summary | Markdown, JSON |
| A2: Sensitive Use Triage | Escalation flags, stop-ship labels | Markdown, JSON |
| A3: Fit for Purpose | Testing/validation safeguards, human oversight requirements | Markdown (Policy Pack controls) |
| T2: Transparency Note | Transparency Note stub (system description, limitations, contact) | Markdown |
| PS1: Privacy | Data handling safeguards, GDPR/HIPAA controls | Markdown (Policy Pack controls) |
| PS2: Security | Adversarial testing, MITRE ATLAS controls | Markdown (Policy Pack controls) |

---

## Using This Tool with RAIS

### For Microsoft Teams:
1. **Initial triage:** Use the RAI Toolkit to quickly assess if a system requires formal Impact Assessment (IA)
2. **Impact Assessment input:** Export Decision Record as structured IA input (risk factors, affected populations, safeguards)
3. **Transparency Note drafting:** Use the Transparency Note stub as a starting template
4. **Policy alignment check:** Review triggered safeguards to confirm alignment with RAIS requirements

### For External Teams:
1. Adapt the RAIS alignment patterns to your organization's governance framework
2. Use the tool's output as a governance conversation starter with legal/compliance
3. Customize policy packs (YAML files) to encode your organization's specific requirements

---

## Important Caveats

⚠️ **This is a demonstration tool, not an official Microsoft product or assessment.**

- **Not authoritative:** This crosswalk is based on publicly available RAIS documentation and does not represent Microsoft's internal processes
- **Not comprehensive:** Real RAIS assessments involve additional artifacts, stakeholder reviews, and approval workflows not captured here
- **Illustrative only:** Gating rules, sensitive use criteria, and thresholds are examples for educational purposes
- **Validate with experts:** Always engage legal, privacy, security, and compliance teams for production assessments

**References:**
- [Microsoft Responsible AI](https://www.microsoft.com/en-us/ai/responsible-ai)
- [RAIS goals and principles](https://www.microsoft.com/en-us/ai/responsible-ai-resources)
- [Transparency Notes guidance](https://www.microsoft.com/en-us/ai/responsible-ai-resources)

---

## See Also

- [`common/utils/exporters.py`](/common/utils/exporters.py) — Decision Record generation logic
- [`common/utils/exporters_transparency_note.py`](/common/utils/exporters_transparency_note.py) — Transparency Note stub generation
- [`docs/methodology_project1.md`](/docs/methodology_project1.md) — Risk scoring methodology
- [`docs/samples/sample_decision_record.md`](/docs/samples/sample_decision_record.md) — Example Decision Record

