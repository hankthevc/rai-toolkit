# Case Study 2: Internal Code Copilot for DevOps Team

## Scenario Narrative

TechFlow Solutions is deploying GitHub Copilot and a custom fine-tuned code completion model to accelerate their internal DevOps team's productivity. The system assists with infrastructure-as-code (Terraform), CI/CD pipeline configuration (GitHub Actions), and Python automation scripts.

**Key Characteristics:**
- **No PII processing**: Works exclusively with infrastructure code and automation scripts; no customer data or personal information
- **Internal-only**: Accessible only to 12 DevOps engineers on the company VPN; not customer-facing
- **Low-stakes**: Mistakes result in failed deployments caught by staging environments and manual review; no direct impact on safety, rights, or critical infrastructure
- **Minimal autonomy (level 0)**: Suggests code; engineers review and approve all changes before merging
- **General sector**: Standard enterprise software development
- **No special modifiers**: No bio, cyber-critical, disinformation, or children-related risks

**Business Context:**
The goal is to reduce boilerplate code writing time by 25% and help junior engineers learn Terraform best practices through real-time suggestions. The worst-case scenario is inefficient code or a broken staging environment—caught by existing code review and CI/CD gates.

## Risk Assessment Inputs

Using the Frontier AI Risk Assessment Framework:

| Parameter | Value | Contribution |
|-----------|-------|--------------|
| Contains PII | ✗ No | 0 |
| Customer-facing | ✗ No | 0 |
| High-stakes | ✗ No | 0 |
| Autonomy level | 0 (Suggestions only) | 0 |
| Sector | General | 0 |
| Modifiers | None | 0 |

**Total Risk Score:** 0  
**Risk Tier:** **Low**

## Generated Decision Record

Below is the actual Decision Record export from the framework:

---

# Frontier AI Risk Decision Record

**Scenario Owner:** Alex Kim (Director of DevOps)  
**Approver:** Maya Patel (VP of Engineering)  
**Assessment Date:** 2024-10-07  
**Next Review Due:** 2025-01-05

## Summary
- **Risk Tier:** Low
- **Risk Score:** 0
- **Key Drivers:** None captured

## Scenario Inputs
- Contains PII: No
- Customer Facing: No
- High Stakes: No
- Autonomy Level: 0
- Sector: General
- Modifiers: None

## Required Safeguards

No controls matched the scenario inputs. Review policy packs for coverage gaps.

---
*Illustrative governance-as-code export. Validate safeguards with legal, compliance, and security teams before implementation.*

## Analysis & Commentary

### Why This Matters

This scenario demonstrates the **opposite end of the risk spectrum** from the healthcare chatbot. With a risk score of zero and **Low** tier classification, the framework correctly identifies that minimal governance overhead is appropriate.

The "No controls matched" outcome is **intentional, not a bug**. Internal developer tools with human-in-the-loop review don't require the same formalization as customer-facing or high-stakes systems.

### Governance Considerations (Even for Low Risk)

While the Decision Record shows zero mandatory controls, responsible teams should still implement basic safeguards:

#### Recommended (Non-Mandatory) Practices

1. **Code Review Gates**  
   - All Copilot-suggested code must pass peer review before merging
   - Senior engineers review infrastructure changes (Terraform state modifications)
   - *Why it's not formalized*: Standard engineering practice, not AI-specific

2. **License Compliance Scanning**  
   - Use tools like `licensee` or GitHub's dependency graph to catch GPL-licensed snippets
   - Block commits containing restrictive licenses incompatible with company policy
   - *Why it's not formalized*: General open-source hygiene, applies to all code sources

3. **Secret Detection**  
   - Run `trufflehog` or `detect-secrets` in CI pipeline
   - Prevent accidental commits of AWS keys, API tokens, or passwords
   - *Why it's not formalized*: Pre-existing security requirement independent of AI use

4. **Usage Monitoring**  
   - Track Copilot acceptance rates and engineer satisfaction
   - Identify patterns of over-reliance or underutilization
   - *Why it's not formalized*: Product analytics, not risk mitigation

#### When to Re-Assess

The risk tier **changes** if:

- **Autonomy increases**: If the company adopts auto-commit bots that merge Copilot suggestions without review → autonomy level 2 → score +2 → **Medium** tier
- **Scope expands to customer data**: If Copilot fine-tuning uses customer database schemas or application code handling PII → PII flag → score +2 → **Low** tier (still), but PII-specific controls would trigger
- **External exposure**: If Copilot suggestions are embedded in public documentation or open-source contributions → customer-facing → score +2 → **Low** tier, but transparency controls activate

### Comparison to Healthcare Chatbot

| Dimension | Internal Copilot | Healthcare Chatbot |
|-----------|------------------|-------------------|
| **Risk Score** | 0 | 12 |
| **Risk Tier** | Low | Critical |
| **Mandatory Controls** | 0 | 15 |
| **Approval Chain** | Team lead (informal) | VP + CAIO (formal) |
| **Testing Requirements** | Standard unit tests | Adversarial red-teaming |
| **Documentation** | README + ADRs | Impact assessment + conformity |
| **Review Cadence** | Annual (or as-needed) | Quarterly (mandatory) |

### False Negative Check

**Could this scenario hide risk?** Three potential blind spots:

1. **Training Data Provenance**: If the fine-tuned model was trained on proprietary customer code without permission, IP/privacy issues exist—but the framework doesn't capture this. *Mitigation*: Future policy pack should add "data provenance" modifier.

2. **Insider Threat**: Malicious engineer could use Copilot to obscure backdoors in generated code. *Mitigation*: Code review and static analysis (SAST) are standard gates, unrelated to AI risk tier.

3. **Overconfidence**: Junior engineers might trust incorrect Copilot suggestions without verification. *Mitigation*: Training and onboarding topic, not governance-as-code concern.

**Assessment**: None of these elevate the tier. The scenario remains **Low** risk with zero mandatory controls.

### Lessons for Similar Scenarios

- **Autonomy matters more than AI presence**: A human-reviewed AI assistant is lower risk than a fully automated non-AI script that deploys infrastructure changes.
  
- **Internal vs. external is a bright line**: Even if Copilot processed PII, staying internal keeps it Low tier (score would be 2). Customer exposure triggers the jump to Medium.

- **Coverage gaps are features, not bugs**: Governance-as-code should bias toward parsimony for low-risk scenarios. Over-formalizing internal tools creates bureaucratic drag without safety benefit.

### Implementation Notes

**What to Document:**
- One-page decision memo confirming Low tier assessment
- Link to this case study in the team wiki
- Next review date (annual unless scope changes)

**What NOT to Document:**
- Formal impact assessments
- Executive approval memos
- Quarterly compliance reports

**Stakeholder Communication:**
"We assessed the DevOps Copilot using our AI risk framework. It scored 0/15 (Low tier) because it's internal-only, suggestion-based, and reviewed by engineers before deployment. Standard code review and CI/CD gates provide sufficient oversight. We'll re-assess if we increase autonomy or expand to customer-facing use cases."

## Conclusion

This case study demonstrates that the Frontier AI Risk Assessment Framework **correctly de-escalates** low-risk scenarios. The absence of mandatory controls is the right outcome—governance should be proportional to risk, not bureaucratic by default.

For similar internal tooling assessments, use this case study as a template to explain why minimal formalization is appropriate and when re-assessment triggers should fire.

