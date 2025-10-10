"""Centralized OpenAI API calls with error handling and demo mode."""

from __future__ import annotations

import time
from typing import Any, Dict

from pydantic import BaseModel


def safe_openai_call(
    messages: list[Dict[str, str]],
    *,
    model: str = "gpt-4o",
    temperature: float = 0.2,
    response_format: type[BaseModel] | None = None,
    max_retries: int = 2,
    demo_mode: bool = False,
    api_key: str | None = None,
) -> Dict[str, Any]:
    """
    Centralized OpenAI API call with retry logic and demo mode fallback.
    
    Args:
        messages: List of chat messages
        model: OpenAI model name
        temperature: Sampling temperature
        response_format: Pydantic model for structured output
        max_retries: Number of retries on 429/5xx errors
        demo_mode: If True, return canned response instead of API call
        api_key: OpenAI API key
    
    Returns:
        Dict with either:
        - {"success": True, "data": parsed_object} on success
        - {"success": False, "error": error_message} on failure
    """
    
    # Demo mode: return canned response
    if demo_mode:
        return _get_demo_response(response_format)
    
    # Check API key
    if not api_key:
        return {
            "success": False,
            "error": "No API key provided. Enable 'Demo mode' in sidebar to explore without API calls."
        }
    
    # Try API call with retry/backoff
    try:
        from openai import OpenAI
    except ImportError:
        return {
            "success": False,
            "error": "OpenAI package not installed. Enable 'Demo mode' to continue."
        }
    
    client = OpenAI(api_key=api_key)
    
    for attempt in range(max_retries + 1):
        try:
            if response_format:
                # Structured output
                completion = client.beta.chat.completions.parse(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    response_format=response_format,
                )
                return {
                    "success": True,
                    "data": completion.choices[0].message.parsed,
                    "model": model,
                    "temperature": temperature,
                }
            else:
                # Standard completion
                completion = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                )
                return {
                    "success": True,
                    "data": completion.choices[0].message.content,
                    "model": model,
                    "temperature": temperature,
                }
        
        except Exception as e:
            error_msg = str(e)
            
            # Retry on rate limit or server errors
            if attempt < max_retries and ("429" in error_msg or "5" in error_msg[:3]):
                sleep_time = 1 * (2 ** attempt)  # 1s, then 2s
                time.sleep(sleep_time)
                continue
            
            # Final error
            return {
                "success": False,
                "error": f"OpenAI API error: {error_msg}. Enable 'Demo mode' to continue."
            }
    
    return {
        "success": False,
        "error": "Max retries exceeded. Enable 'Demo mode' to continue."
    }


def _get_demo_response(response_format: type[BaseModel] | None) -> Dict[str, Any]:
    """
    Generate canned demo response based on expected format.
    """
    # For ScenarioAnalysis (from ai_parser.py)
    if response_format and "ScenarioAnalysis" in str(response_format):
        from .ai_parser import ScenarioAnalysis
        
        demo_analysis = ScenarioAnalysis(
            contains_pii=True,
            customer_facing=True,
            high_stakes=True,
            autonomy_level=2,
            sector="Healthcare",
            modifiers=["Cyber"],
            model_type="Traditional ML",
            data_source="Proprietary/Internal",
            learns_in_production=False,
            international_data=False,
            explainability_level="Post-hoc Explainable",
            uses_foundation_model="No Third-Party",
            generates_synthetic_content=False,
            dual_use_risk="None / Low",
            decision_reversible="Partially Reversible",
            protected_populations=["Elderly"],
            reasoning="Demo mode: This is a canned analysis for demonstration purposes. The system appears to be a healthcare application processing sensitive data with moderate automation.",
            estimated_risk_tier="High",
            key_risk_factors=[
                "Processes PII/PHI in healthcare context",
                "Customer-facing with moderate autonomy",
                "Elderly users may be vulnerable population"
            ],
            recommended_safeguards=[
                "HIPAA compliance review required",
                "Accessibility audit for elderly users",
                "Data encryption at rest and in transit",
                "Audit logging for all data access",
                "Regular bias testing"
            ],
            framework_alignment="NIST AI RMF (GOVERN/MAP), EU AI Act (potential high-risk), HIPAA",
            gaps_and_limitations=[
                "Data storage location unknown - can't assess GDPR cross-border requirements",
                "Vendor/DPA terms unknown - supply chain risk unclear"
            ]
        )
        
        return {
            "success": True,
            "data": demo_analysis,
            "model": "demo-mode",
            "temperature": 0.0,
        }
    
    # For InterviewResponse (from ai_interviewer.py)
    if response_format and "InterviewResponse" in str(response_format):
        from .ai_interviewer import InterviewResponse, InterviewQuestion
        
        demo_response = InterviewResponse(
            needs_clarification=True,
            questions=[
                InterviewQuestion(
                    question="Where is the data stored (US, EU, or other regions)?",
                    rationale="Data location affects GDPR, Schrems II, and data sovereignty compliance",
                    framework_reference="GDPR Art. 44-50, EU AI Act Art. 10"
                ),
                InterviewQuestion(
                    question="Is there a Business Associate Agreement (BAA) in place with data processors?",
                    rationale="Required for HIPAA compliance when PHI is involved",
                    framework_reference="HIPAA 45 CFR § 164.502(e)"
                )
            ],
            reasoning="Demo mode: Need to clarify data location and contractual safeguards for comprehensive assessment",
            ready_for_analysis=False
        )
        
        return {
            "success": True,
            "data": demo_response,
            "model": "demo-mode",
            "temperature": 0.0,
        }
    
    # Generic text response
    return {
        "success": True,
        "data": "Demo mode: This is a placeholder response for demonstration purposes.",
        "model": "demo-mode",
        "temperature": 0.0,
    }

