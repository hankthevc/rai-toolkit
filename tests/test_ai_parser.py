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
    )

    assert analysis.contains_pii is True
    assert analysis.customer_facing is True
    assert analysis.high_stakes is True
    assert analysis.autonomy_level == 2
    assert analysis.sector == "Healthcare"
    assert "Bio" in analysis.modifiers
    assert "Cyber" in analysis.modifiers
    assert len(analysis.reasoning) > 0


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
    )

    summary = format_analysis_summary(analysis)

    # Check that summary includes key information
    assert "AI Analysis Summary" in summary
    assert "Financial system" in summary
    assert "Yes" in summary  # For PII
    assert "No" in summary   # For customer_facing
    assert "Human-in-the-loop" in summary
    assert "Finance" in summary
    assert "Cyber" in summary


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
    )

    summary = format_analysis_summary(analysis)

    assert "None" in summary  # Should indicate no modifiers
    assert "Suggestion only" in summary


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
    import sys
    from common.utils import ai_parser
    
    # Temporarily remove openai from imports
    monkeypatch.setattr(ai_parser, "OpenAI", None)
    
    from common.utils.ai_parser import parse_scenario_with_ai
    
    with pytest.raises(ImportError, match="openai package not installed"):
        parse_scenario_with_ai("Test scenario")


def test_parse_scenario_empty_description():
    """Test that empty descriptions return None."""
    from common.utils.ai_parser import parse_scenario_with_ai
    
    assert parse_scenario_with_ai("") is None
    assert parse_scenario_with_ai("   ") is None


def test_parse_scenario_missing_api_key(monkeypatch):
    """Test that missing API key raises helpful error."""
    import os
    from common.utils.ai_parser import parse_scenario_with_ai
    
    # Clear environment variable
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    
    with pytest.raises(ValueError, match="OpenAI API key required"):
        parse_scenario_with_ai("Test scenario", api_key=None)

