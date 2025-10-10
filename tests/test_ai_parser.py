"""Tests for AI-powered scenario parsing functionality."""

from __future__ import annotations

import pytest

from common.utils.ai_parser import (
    ScenarioAnalysis,
    format_analysis_summary,
)


def test_scenario_analysis_model():
    """Test ScenarioAnalysis Pydantic model validation."""
    analysis = ScenarioAnalysis(
        contains_pii=True,
        customer_facing=True,
        high_stakes=True,
        autonomy_level=2,
        sector="Healthcare",
        modifiers=["Bio", "Cyber"],
        reasoning="Test scenario involves patient data and automated decisions.",
        estimated_risk_tier="Critical",
        key_risk_factors=["Patient data exposure", "Automated medical decisions"],
        recommended_safeguards=["HIPAA compliance", "Human oversight"],
        framework_alignment="EU AI Act High-Risk, NIST AI RMF GOVERN"
    )

    assert analysis.contains_pii is True
    assert analysis.customer_facing is True
    assert analysis.high_stakes is True
    assert analysis.autonomy_level == 2
    assert analysis.sector == "Healthcare"
    assert "Bio" in analysis.modifiers
    assert "Cyber" in analysis.modifiers
    assert len(analysis.reasoning) > 0
    assert analysis.estimated_risk_tier == "Critical"
    assert len(analysis.key_risk_factors) > 0
    assert len(analysis.recommended_safeguards) > 0
    assert len(analysis.framework_alignment) > 0


def test_scenario_analysis_autonomy_validation():
    """Test that autonomy_level is constrained to 0-3."""
    # Valid values
    for level in [0, 1, 2, 3]:
        analysis = ScenarioAnalysis(
            contains_pii=False,
            customer_facing=False,
            high_stakes=False,
            autonomy_level=level,
            sector="General",
            modifiers=[],
            reasoning="Test",
            estimated_risk_tier="Low",
            key_risk_factors=["Test factor"],
            recommended_safeguards=["Test safeguard"],
            framework_alignment="Test framework"
        )
        assert analysis.autonomy_level == level

    # Invalid value should raise validation error
    with pytest.raises(Exception):  # Pydantic ValidationError
        ScenarioAnalysis(
            contains_pii=False,
            customer_facing=False,
            high_stakes=False,
            autonomy_level=5,  # Invalid: out of range
            sector="General",
            modifiers=[],
            reasoning="Test",
            estimated_risk_tier="Low",
            key_risk_factors=["Test"],
            recommended_safeguards=["Test"],
            framework_alignment="Test"
        )


def test_format_analysis_summary():
    """Test that analysis summary is formatted correctly."""
    analysis = ScenarioAnalysis(
        contains_pii=True,
        customer_facing=False,
        high_stakes=True,
        autonomy_level=1,
        sector="Finance",
        modifiers=["Cyber"],
        reasoning="Financial system with human oversight and cyber threat exposure.",
        estimated_risk_tier="High",
        key_risk_factors=["Financial data exposure", "Cyber threats"],
        recommended_safeguards=["Access controls", "Audit logging"],
        framework_alignment="NIST AI RMF, ISO 42001"
    )

    summary = format_analysis_summary(analysis)

    # Check that summary includes key information
    assert "AI Governance Analysis" in summary
    assert "Financial system" in summary
    assert "Yes" in summary  # For PII
    assert "No" in summary   # For customer_facing
    assert "Human-in-the-loop" in summary
    assert "Finance" in summary
    assert "Cyber" in summary
    assert "High Risk" in summary
    assert "Financial data exposure" in summary
    assert "NIST AI RMF" in summary


def test_format_analysis_summary_no_modifiers():
    """Test summary formatting when no modifiers are present."""
    analysis = ScenarioAnalysis(
        contains_pii=False,
        customer_facing=False,
        high_stakes=False,
        autonomy_level=0,
        sector="General",
        modifiers=[],
        reasoning="Low-risk internal tool.",
        estimated_risk_tier="Low",
        key_risk_factors=["Minimal risk"],
        recommended_safeguards=["Basic documentation"],
        framework_alignment="General best practices"
    )

    summary = format_analysis_summary(analysis)

    assert "None" in summary  # Should indicate no modifiers
    assert "Suggestion only" in summary
    assert "Low Risk" in summary


# Integration test (requires API key, marked as skip by default)
@pytest.mark.skip(reason="Requires OpenAI API key; run manually with pytest -m integration")
def test_parse_scenario_with_ai_integration():
    """Integration test for OpenAI API parsing (requires OPENAI_API_KEY)."""
    from common.utils.ai_parser import parse_scenario_with_ai

    description = (
        "A chatbot that helps hospital patients schedule appointments "
        "and refill prescriptions by accessing their medical records."
    )

    analysis = parse_scenario_with_ai(description)

    assert analysis is not None
    assert analysis.contains_pii is True  # Should detect PHI
    assert analysis.sector == "Healthcare"
    assert len(analysis.reasoning) > 0


def test_parse_scenario_missing_openai_package(monkeypatch):
    """Test graceful handling when openai package is not installed."""
    from common.utils.ai_parser import parse_scenario_with_ai
    
    # With no API key and demo_mode=False, should return None (graceful failure)
    result = parse_scenario_with_ai("Test scenario", api_key=None, demo_mode=False)
    
    # Function now returns None instead of raising
    assert result is None


def test_parse_scenario_empty_description():
    """Test that empty descriptions return None."""
    from common.utils.ai_parser import parse_scenario_with_ai
    
    assert parse_scenario_with_ai("") is None
    assert parse_scenario_with_ai("   ") is None


def test_parse_scenario_missing_api_key(monkeypatch):
    """Test that missing API key returns None gracefully."""
    import os
    from common.utils.ai_parser import parse_scenario_with_ai
    
    # Clear environment variable
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    
    # Now returns None instead of raising
    result = parse_scenario_with_ai("Test scenario", api_key=None, demo_mode=False)
    assert result is None

