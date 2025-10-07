# Real-World Case Studies

This directory contains detailed case studies demonstrating how the Frontier AI Risk Assessment Framework evaluates realistic scenarios across the risk spectrum. Each case study includes:

- **Scenario narrative** with business context
- **Risk assessment inputs** with scoring breakdown
- **Generated Decision Record** (actual framework export)
- **Analysis & commentary** explaining control selection
- **Implementation priorities** and lessons learned

## Case Studies Overview

### [1. Healthcare Patient Support Chatbot](01_healthcare_chatbot.md)
**Risk Tier:** Critical (score: 12)  
**Controls Triggered:** 15

A customer-facing medical chatbot processing protected health information (PHI). Demonstrates maximum governance requirements when PII, high-stakes outcomes, and healthcare sector combine. Shows how EU AI Act, NIST AI RMF, ISO 42001, OWASP, MITRE ATLAS, and U.S. OMB controls stack for defense-in-depth.

**Key Takeaways:**
- Critical tier requires C-suite accountability across multiple frameworks
- Healthcare + customer-facing + autonomy = compounding risk
- Technical security (adversarial testing) and human oversight both mandatory
- 15 controls span governance, technical testing, privacy engineering, and monitoring

---

### [2. Internal Code Copilot for DevOps Team](02_internal_code_copilot.md)
**Risk Tier:** Low (score: 0)  
**Controls Triggered:** 0

An AI coding assistant used exclusively by internal engineers with human review gates. Demonstrates that the framework correctly de-escalates low-risk scenarios and avoids bureaucratic overhead for internal tooling.

**Key Takeaways:**
- Zero mandatory controls is the **correct outcome** for internal, suggestion-only tools
- Autonomy level 0 (human-reviewed) keeps risk minimal regardless of AI capabilities
- Re-assessment triggers defined (autonomy increase, external exposure, PII processing)
- Governance should be proportional; internal tools don't need conformity assessments

---

### [3. AI-Powered Hiring Assessment Platform](03_hiring_assessment_tool.md)
**Risk Tier:** Critical (score: 9)  
**Controls Triggered:** 11

A customer-facing platform that ranks job candidates using resume analysis, video interviews, and coding challenges. Demonstrates employment AI's unique risk profile under EU AI Act and identifies policy pack gaps around fairness/bias.

**Key Takeaways:**
- Employment decisions are high-risk even without healthcare/finance sector classification
- EU AI Act explicitly categorizes hiring as high-risk (mandatory third-party conformity assessment)
- Framework gaps identified: missing "Fairness" modifier and "Employment" sector
- Real-world precedents (Amazon recruiting tool, HireVue audit) validate control necessity

---

## Using These Case Studies

### For Interviews
Reference these when explaining your governance-as-code approach:
- *"I validated the framework against three realistic scenarios—a healthcare chatbot, internal dev tooling, and hiring AI—to ensure it correctly escalates high-risk cases and de-escalates low-risk ones."*

### For Product Development
Use as templates when assessing new AI systems:
1. Map your scenario to the closest case study
2. Adjust inputs based on differences (e.g., higher autonomy, different sector)
3. Review triggered controls to estimate compliance workload
4. Adapt implementation priorities to your team's capacity

### For Policy Pack Authoring
Case studies surface **coverage gaps** that inform future policy pack iterations:
- Case Study 3 identified missing "Fairness" modifier → roadmap for v0.2
- Healthcare case noted lack of explainability controls → potential ISO 42001 addition
- Cross-study analysis shows NIST-GOV-01 (executive accountability) triggers in all Critical scenarios → validates weight distribution

### For Stakeholder Communication
Each case study includes communication templates for:
- **Sales/Marketing**: Positioning governance rigor as competitive advantage
- **Legal/Compliance**: Demonstrating framework alignment with regulations
- **Engineering**: Translating controls into technical requirements

---

## Methodology Notes

### Score Calculation
Each case study shows the **additive scoring breakdown**:
```
Score = (PII × 2) + (Customer-facing × 2) + (High-stakes × 3) + (Autonomy level) + (Sector bump) + (Σ Modifiers)
```

### Tier Thresholds
- **Low:** 0-2 points
- **Medium:** 3-5 points
- **High:** 6-8 points
- **Critical:** 9+ points

### Control Matching Logic
Controls trigger when scenario attributes match the `when` clause in policy pack YAML files. A control with:
```yaml
when:
  tier: ["High", "Critical"]
  contains_pii: true
```
...will apply to scenarios with (High OR Critical) tier **AND** PII flag set.

---

## Future Case Studies (Roadmap)

Planned additions for comprehensive coverage:

- **Financial fraud detection model** (Finance sector, High tier, model explainability focus)
- **Content moderation AI** (Disinformation modifier, customer-facing, bias/fairness)
- **Autonomous vehicle perception** (Critical Infrastructure, Bio/Cyber modifiers, safety-critical)
- **Educational tutoring chatbot** (Children modifier, moderate autonomy)

Contributions welcome! See [CONTRIBUTING.md](../../CONTRIBUTING.md) for case study authoring guidelines.

---

## Validation & Disclaimer

These case studies use **illustrative policy mappings** for educational purposes. Before deploying similar systems:
- Validate framework clauses with legal counsel
- Conduct jurisdiction-specific compliance reviews (GDPR, CCPA, etc.)
- Engage third-party auditors for high-risk systems (EU AI Act Article 43)

The scenarios are realistic but fictional. Any resemblance to actual products is coincidental.

