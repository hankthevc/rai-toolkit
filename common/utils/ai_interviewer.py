"""AI-powered interview mode for comprehensive scenario capture.

This module implements a multi-turn conversation where the AI asks clarifying
questions tuned to governance frameworks before producing final analysis.
"""

from __future__ import annotations

import os
from typing import Optional

from pydantic import BaseModel, Field

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class InterviewQuestion(BaseModel):
    """A single clarifying question from the AI interviewer."""
    
    question: str = Field(
        description="The clarifying question to ask the user"
    )
    rationale: str = Field(
        description="Why this question matters for governance assessment"
    )
    framework_reference: str = Field(
        description="Which governance framework or requirement this relates to"
    )


class InterviewResponse(BaseModel):
    """AI's response during the interview phase."""
    
    needs_clarification: bool = Field(
        description="Whether more information is needed before final analysis"
    )
    questions: list[InterviewQuestion] = Field(
        default_factory=list,
        description="List of clarifying questions to ask (1-5 as needed, only ask what's necessary)"
    )
    reasoning: str = Field(
        default="",
        description="Explanation of what's still unclear and why it matters"
    )
    ready_for_analysis: bool = Field(
        default=False,
        description="Whether enough context has been gathered for final analysis"
    )


INTERVIEW_SYSTEM_PROMPT = """You are an expert AI governance consultant conducting an initial assessment interview.

Your role is to ask targeted clarifying questions to ensure comprehensive risk assessment aligned with:
- NIST AI RMF (data governance, supply chain, human oversight)
- EU AI Act (high-risk criteria, transparency, human oversight)
- GDPR (data transfers, explainability, automated decision-making)
- HIPAA (for healthcare scenarios)
- OWASP LLM Top 10 (for generative AI)
- MITRE ATLAS (for ML security threats)
- Export controls (EAR/ITAR for dual-use scenarios)

**INTERVIEW STRATEGY:**

1. **Identify ambiguities** in the initial description that affect risk tier:
   - Is "customer-facing" public users or business partners?
   - Does "AI suggests" mean human approves before action, or after?
   - Is "medical records" PHI under HIPAA or just scheduling data?
   
2. **Ask framework-specific questions**:
   - GDPR: "Where is data stored? Any cross-border transfers?"
   - HIPAA: "Is there a BAA with third-party providers?"
   - EU AI Act: "What's the autonomy level - does a human review before impact?"
   - OWASP: "For LLMs, is user input sanitized? Any prompt injection defenses?"
   - Export controls: "Could this technology be weaponized or used for surveillance?"

3. **Drill into high-risk indicators**:
   - If healthcare + elderly → "What accessibility accommodations exist?"
   - If LLM + customer-facing → "How do you handle hallucinations?"
   - If real-time learning → "How do you prevent data poisoning?"
   - If external API + PII → "What data goes to the vendor? Contract terms?"

4. **Prioritize questions** (ask 1-5 as needed, be efficient):
   - What would most change the risk tier?
   - What's required for stop-ship rules? (e.g., Critical + PII + irreversible)
   - What's legally mandated? (e.g., GDPR Art. 22 for automated decisions)
   - **Only ask what you truly need** - if 1-2 questions are sufficient, stop there

5. **Format requirements**:
   - Each question should be specific and actionable
   - Include why it matters (the rationale)
   - Reference the relevant framework
   - Keep questions concise (1-2 sentences)

**GUIDELINES:**
- Ask about what's UNCLEAR, not what's already stated
- Be efficient: Ask 1-2 questions if that's sufficient, up to 5 max if needed
- If the description is comprehensive, set ready_for_analysis=True immediately
- Focus on details that affect compliance, not just curiosity
- Fewer, high-quality questions > exhaustive questioning
- Use plain language, not legal jargon

**EXAMPLE OUTPUT:**

For description: "A chatbot that helps hospital patients schedule appointments"

{
  "needs_clarification": true,
  "questions": [
    {
      "question": "Does the chatbot access patient medical records (PHI) or just scheduling availability?",
      "rationale": "If it processes PHI, HIPAA Privacy Rule applies and requires BAA with any third-party providers",
      "framework_reference": "HIPAA 45 CFR 164.308"
    },
    {
      "question": "Do appointments get booked automatically, or does a staff member review/approve before confirming?",
      "rationale": "Autonomy level affects EU AI Act classification and human oversight requirements",
      "framework_reference": "EU AI Act Article 14 (human oversight)"
    },
    {
      "question": "What percentage of your patients are elderly (65+) or have disabilities?",
      "rationale": "Protected populations trigger enhanced safeguards under ADA and age discrimination laws",
      "framework_reference": "ADA Title III, Age Discrimination Act"
    },
    {
      "question": "Is the underlying AI model self-hosted or do you use an external API (like OpenAI)?",
      "rationale": "External APIs create data leakage risks and require vendor contract review for PHI",
      "framework_reference": "NIST AI RMF MANAGE-3.2 (supply chain)"
    }
  ],
  "reasoning": "The initial description lacks critical details about data handling (HIPAA), autonomy level (EU AI Act), vulnerable populations (civil rights), and technical architecture (supply chain risk). These details could shift the assessment from Medium to Critical tier.",
  "ready_for_analysis": false
}

**YOUR TASK:**
Analyze the user's scenario description and determine what clarifying questions are needed before conducting a comprehensive risk assessment.
"""


def conduct_interview(
    initial_description: str,
    conversation_history: list[dict] = None,
    api_key: Optional[str] = None,
) -> Optional[InterviewResponse]:
    """Conduct AI governance interview to gather comprehensive context.
    
    Args:
        initial_description: User's initial use case description
        conversation_history: List of {"question": str, "answer": str} from previous turns
        api_key: OpenAI API key
        
    Returns:
        InterviewResponse with questions or ready_for_analysis=True
    """
    if OpenAI is None:
        raise ImportError("openai package not installed. Run: pip install openai")
    
    if not initial_description or not initial_description.strip():
        return None
    
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key required")
    
    # Build conversation context
    conversation_context = f"**Initial Description:**\n{initial_description}\n\n"
    
    if conversation_history:
        conversation_context += "**Previous Q&A:**\n"
        for i, turn in enumerate(conversation_history, 1):
            conversation_context += f"Q{i}: {turn['question']}\n"
            conversation_context += f"A{i}: {turn['answer']}\n\n"
    
    user_prompt = f"""{conversation_context}

Based on the information provided so far, do you need additional clarification before conducting a final risk assessment?

If yes, ask 3-5 targeted questions that would most impact the risk tier or compliance requirements.
If no (you have enough context), set ready_for_analysis=True."""
    
    try:
        client = OpenAI(api_key=api_key)
        
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": INTERVIEW_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format=InterviewResponse,
            temperature=0.5,  # Balanced between consistency and conversational
        )
        
        return completion.choices[0].message.parsed
        
    except Exception as e:
        print(f"Interview failed: {e}")
        import traceback
        print(traceback.format_exc())
        return None


def format_interview_questions(response: InterviewResponse) -> str:
    """Format interview questions for display in UI.
    
    Args:
        response: InterviewResponse from conduct_interview()
        
    Returns:
        Markdown-formatted questions with rationale
    """
    if response.ready_for_analysis:
        return "✅ **Sufficient information gathered.** Proceeding with comprehensive analysis..."
    
    output = f"### 🔍 I need a few more details\n\n"
    output += f"{response.reasoning}\n\n"
    output += f"**Please answer these {len(response.questions)} questions:**\n\n"
    
    for i, q in enumerate(response.questions, 1):
        output += f"**{i}. {q.question}**\n"
        output += f"*Why this matters:* {q.rationale}\n"
        output += f"*Framework:* {q.framework_reference}\n\n"
    
    return output

