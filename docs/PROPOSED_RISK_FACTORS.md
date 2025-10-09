# Proposed Additional Risk Factors for RAI Toolkit

## Current Risk Assessment Coverage

**Existing factors:**
- `contains_pii` — Data sensitivity
- `customer_facing` — External exposure
- `high_stakes` — Impact severity
- `autonomy_level` (0-3) — Human oversight
- `sector` — Domain-specific regulations
- `modifiers` — Bio, Cyber, Disinformation, Children

---

## 10 Proposed Additional Risk Factors

### 1. **Model Architecture Type** (`model_type`)
**Why it matters:** Different AI architectures have distinct risk profiles and threat models.

**Options:**
- `Traditional ML` (classification, regression, clustering)
- `Generative AI / LLM` (text generation, code generation)
- `Computer Vision` (image recognition, object detection)
- `Multimodal` (text + image + audio combinations)
- `Reinforcement Learning` (autonomous agents, game playing)

**Risk implications:**
- **LLMs:** Prompt injection, jailbreaking, data leakage, hallucinations (OWASP LLM Top 10)
- **Computer Vision:** Adversarial examples, deepfakes, bias in facial recognition (MITRE ATLAS)
- **Multimodal:** Increased attack surface, cross-modal attacks
- **RL:** Reward hacking, emergent behavior, safety specification failures

**Governance alignment:** NIST AI RMF MAP-1.1 (categorize AI system), EU AI Act Annex III risk categories

---

### 2. **Training Data Provenance** (`data_source`)
**Why it matters:** Data source determines poisoning risk, bias exposure, IP concerns, and compliance obligations.

**Options:**
- `Proprietary/Internal` — Company data, controlled curation
- `Public Datasets` — ImageNet, Common Crawl, academic benchmarks
- `Internet-Scraped` — Web crawling, social media
- `User-Generated` — Production data, customer inputs
- `Third-Party/Vendor` — Licensed datasets, data brokers
- `Synthetic` — AI-generated training data

**Risk implications:**
- **Internet-scraped:** Copyright issues, toxic content, bias amplification, PII contamination
- **User-generated:** Privacy risks, adversarial data injection, concept drift
- **Third-party:** Supply chain integrity, license compliance, audit rights

**Governance alignment:** NIST AI RMF GOVERN-1.5 (data governance), EU AI Act Art. 10 (data quality), ISO 42001 data management

---

### 3. **Real-Time Learning / Adaptation** (`learns_in_production`)
**Why it matters:** Online learning introduces drift, poisoning, and loss of reproducibility.

**Boolean flag:** Does the model update based on production data?

**Risk implications:**
- **Yes:** Data poisoning attacks, adversarial feedback loops, concept drift, loss of auditability
- **No:** Static model, reproducible, easier to validate but may degrade over time

**Governance alignment:** NIST AI RMF MANAGE-1.2 (continuous monitoring), MITRE ATLAS AML.T0018 (online learning poisoning)

---

### 4. **Cross-Border Data Transfers** (`international_data`)
**Why it matters:** Data sovereignty, GDPR/CPRA adequacy decisions, national security concerns.

**Boolean flag:** Does the system transfer personal data across jurisdictions?

**Risk implications:**
- Schrems II invalidation risk
- Export control violations (EAR, ITAR for AI models)
- Conflicting legal obligations (CLOUD Act vs GDPR)
- National security review triggers (CFIUS, EU FDI screening)

**Governance alignment:** GDPR Art. 44-50, EU AI Act Art. 85 (international cooperation), US OMB AI Policy M-24-10

---

### 5. **Explainability / Interpretability** (`explainability_level`)
**Why it matters:** Black-box models trigger regulatory obligations and limit incident investigation.

**Options:**
- `Inherently Interpretable` (linear models, decision trees, rule-based)
- `Post-hoc Explainable` (SHAP, LIME, attention visualization)
- `Limited Explainability` (complex ensembles, some neural nets)
- `Black Box` (foundation models, proprietary APIs)

**Risk implications:**
- **Black box:** GDPR Art. 22 right to explanation, EU AI Act transparency obligations, hard to debug failures
- **Interpretable:** Easier audits, better incident response, user trust

**Governance alignment:** GDPR Art. 22, EU AI Act Art. 13 (transparency), NIST AI RMF MANAGE-3.2 (explainability)

---

### 6. **Third-Party Model Dependencies** (`uses_foundation_model`)
**Why it matters:** Supply chain risk, vendor lock-in, data leakage to external providers.

**Options:**
- `Self-Hosted Open Source` (Llama, Mistral on own infrastructure)
- `Self-Hosted Proprietary` (licensed models on-prem)
- `External API` (OpenAI, Anthropic, Google APIs)
- `Hybrid` (RAG with external embeddings + internal retrieval)
- `No Third-Party` (fully in-house model)

**Risk implications:**
- **External API:** Data sent to third party, terms of service changes, rate limits, geopolitical access restrictions
- **Open source:** Model supply chain attacks, licensing compliance, ongoing maintenance burden

**Governance alignment:** NIST AI RMF MAP-1.5 (supply chain), EU AI Act Art. 61 (supply chain obligations), ISO 42001 vendor management

---

### 7. **Synthetic Content Generation** (`generates_synthetic_content`)
**Why it matters:** Deepfakes, misinformation, provenance tracking obligations.

**Boolean flag:** Does the system create text, images, audio, or video?

**Risk implications:**
- Deepfakes for fraud/blackmail
- Misinformation at scale
- Copyright infringement (style mimicry)
- Watermarking/provenance requirements (C2PA, Adobe CAI)

**Governance alignment:** EU AI Act Art. 52 (synthetic content transparency), NIST AI RMF GOVERN-4.3 (societal impacts), C2PA standards

---

### 8. **Decision Reversibility** (`decision_reversible`)
**Why it matters:** Irreversible decisions require higher safeguards (right to appeal).

**Options:**
- `Fully Reversible` — Decisions can be undone without harm (content recommendations)
- `Reversible with Cost` — Can appeal but with time/money cost (loan denial)
- `Difficult to Reverse` — Significant harm to undo (reputation damage from content moderation)
- `Irreversible` — Cannot undo (autonomous weapons, some medical interventions)

**Risk implications:**
- **Irreversible:** Requires human oversight, appeals process, higher accuracy thresholds
- **Reversible:** Lower risk tolerance acceptable

**Governance alignment:** GDPR Art. 22 (right to human review), EU AI Act Art. 14 (human oversight), NIST AI RMF MANAGE-2.3

---

### 9. **Dual-Use Potential** (`dual_use_risk`)
**Why it matters:** Technologies designed for beneficial use can be weaponized or abused.

**Options:**
- `None` — Single benign purpose
- `Low` — Minimal misuse potential
- `Moderate` — Could be adapted for harmful use (facial recognition → surveillance)
- `High` — Direct dual-use (biological research AI, cyber tools, persuasion systems)

**Risk implications:**
- Export controls (EAR, Wassenaar Arrangement)
- Misuse research ethics (AI safety red-teaming)
- Terms of service restrictions
- Government access requests (lawful intercept, surveillance)

**Governance alignment:** White House EO 14110 (dual-use foundation models), NIST AI RMF GOVERN-4.3, Wassenaar Arrangement intrusion software controls

---

### 10. **Vulnerable / Protected Populations** (`protected_populations`)
**Why it matters:** Enhanced protections for groups at heightened risk.

**Options (multi-select):**
- `Children` (existing)
- `Elderly` — Cognitive decline, digital literacy, elder fraud
- `People with Disabilities` — Accessibility, discriminatory denial of accommodations
- `Low-Income / Unbanked` — Financial exclusion, predatory systems
- `Non-Native Speakers / Low Literacy` — Language barriers, comprehension of AI disclosures
- `Asylum Seekers / Immigrants` — Life-or-death decisions, due process
- `Incarcerated Persons` — Parole/sentencing algorithms, limited recourse
- `Healthcare Vulnerable` — Terminal illness, cognitive impairment, medical decision-making

**Risk implications:**
- Heightened scrutiny under civil rights law (ADA, Fair Housing Act, ECOA)
- EU AI Act prohibited uses (social scoring, emotion recognition in workplaces/schools)
- Ethical obligations beyond legal compliance

**Governance alignment:** EU AI Act Art. 5 (prohibited uses), NIST AI RMF GOVERN-5.1 (equity), US OMB M-24-10 (safety-impacting decisions)

---

## Implementation Priorities

### High Priority (Immediate Impact)
1. **Model Architecture Type** — Determines threat model (OWASP LLM vs MITRE ATLAS computer vision)
2. **Explainability Level** — Triggers regulatory obligations (GDPR, EU AI Act)
3. **Third-Party Model Dependencies** — Supply chain risk is top concern for 2024-2025
4. **Synthetic Content Generation** — Hot-button issue (deepfakes, provenance standards)

### Medium Priority (Governance Depth)
5. **Training Data Provenance** — Shows data governance sophistication
6. **Decision Reversibility** — Aligns with right-to-appeal requirements
7. **Protected Populations** — Demonstrates civil rights/equity awareness

### Lower Priority (Specialist Knowledge)
8. **Real-Time Learning** — More technical, shows ML Ops understanding
9. **Cross-Border Data** — Important for global orgs, less universal
10. **Dual-Use Potential** — National security niche, shows breadth

---

## How to Add Them

### Code Changes Needed

1. **Update `RiskInputs` model** (`common/utils/risk_engine.py`):
   ```python
   class RiskInputs(BaseModel):
       # ... existing fields ...
       model_type: str = "Traditional ML"
       data_source: str = "Proprietary/Internal"
       learns_in_production: bool = False
       international_data: bool = False
       explainability_level: str = "Post-hoc Explainable"
       uses_foundation_model: str = "No Third-Party"
       generates_synthetic_content: bool = False
       decision_reversible: str = "Fully Reversible"
       dual_use_risk: str = "None"
       protected_populations: List[str] = Field(default_factory=list)
   ```

2. **Update weights** in `calculate_risk_score()`:
   ```python
   # Example weights
   if inputs.learns_in_production:
       score += 2
       factors.append("Real-time learning (+2)")
   
   if inputs.generates_synthetic_content and inputs.customer_facing:
       score += 2
       factors.append("Public synthetic content generation (+2)")
   
   explainability_weights = {
       "Black Box": 2,
       "Limited Explainability": 1,
       "Post-hoc Explainable": 0,
       "Inherently Interpretable": 0
   }
   ```

3. **Update Streamlit form** (`project1_risk_framework/app.py`):
   - Add dropdowns for categorical fields
   - Add checkboxes for boolean fields
   - Add multiselect for protected populations

4. **Update AI parser** (`common/utils/ai_parser.py`):
   - Extend `ScenarioAnalysis` Pydantic model
   - Enhance system prompt to extract these factors

5. **Update policy packs** (`common/policy_packs/*.yaml`):
   - Add `when` conditions for new factors
   - Example: `uses_foundation_model: ["External API"]` → triggers supply chain controls

---

## Demo Value for Hiring Managers

**Showing breadth across:**
- ✅ **ML/AI technical risks** — Model types, training data, real-time learning
- ✅ **Privacy/data governance** — Cross-border, data provenance, PII
- ✅ **Security threats** — Dual-use, supply chain, adversarial ML
- ✅ **Regulatory compliance** — GDPR explainability, EU AI Act synthetic content, protected populations
- ✅ **Ethics & equity** — Vulnerable populations, decision reversibility
- ✅ **Emerging risks** — Foundation model dependencies, synthetic content

This positions you as someone who understands AI governance **holistically**, not just one dimension.

---

## Suggested Next Steps

1. **Phase 1:** Add 3 high-priority factors (model type, explainability, foundation models)
2. **Phase 2:** Update AI parser to extract these from plain-language descriptions
3. **Phase 3:** Create policy pack controls that trigger on new factors
4. **Phase 4:** Add remaining 7 factors for comprehensive coverage
5. **Document:** Write case study showing how all factors interact for a complex scenario

---

*This expansion demonstrates knowledge spanning NIST AI RMF, EU AI Act, GDPR, OWASP, MITRE ATLAS, supply chain security, civil rights law, and AI safety research—showing you're ready for senior governance roles.*

