# 💬 AI Interview Mode - Multi-Turn Governance Assessment

**Status:** ✅ Fully implemented  
**Added:** October 9, 2025

---

## The Problem

One-shot AI analysis has a fundamental limitation: **ambiguity**. 

When a user says "chatbot for hospital patients," critical details are missing:
- Does it access medical records (HIPAA)?
- What's the autonomy level (EU AI Act)?
- Are patients elderly/disabled (ADA, accessibility)?
- Self-hosted or external API (supply chain risk)?

A single AI analysis must **guess** at these details, leading to either:
1. Generic assessments that miss key risks
2. Over-conservative assessments that flag everything as high-risk

---

## The Solution: AI-Powered Interview Mode

Instead of one-shot analysis, the AI now conducts a **multi-turn interview** asking targeted clarifying questions before final assessment.

### User Experience Flow

**Step 1: Initial Description**
User pastes: "A chatbot that helps hospital patients schedule appointments and refill prescriptions"

**Step 2: Choose Mode**
- **💬 Interview Mode (Recommended)** ← AI asks clarifying questions
- **⚡ Quick Analysis** ← One-shot analysis (original behavior)

**Step 3: AI Asks Clarifying Questions**
```
🔍 Clarifying Questions for Comprehensive Assessment

The initial description lacks critical details about data handling (HIPAA), 
autonomy level (EU AI Act), vulnerable populations (civil rights), and technical 
architecture (supply chain risk). These details could shift the assessment from 
Medium to Critical tier.

Please answer these 4 questions to ensure accurate risk assessment:

Question 1: Does the chatbot access patient medical records (PHI) or just scheduling availability?
💡 Why this matters: If it processes PHI, HIPAA Privacy Rule applies and requires 
BAA with any third-party providers (HIPAA 45 CFR 164.308)

[text input for answer]

Question 2: Do appointments get booked automatically, or does a staff member review/approve before confirming?
💡 Why this matters: Autonomy level affects EU AI Act classification and human 
oversight requirements (EU AI Act Article 14)

[text input for answer]

...
```

**Step 4: User Answers**
User provides specific details for each question

**Step 5: AI Evaluates**
- **Either:** "Sufficient context gathered! Proceeding with analysis..." → Final assessment
- **Or:** Asks 2-3 follow-up questions based on answers → Loop back to Step 3

**Step 6: Comprehensive Final Analysis**
AI produces risk assessment enriched with all interview context, resulting in:
- More accurate risk tier
- More specific safeguards
- Better framework alignment
- Fewer false positives/negatives

---

## How It Works

### Interview Strategy

The AI is programmed to ask about:

**1. Ambiguities that affect risk tier:**
- "Customer-facing" → Public users or business partners?
- "AI suggests" → Human approves before or after action?
- "Medical records" → PHI under HIPAA or just scheduling data?

**2. Framework-specific requirements:**
- **GDPR:** "Where is data stored? Any cross-border transfers?"
- **HIPAA:** "Is there a BAA with third-party providers?"
- **EU AI Act:** "What's the autonomy level - does human review before impact?"
- **OWASP:** "For LLMs, is user input sanitized? Prompt injection defenses?"
- **Export controls:** "Could this be weaponized or used for surveillance?"

**3. High-risk indicators:**
- If healthcare + elderly → "What accessibility accommodations exist?"
- If LLM + customer-facing → "How do you handle hallucinations?"
- If real-time learning → "How do you prevent data poisoning?"
- If external API + PII → "What data goes to vendor? Contract terms?"

**4. Stop-ship triggers:**
- Critical + PII + irreversible → Legal review status?
- Protected populations → Bias testing completed?
- Dual-use risk → Export control classification obtained?

### Question Format

Each question includes:
- **The question** (specific and actionable)
- **Rationale** (why it matters for governance)
- **Framework reference** (HIPAA 164.308, EU AI Act Art. 14, etc.)

This educates users **while** gathering information.

---

## Example Interview Session

### Initial Description
"A chatbot that helps hospital patients schedule appointments and refill prescriptions"

### AI's First Round (4 questions)

**Q1:** Does the chatbot access patient medical records (PHI) or just scheduling availability?  
**Why:** If it processes PHI, HIPAA Privacy Rule applies and requires BAA with any third-party providers  
**Framework:** HIPAA 45 CFR 164.308

**Q2:** Do appointments get booked automatically, or does a staff member review/approve before confirming?  
**Why:** Autonomy level affects EU AI Act classification and human oversight requirements  
**Framework:** EU AI Act Article 14 (human oversight)

**Q3:** What percentage of your patients are elderly (65+) or have disabilities?  
**Why:** Protected populations trigger enhanced safeguards under ADA and age discrimination laws  
**Framework:** ADA Title III, Age Discrimination Act

**Q4:** Is the underlying AI model self-hosted or do you use an external API (like OpenAI)?  
**Why:** External APIs create data leakage risks and require vendor contract review for PHI  
**Framework:** NIST AI RMF MANAGE-3.2 (supply chain)

### User Answers

**A1:** "Yes, it accesses medical records to check medication history and insurance eligibility"  
**A2:** "The chatbot suggests appointment times automatically, but nurses must approve prescription refills"  
**A3:** "About 40% of our patients are 65+ and 15% have mobility/hearing disabilities"  
**A4:** "We use OpenAI's GPT-4 API"

### AI's Response

```
✅ Sufficient context gathered! Proceeding with comprehensive analysis...

[Produces final risk assessment with:]
- Risk Tier: Critical (score: 15)
- Rationale: PHI processing + healthcare + elderly population + external API + high stakes
- Triggered safeguards: HIPAA BAA, bias testing, accessibility audit, ADA compliance, etc.
- Framework alignment: EU AI Act Annex III (high-risk), HIPAA, ADA, NIST AI RMF
```

### Result

The interview revealed:
- ✅ PHI processing (not just scheduling) → HIPAA applies
- ✅ Nurse approval for prescriptions → Level 2 autonomy (not fully automated)
- ✅ 40% elderly + 15% disabled → Protected populations safeguards
- ✅ OpenAI API → Supply chain + BAA requirements

Without the interview, AI might have:
- ❌ Guessed "just scheduling" → Missed HIPAA requirements
- ❌ Assumed full autonomy → Overestimated risk
- ❌ Ignored accessibility → Missed ADA compliance

**The interview makes the difference between generic and actionable governance.**

---

## Technical Implementation

### New Module: `common/utils/ai_interviewer.py`

**Core Function:**
```python
def conduct_interview(
    initial_description: str,
    conversation_history: list[dict] = None,
    api_key: str = None,
) -> InterviewResponse
```

**Returns:**
```python
class InterviewResponse:
    needs_clarification: bool
    questions: list[InterviewQuestion]
    reasoning: str
    ready_for_analysis: bool
```

**Each Question:**
```python
class InterviewQuestion:
    question: str              # "Does the chatbot access PHI?"
    rationale: str             # "If yes, HIPAA Privacy Rule applies..."
    framework_reference: str   # "HIPAA 45 CFR 164.308"
```

### System Prompt Strategy

The interview prompt is **framework-aware**:
- References NIST AI RMF, EU AI Act, GDPR, HIPAA, OWASP, MITRE ATLAS, Export controls
- Asks about ambiguities that affect risk tier
- Drills into high-risk indicators
- Prioritizes questions (3-5 max per round)
- Uses plain language, not legal jargon

### Session State Management

**State variables:**
- `interview_mode` (bool) — Whether in interview flow
- `interview_history` (list) — Q&A pairs from all rounds
- `interview_questions` (InterviewResponse) — Current question set

**Flow control:**
- User clicks "Interview Mode" → Sets `interview_mode=True`
- AI asks questions → Stores in `interview_questions`
- User answers → Appends to `interview_history`
- AI evaluates → Either asks more OR sets `ready_for_analysis=True`
- Final analysis uses enriched description with all interview context

---

## Benefits

### For Accuracy
- **Fewer false positives:** Won't flag low-risk scenarios as Critical due to ambiguity
- **Fewer false negatives:** Won't miss HIPAA/GDPR requirements hidden in vague descriptions
- **Nuanced assessment:** Understands "nurse approves" vs "fully automated"

### For Education
- Users **learn** while answering (rationale + framework references)
- Understand **why** each detail matters
- See connections between technical choices and governance requirements

### For Compliance
- Creates **audit trail** of clarifying questions and answers
- Documents **what was considered** in risk assessment
- Shows **due diligence** in gathering context

### For Portfolio
- Demonstrates **conversational AI design**
- Shows **prompt engineering** for multi-turn flows
- Illustrates **governance depth** across frameworks
- Meta-governance: AI interviewing about AI governance

---

## Comparison: Interview Mode vs Quick Analysis

| Aspect | Interview Mode | Quick Analysis |
|--------|----------------|----------------|
| **Questions asked** | 3-10 (multi-round) | 0 |
| **Context gathered** | High (targeted questions) | Low (guesses from description) |
| **Accuracy** | Higher (fewer assumptions) | Lower (must guess ambiguities) |
| **Time** | 2-3 minutes | 30 seconds |
| **Education** | High (learns while answering) | Low (just sees results) |
| **Best for** | Production deployments | Quick demos, low-risk scenarios |

---

## User Guide

### When to Use Interview Mode

**✅ Use Interview Mode when:**
- Deploying to production (need accuracy)
- High-stakes scenarios (healthcare, finance, critical infrastructure)
- Protected populations involved (children, elderly, disabilities)
- Compliance documentation required (audit trail)
- Learning about governance frameworks

**⚡ Use Quick Analysis when:**
- Quick demos or prototypes
- Obviously low-risk scenarios (internal tools, suggestion-only)
- Time-constrained
- Already comprehensive description provided

### How to Write Good Answers

**✅ Good answers:**
- Specific: "40% of patients are 65+" not "Some elderly"
- Technical: "We use OpenAI GPT-4 API with BAA" not "An AI service"
- Complete: Answer the full question, not just part

**❌ Vague answers:**
- "I think so" → Specify yes/no
- "Pretty secure" → Describe actual controls
- "Standard stuff" → List specific safeguards

**The AI will ask follow-ups if answers are too vague.**

---

## Future Enhancements

1. **Smart follow-ups** — If answer is vague, auto-ask clarifying sub-question
2. **Framework-specific modes** — "HIPAA Interview" vs "EU AI Act Interview"
3. **Save interview templates** — Export Q&A for reuse on similar scenarios
4. **Multi-language** — Conduct interviews in Spanish, French, etc.
5. **Voice mode** — Audio interview for accessibility
6. **Pre-populated answers** — Auto-fill from organization profile
7. **Comparison mode** — Show how different answers change the risk tier

---

## API Cost Considerations

**Interview Mode:**
- Round 1: ~$0.01 (analyze + generate questions)
- Round 2 (if needed): ~$0.01 (evaluate answers + maybe more questions)
- Final analysis: ~$0.01 (comprehensive with full context)
- **Total: ~$0.02-0.03 per scenario**

**Quick Analysis:**
- One-shot: ~$0.01
- **Total: ~$0.01 per scenario**

**For demos:** Totally reasonable  
**For production at scale:** Consider GPT-4o-mini for question generation (save 90%)

---

## Deployment

**Files Changed:**
- `common/utils/ai_interviewer.py` — NEW file with interview logic
- `project1_risk_framework/app.py` — Added interview mode UI flow

**No Breaking Changes:**
- Quick Analysis still available (button renamed to "⚡ Quick Analysis")
- All existing functionality preserved
- Interview Mode is opt-in (user chooses)

**Commit Message:**
```
feat: Add AI Interview Mode for comprehensive multi-turn assessments

Replace one-shot analysis with intelligent interview flow:
- AI asks 3-5 clarifying questions tuned to governance frameworks
- Each question includes rationale + framework reference
- Multi-round conversation until sufficient context gathered
- Final analysis enriched with all interview context

Benefits:
- Higher accuracy (fewer false positives/negatives)
- Educational (users learn while answering)
- Audit trail (documents what was considered)
- Handles ambiguity better than one-shot guessing

Examples: "Does it access PHI?" (HIPAA 164.308), "What autonomy level?" 
(EU AI Act Art. 14), "Any elderly users?" (ADA, accessibility)

Quick Analysis still available for demos and obvious low-risk scenarios.
```

---

**Status:** ✅ Ready to deploy! This is a major leap forward in governance tooling. 🚀

