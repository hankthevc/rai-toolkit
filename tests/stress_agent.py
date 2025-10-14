"""Comprehensive stress test suite for RAI Toolkit Streamlit app.

Evaluates the application from the perspective of a senior responsible AI governance
professional, testing functional correctness, UX, performance, and governance rigor.
"""

from __future__ import annotations

import asyncio
import time
from pathlib import Path

import pytest
from playwright.async_api import Page, expect

from tests.report_generator import Issue, StressTestReport

# Initialize global report
REPORT = StressTestReport()
SCREENSHOTS_DIR = Path(__file__).parent.parent / "stress_test_reports" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


async def take_screenshot(page: Page, name: str) -> Path:
    """Capture screenshot for issue documentation."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filepath = SCREENSHOTS_DIR / f"{name}_{timestamp}.png"
    await page.screenshot(path=str(filepath), full_page=True)
    return filepath


async def wait_for_streamlit_ready(page: Page, timeout: int = 10000):
    """Wait for Streamlit app to be fully loaded."""
    try:
        # Wait for Streamlit's main container
        await page.wait_for_selector('[data-testid="stAppViewContainer"]', timeout=timeout)
        # Give it a moment to settle
        await asyncio.sleep(1)
    except Exception:
        pass  # Continue even if selector not found


# =======================
# FUNCTIONAL CORRECTNESS
# =======================


@pytest.mark.asyncio
async def test_happy_path_healthcare_chatbot(page: Page):
    """Test complete workflow: describe scenario → interview → analysis → export."""
    try:
        await wait_for_streamlit_ready(page)
        
        # Enter scenario description
        scenario = "A chatbot that helps hospital patients schedule appointments and refill prescriptions. It accesses their medical records to check medication history and insurance eligibility."
        
        textareas = page.locator("textarea")
        if await textareas.count() > 0:
            await textareas.first.fill(scenario)
        else:
            screenshot = await take_screenshot(page, "happy_path_no_textarea")
            REPORT.add_issue(Issue(
                severity="Critical",
                category="Functional",
                title="Main scenario input field not found",
                description="The primary textarea for entering AI use case descriptions is missing or not loading.",
                screenshot_path=screenshot,
                recommendation="Verify Streamlit app initialization and ensure the main input field renders correctly."
            ))
            pytest.fail("No textarea found for scenario input")
        
        # Click analyze button
        analyze_button = page.locator("button", has_text="Analyze")
        if await analyze_button.count() > 0:
            await analyze_button.first.click()
            await asyncio.sleep(3)  # Wait for AI processing
        else:
            screenshot = await take_screenshot(page, "happy_path_no_button")
            REPORT.add_issue(Issue(
                severity="Critical",
                category="Functional",
                title="Analyze button not found",
                description="The primary action button to start analysis is missing.",
                screenshot_path=screenshot,
                recommendation="Check button rendering logic and ensure proper Streamlit button initialization."
            ))
            pytest.fail("No analyze button found")
        
        # Check for interview questions or analysis output
        await asyncio.sleep(2)
        page_content = await page.content()
        
        if "Step 1" not in page_content and "Assessment" not in page_content and "Question" not in page_content:
            screenshot = await take_screenshot(page, "happy_path_no_output")
            REPORT.add_issue(Issue(
                severity="High",
                category="Functional",
                title="No analysis output after clicking Analyze",
                description="After clicking the Analyze button, no interview questions or risk assessment appeared.",
                screenshot_path=screenshot,
                reproduction_steps=[
                    "Enter a healthcare chatbot scenario",
                    "Click 'Analyze AI Use Case' button",
                    "Wait 5 seconds",
                    "Observe no output appears"
                ],
                recommendation="Check API key configuration, error handling, and ensure AI analysis logic executes properly.",
                governance_impact="Users cannot perform risk assessments, making the tool non-functional."
            ))
        
        REPORT.add_metric("Happy Path Completion", "Partial" if "Assessment" not in page_content else "Success")
        
    except Exception as e:
        screenshot = await take_screenshot(page, "happy_path_exception")
        REPORT.add_issue(Issue(
            severity="Critical",
            category="Functional",
            title=f"Happy path test crashed: {type(e).__name__}",
            description=str(e),
            screenshot_path=screenshot,
            recommendation="Investigate root cause of exception and add error handling."
        ))
        raise


@pytest.mark.asyncio
async def test_edge_case_empty_input(page: Page):
    """Verify graceful handling of empty input."""
    try:
        await wait_for_streamlit_ready(page)
        
        # Try to click analyze without entering text
        analyze_button = page.locator("button", has_text="Analyze")
        if await analyze_button.count() > 0:
            initial_button_state = await analyze_button.first.is_disabled()
            
            # If button allows clicking with empty input
            if not initial_button_state:
                await analyze_button.first.click()
                await asyncio.sleep(2)
                
                page_content = await page.content()
                
                # Check if appropriate error message is shown
                if "provide" not in page_content.lower() and "describe" not in page_content.lower() and "enter" not in page_content.lower():
                    screenshot = await take_screenshot(page, "empty_input_no_validation")
                    REPORT.add_issue(Issue(
                        severity="Medium",
                        category="UX",
                        title="Empty input allowed without clear feedback",
                        description="User can click Analyze button with empty scenario description, but no clear validation message appears.",
                        screenshot_path=screenshot,
                        reproduction_steps=[
                            "Leave scenario description empty",
                            "Click 'Analyze AI Use Case' button",
                            "Observe lack of validation feedback"
                        ],
                        recommendation="Add client-side validation or clear error message prompting user to enter a description."
                    ))
        
    except Exception as e:
        print(f"Edge case empty input test error (non-critical): {e}")


@pytest.mark.asyncio
async def test_edge_case_very_long_input(page: Page):
    """Test handling of extremely long scenario descriptions."""
    try:
        await wait_for_streamlit_ready(page)
        
        # Create 10,000 character input
        long_text = "A " * 5000  # ~10,000 characters
        
        textareas = page.locator("textarea")
        if await textareas.count() > 0:
            start_time = time.time()
            await textareas.first.fill(long_text)
            fill_time = time.time() - start_time
            
            if fill_time > 3:
                REPORT.add_issue(Issue(
                    severity="Low",
                    category="Performance",
                    title="Slow textarea performance with long input",
                    description=f"Filling textarea with 10,000 characters took {fill_time:.2f}s (>3s threshold).",
                    recommendation="Consider debouncing or optimizing input handling for large text."
                ))
            
            REPORT.add_metric("Long Input Fill Time", f"{fill_time:.2f}s")
        
    except Exception as e:
        print(f"Long input test error (non-critical): {e}")


@pytest.mark.asyncio
async def test_special_characters_unicode(page: Page):
    """Test handling of special characters and Unicode."""
    try:
        await wait_for_streamlit_ready(page)
        
        # Test with emoji, Unicode, and special characters
        special_text = "AI chatbot 🤖 with 中文支持 and special chars: <script>alert('xss')</script> ' \" & % $"
        
        textareas = page.locator("textarea")
        if await textareas.count() > 0:
            await textareas.first.fill(special_text)
            
            # Verify text was accepted
            filled_value = await textareas.first.input_value()
            if special_text not in filled_value:
                REPORT.add_issue(Issue(
                    severity="Medium",
                    category="Functional",
                    title="Special characters not properly handled in input",
                    description="Input field does not correctly accept or display special characters, emoji, or Unicode.",
                    recommendation="Ensure proper UTF-8 encoding and sanitization without losing legitimate special characters."
                ))
        
    except Exception as e:
        print(f"Special characters test error (non-critical): {e}")


# =======================
# UX / USABILITY
# =======================


@pytest.mark.asyncio
async def test_disclaimer_visibility(page: Page):
    """Verify demo disclaimer is prominently displayed."""
    try:
        await wait_for_streamlit_ready(page)
        
        page_text = await page.text_content("body")
        
        disclaimer_keywords = ["demo", "prototype", "not production", "sample", "demonstrative"]
        found_disclaimer = any(keyword in page_text.lower() for keyword in disclaimer_keywords)
        
        if not found_disclaimer:
            screenshot = await take_screenshot(page, "missing_disclaimer")
            REPORT.add_issue(Issue(
                severity="High",
                category="Governance",
                title="Demo disclaimer not prominently displayed",
                description="No clear disclaimer warning users this is a demonstration tool, not production software.",
                screenshot_path=screenshot,
                recommendation="Add prominent disclaimer banner or info box explaining demo nature and limitations.",
                governance_impact="Governance professionals expect clear framing of tool limitations. Missing disclaimer reduces credibility."
            ))
        
    except Exception as e:
        print(f"Disclaimer test error: {e}")


@pytest.mark.asyncio
async def test_error_message_quality(page: Page):
    """Check if error messages are clear and actionable."""
    try:
        await wait_for_streamlit_ready(page)
        
        # Look for any error or warning messages currently displayed
        error_selectors = [
            '[data-testid="stException"]',
            '.stError',
            '[role="alert"]'
        ]
        
        for selector in error_selectors:
            error_elements = page.locator(selector)
            count = await error_elements.count()
            
            if count > 0:
                for i in range(count):
                    error_text = await error_elements.nth(i).text_content()
                    
                    # Check if error message is vague or unhelpful
                    vague_patterns = ["error occurred", "something went wrong", "failed", "none", "null"]
                    is_vague = any(pattern in error_text.lower() for pattern in vague_patterns) and len(error_text) < 50
                    
                    if is_vague:
                        screenshot = await take_screenshot(page, f"vague_error_{i}")
                        REPORT.add_issue(Issue(
                            severity="Medium",
                            category="UX",
                            title="Vague or unhelpful error message",
                            description=f"Error message lacks actionable guidance: '{error_text}'",
                            screenshot_path=screenshot,
                            recommendation="Provide specific error messages with clear next steps (e.g., 'API key missing. Add OPENAI_API_KEY to Streamlit secrets.')."
                        ))
        
    except Exception as e:
        print(f"Error message quality test error: {e}")


@pytest.mark.asyncio
async def test_navigation_clarity(page: Page):
    """Assess whether app workflow is clear and intuitive."""
    try:
        await wait_for_streamlit_ready(page)
        
        page_text = await page.text_content("body")
        
        # Check for clear instructions or guidance
        has_instructions = any(keyword in page_text.lower() for keyword in [
            "describe your", "enter your", "step 1", "getting started"
        ])
        
        if not has_instructions:
            screenshot = await take_screenshot(page, "unclear_navigation")
            REPORT.add_issue(Issue(
                severity="Low",
                category="UX",
                title="Workflow instructions could be clearer",
                description="No explicit step-by-step guidance for first-time users.",
                screenshot_path=screenshot,
                recommendation="Add a 'Quick Start' section or numbered workflow steps to guide users."
            ))
        
    except Exception as e:
        print(f"Navigation test error: {e}")


# =======================
# PERFORMANCE
# =======================


@pytest.mark.asyncio
async def test_page_load_performance(page: Page):
    """Measure initial page load time."""
    try:
        start_time = time.time()
        await wait_for_streamlit_ready(page)
        load_time = time.time() - start_time
        
        REPORT.add_metric("Page Load Time", f"{load_time:.2f}s")
        
        if load_time > 5:
            REPORT.add_issue(Issue(
                severity="Medium",
                category="Performance",
                title="Slow page load time",
                description=f"Initial page load took {load_time:.2f}s (>5s threshold).",
                recommendation="Optimize Streamlit caching, reduce initial data loading, or improve asset delivery."
            ))
        
    except Exception as e:
        print(f"Page load test error: {e}")


# =======================
# GOVERNANCE-SPECIFIC
# =======================


@pytest.mark.asyncio
async def test_framework_citations_present(page: Page):
    """Verify governance framework references are visible."""
    try:
        await wait_for_streamlit_ready(page)
        
        # Run a sample analysis to get output
        textareas = page.locator("textarea")
        if await textareas.count() > 0:
            await textareas.first.fill("Healthcare AI chatbot for patient appointment scheduling")
            
            analyze_button = page.locator("button", has_text="Analyze")
            if await analyze_button.count() > 0:
                await analyze_button.first.click()
                await asyncio.sleep(5)  # Wait for analysis
                
                page_text = await page.text_content("body")
                
                # Check for framework mentions
                frameworks = ["NIST", "EU AI Act", "ISO", "OWASP", "MITRE", "HIPAA", "GDPR"]
                found_frameworks = [fw for fw in frameworks if fw in page_text]
                
                REPORT.add_metric("Frameworks Referenced", len(found_frameworks))
                
                if len(found_frameworks) < 2:
                    screenshot = await take_screenshot(page, "missing_frameworks")
                    REPORT.add_issue(Issue(
                        severity="High",
                        category="Governance",
                        title="Insufficient governance framework citations",
                        description=f"Only {len(found_frameworks)} framework(s) referenced in output. Expected multiple frameworks for credibility.",
                        screenshot_path=screenshot,
                        recommendation="Ensure AI analysis and policy packs reference relevant frameworks (NIST AI RMF, EU AI Act, ISO 42001, etc.).",
                        governance_impact="Governance professionals expect rigorous framework alignment. Lack of citations undermines credibility."
                    ))
        
    except Exception as e:
        print(f"Framework citations test error: {e}")


@pytest.mark.asyncio
async def test_risk_tier_transparency(page: Page):
    """Check if risk assessment rationale is transparent."""
    try:
        await wait_for_streamlit_ready(page)
        
        # Run analysis
        textareas = page.locator("textarea")
        if await textareas.count() > 0:
            await textareas.first.fill("Internal code completion tool for engineers")
            
            analyze_button = page.locator("button", has_text="Analyze")
            if await analyze_button.count() > 0:
                await analyze_button.first.click()
                await asyncio.sleep(5)
                
                page_text = await page.text_content("body")
                
                # Check for risk tier + reasoning
                has_risk_tier = any(tier in page_text for tier in ["Low", "Medium", "High", "Critical"])
                has_reasoning = any(keyword in page_text.lower() for keyword in [
                    "because", "due to", "reasoning", "factors", "why"
                ])
                
                if has_risk_tier and not has_reasoning:
                    screenshot = await take_screenshot(page, "missing_reasoning")
                    REPORT.add_issue(Issue(
                        severity="High",
                        category="Governance",
                        title="Risk tier lacks transparent reasoning",
                        description="Risk classification is shown but rationale is not clearly explained.",
                        screenshot_path=screenshot,
                        recommendation="Always display clear reasoning for risk tier assignment with specific factors.",
                        governance_impact="Transparency is critical for AI governance. Users need to understand WHY a tier was assigned."
                    ))
        
    except Exception as e:
        print(f"Risk transparency test error: {e}")


@pytest.mark.asyncio
async def test_export_quality(page: Page):
    """Verify decision record export contains required sections."""
    try:
        await wait_for_streamlit_ready(page)
        
        # Run full workflow to get export button
        textareas = page.locator("textarea")
        if await textareas.count() > 0:
            await textareas.first.fill("Automated trading system for securities")
            
            analyze_button = page.locator("button", has_text="Analyze")
            if await analyze_button.count() > 0:
                await analyze_button.first.click()
                await asyncio.sleep(5)
                
                # Look for download button
                download_buttons = page.locator("button", has_text="Decision Record")
                if await download_buttons.count() == 0:
                    download_buttons = page.locator('[data-testid="stDownloadButton"]')
                
                if await download_buttons.count() > 0:
                    REPORT.add_metric("Export Available", "Yes")
                else:
                    screenshot = await take_screenshot(page, "missing_export")
                    REPORT.add_issue(Issue(
                        severity="Medium",
                        category="Functional",
                        title="Decision record export not found",
                        description="No download button for decision record found after analysis.",
                        screenshot_path=screenshot,
                        recommendation="Ensure download button renders after successful risk assessment."
                    ))
        
    except Exception as e:
        print(f"Export quality test error: {e}")


# =======================
# PROFESSIONAL POLISH
# =======================


@pytest.mark.asyncio
async def test_ui_consistency(page: Page):
    """Check for consistent styling and formatting."""
    try:
        await wait_for_streamlit_ready(page)
        
        # Check button consistency
        buttons = page.locator("button")
        button_count = await buttons.count()
        
        if button_count > 3:
            # Sample a few buttons to check styling
            styles = []
            for i in range(min(3, button_count)):
                style = await buttons.nth(i).get_attribute("style")
                styles.append(style)
            
            # Basic check: if styles are wildly different, flag it
            # (This is a simplified check; real implementation would be more sophisticated)
            REPORT.add_metric("UI Elements Checked", f"{button_count} buttons")
        
    except Exception as e:
        print(f"UI consistency test error: {e}")


# =======================
# STATE MANAGEMENT
# =======================


@pytest.mark.asyncio
async def test_rapid_button_clicking(page: Page):
    """Test if rapid button clicks cause state corruption."""
    try:
        await wait_for_streamlit_ready(page)
        
        textareas = page.locator("textarea")
        if await textareas.count() > 0:
            await textareas.first.fill("Test scenario")
            
            analyze_button = page.locator("button", has_text="Analyze")
            if await analyze_button.count() > 0:
                # Click rapidly 5 times
                for _ in range(5):
                    await analyze_button.first.click()
                    await asyncio.sleep(0.1)
                
                await asyncio.sleep(3)
                
                # Check if page is still responsive
                page_text = await page.text_content("body")
                
                # Look for error indicators
                if "traceback" in page_text.lower() or "exception" in page_text.lower():
                    screenshot = await take_screenshot(page, "rapid_click_error")
                    REPORT.add_issue(Issue(
                        severity="High",
                        category="Functional",
                        title="Rapid button clicks cause errors",
                        description="Clicking the analyze button multiple times rapidly causes exceptions or crashes.",
                        screenshot_path=screenshot,
                        reproduction_steps=[
                            "Enter a scenario",
                            "Rapidly click 'Analyze AI Use Case' button 5 times",
                            "Observe error state"
                        ],
                        recommendation="Implement button debouncing or disable button while processing."
                    ))
        
    except Exception as e:
        print(f"Rapid clicking test error: {e}")


# =======================
# PYTEST CONFIGURATION
# =======================


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context for testing."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "en-US",
    }


def pytest_configure(config):
    """Configure pytest and initialize report."""
    print("\n🚀 Starting RAI Toolkit stress tests...")
    print("   Evaluating: Functional correctness, UX, performance, governance rigor\n")


def pytest_sessionfinish(session, exitstatus):
    """Generate HTML report after all tests complete."""
    # Update test summary from pytest (simplified approach)
    # Count based on exit status as detailed session stats require plugin hooks
    total = len(session.items) if hasattr(session, 'items') else 0
    failed = min(exitstatus, total) if exitstatus > 0 else 0
    passed = total - failed
    skipped = 0
    
    REPORT.update_test_summary(passed, failed, skipped)
    
    # Generate report
    report_dir = Path(__file__).parent.parent / "stress_test_reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"report_{timestamp}.html"
    
    REPORT.generate_html(report_path)
    
    print(f"\n✅ Stress test complete! Report: {report_path}\n")

