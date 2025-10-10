# RAI Toolkit — Portfolio Overview

**Henry Appel** | AI Security Strategist | [henryappel@gmail.com](mailto:henryappel@gmail.com)

---

## Project Summary

**RAI Toolkit** is a governance-as-code demonstration showing how AI risk assessment, policy enforcement, and decision documentation can operate inside a single executable workflow. Built to showcase the intersection of AI security, threat modeling, and executive operations—translating frameworks like NIST AI RMF, EU AI Act, and OWASP LLM Top 10 into working code.

**🚀 [Live Demo](https://rai-toolkit.streamlit.app/)** | **📂 [GitHub Repository](https://github.com/hankthevc/rai-toolkit)**

---

## What It Demonstrates

### 1. **Technical Execution**
- **AI-powered scenario parsing (NEW)** using OpenAI API with structured outputs to auto-fill risk assessments from plain-language descriptions—demonstrating LLM integration in governance workflows
- **Python/Streamlit application** with risk calculator, policy engine, and exportable decision records
- **YAML-encoded policy packs** with conditional logic for safeguard assignment
- **Transparent scoring model** that teams can defend in audits and compliance reviews
- **CI/CD pipeline** (GitHub Actions) running automated tests on policy pack integrity
- **Interactive analytics dashboard** with 8+ visualizations for governance trends

### 2. **Policy Translation**
- Converted 6 major AI governance frameworks into executable safeguards:
  - NIST AI RMF (Govern/Map/Measure/Manage)
  - EU AI Act (Article 6 risk tiers, transparency obligations)
  - ISO/IEC 42001 (AI management systems)
  - U.S. OMB AI Policy (federal inventory/impact assessment)
  - OWASP LLM Top 10 (prompt injection, data leakage)
  - MITRE ATLAS (adversarial ML tactics)
- Each safeguard includes policy citations and applicability conditions

### 3. **Threat Modeling & Risk Assessment**
- **Additive risk model** scoring scenarios across 7 dimensions (autonomy, PII, customer-facing, etc.)
- **4-tier classification** (Low/Medium/High/Critical) aligned with EU AI Act risk categories
- **Real-world case studies** demonstrating:
  - Healthcare chatbot (Critical tier, 15 safeguards, PHI protection)
  - Internal code copilot (Low tier, appropriate de-escalation)
  - Hiring assessment platform (Critical tier, employment AI obligations)

### 4. **Cross-Functional Communication**
- Framework crosswalk documents tailored for compliance, security, and engineering audiences
- Exportable Decision Records (Markdown) for ticketing systems and audit trails
- Educational documentation and clear methodology guides

---

## Key Technical Components

### Risk Engine (`common/utils/risk_engine.py`)
Transparent additive scoring model with configurable weights:
```python
score = base_autonomy_score + Σ(risk_modifiers)
tier = f(score) → {Low, Medium, High, Critical}
```

### Policy Packs (`common/policy_packs/`)
YAML-encoded safeguards with conditional applicability:
```yaml
- control_id: "NIST-GV-1.3"
  description: "Establish AI incident response procedures"
  applies_to:
    risk_tiers: ["Medium", "High", "Critical"]
    modifiers: ["customer_facing", "automated_decision"]
  references:
    - framework: "NIST AI RMF"
      citation: "GOVERN 1.3"
```

### Decision Record Exporter (`common/utils/exporters.py`)
Generates audit-ready Markdown files with:
- Risk tier and score breakdown
- All triggered safeguards with policy citations
- Review metadata (timestamp, ownership, next review date)

---

## Skills Demonstrated

| Category | Details |
|----------|---------|
| **AI/LLM Integration** | OpenAI API integration with structured outputs, prompt engineering for governance tasks, AI-assisted workflows |
| **AI Security** | Adversarial ML frameworks (MITRE ATLAS), LLM threat modeling (OWASP Top 10), red-team scenario design |
| **Policy-as-Code** | Translating regulatory requirements into executable logic, maintaining traceability to source frameworks |
| **Python Development** | Streamlit UIs, pytest test suites, Pydantic models, modular architecture, CI/CD automation |
| **Threat Intelligence** | Risk scoring methodologies, incident response workflows, data classification schemes |
| **Executive Operations** | Decision memos (Decision Records), stakeholder communication (crosswalks), audit preparation |

---

## Use Cases in Interviews

### For AI Security Roles
- **"How do you approach threat modeling for LLMs?"**  
  → Walk through the OWASP LLM Top 10 integration, showing how prompt injection and data leakage risks trigger specific safeguards
  
- **"Show me an adversarial simulation you've designed."**  
  → Explain the Healthcare Chatbot case study's adversarial testing requirements (triggered by Critical tier + PII modifiers)

### For Responsible AI / AI Governance Roles
- **"How do you bridge policy and engineering teams?"**  
  → Demonstrate the YAML policy packs: engineers read conditional logic, compliance reads policy citations
  
- **"How do you handle competing framework requirements?"**  
  → Show the framework crosswalk documents mapping NIST AI RMF ↔ EU AI Act ↔ ISO 42001

### For Chief of Staff / Executive Operations Roles
- **"How do you create decision artifacts for executives?"**  
  → Show the Decision Record export feature: 2-minute scenario → executive-ready memo with risk tier, controls, and next actions
  
- **"How do you manage cross-functional workflows?"**  
  → Walk through the end-to-end intake process from scenario submission → risk scoring → safeguard assignment → export

---

## Project Metrics

- **AI-powered auto-fill** using GPT-4o with structured outputs (NEW)
- **6 governance frameworks** encoded as policy packs
- **60+ safeguards** with conditional applicability logic
- **3 detailed case studies** spanning healthcare, internal tooling, hiring
- **8+ analytics visualizations** for governance trend analysis
- **Full CI/CD pipeline** with automated testing
- **< 30 seconds** from plain-language description → AI analysis → risk-assessed Decision Record
- **Educational documentation** with clear methodology guides and framework crosswalks

---

## Background Context

I built this toolkit to demonstrate how AI governance can move from policy documents to executable systems. As a former NSC policy advisor who coordinated 12 agencies on commercial spyware and ran intelligence downgrades for election protection, I've seen firsthand how governance processes break down when policy, security, and engineering teams speak different languages.

This project shows governance-as-code in practice:
- **Policy teams** see familiar framework citations (NIST, EU AI Act, ISO 42001)
- **Security teams** see threat modeling (OWASP, MITRE ATLAS) and risk tiers
- **Engineering teams** see clean Python code with transparent logic
- **Executives** get 2-minute decision records with clear ownership and timelines

Now working as an AI security researcher at 2430 Group, I design red-team frameworks for frontier systems and brief leadership on mitigations and IP-protection risks. This toolkit applies that same bridge-building approach to responsible AI governance.

---

## Links & Resources

- **Live Demo:** https://rai-toolkit.streamlit.app/
- **GitHub Repository:** https://github.com/hankthevc/rai-toolkit
- **Case Studies:** [Healthcare Chatbot](https://github.com/hankthevc/rai-toolkit/blob/main/docs/case_studies/01_healthcare_chatbot.md) | [Code Copilot](https://github.com/hankthevc/rai-toolkit/blob/main/docs/case_studies/02_internal_code_copilot.md) | [Hiring Platform](https://github.com/hankthevc/rai-toolkit/blob/main/docs/case_studies/03_hiring_assessment_tool.md)
- **Framework Crosswalks:** [NIST AI RMF](https://github.com/hankthevc/rai-toolkit/blob/main/docs/crosswalks/nist_ai_rmf.md) | [EU AI Act](https://github.com/hankthevc/rai-toolkit/blob/main/docs/crosswalks/eu_ai_act.md) | [OWASP LLM Top 10](https://github.com/hankthevc/rai-toolkit/blob/main/docs/crosswalks/owasp_llm_top10.md)

---

## Professional Profile

**Henry Appel**  
AI Security Strategist | Former White House NSC Policy Advisor

- **Current:** AI Security Researcher, 2430 Group (2025–Present)  
  Red-team frameworks for frontier systems; nation-state attack path simulation; executive briefings on mitigations and IP risks

- **Previous:** Policy Advisor for Intelligence Programs, White House NSC (2023–2024)  
  Coordinated 12 agencies + 30 international partners against commercial spyware; focal point for AI-related intelligence; ran downgrades protecting U.S. elections

- **IC Experience:** ODNI/NCTC Analyst (2018–2025)  
  PRC/DPRK cyber operations, ransomware, commercial spyware; CIA Career Analyst Program; overseas HUMINT deployments

- **Education:** M.A. Security Studies, Georgetown (2019) | B.A. Government/International Affairs, Claremont McKenna (2015)

- **Languages:** Hindi/Urdu (advanced-mid), German (low-mid)

**Contact:** [henryappel@gmail.com](mailto:henryappel@gmail.com) | Washington, DC

---

*This portfolio document is optimized for sharing with hiring managers, recruiters, and technical interviewers. For questions about the project or collaboration opportunities, reach out via email or GitHub issues.*

