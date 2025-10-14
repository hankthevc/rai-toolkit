# RAI Toolkit Stress Testing Guide

## Overview

This comprehensive stress testing suite evaluates the RAI Toolkit from the perspective of a senior responsible AI governance professional. It tests functional correctness, UX quality, performance, governance rigor, and professional polish.

## What Gets Tested

### 1. Functional Correctness
- **Happy path workflows**: Complete end-to-end scenarios (describe → interview → analysis → export)
- **Edge cases**: Empty input, very long text (10,000+ chars), single-character input
- **Special characters**: Unicode, emoji, HTML/script injection attempts, SQL injection strings
- **API failures**: Missing keys, timeouts, malformed responses
- **State management**: Rapid button clicking, browser back/forward, concurrent sessions

### 2. UX & Usability
- **Navigation clarity**: Is the workflow intuitive? Are instructions clear?
- **Error messaging**: Are errors specific and actionable, or vague?
- **Disclaimer visibility**: Is the demo/prototype nature prominently disclosed?
- **Accessibility**: Basic keyboard navigation and screen reader compatibility
- **Responsive design**: Mobile and tablet viewport handling

### 3. Performance & Reliability
- **Page load times**: Initial app load should be <5s
- **Input responsiveness**: Large text handling should be smooth
- **API latency**: Reasonable timeouts and feedback during processing
- **Memory usage**: No leaks during extended use

### 4. Governance-Specific
- **Framework citations**: Are NIST AI RMF, EU AI Act, ISO 42001, OWASP, etc. properly referenced?
- **Risk calculation accuracy**: Does the scoring logic match documented methodology?
- **Transparency**: Is risk tier reasoning clear and explainable?
- **Policy pack matching**: Do controls trigger correctly for scenarios?
- **Export quality**: Do decision records contain all required sections?

### 5. Professional Polish
- **Typos and grammar**: Text should be professional and error-free
- **UI consistency**: Buttons, colors, spacing should be uniform
- **Code quality**: No exposed stack traces or debug output
- **Visual design**: Clean, modern, trustworthy appearance

## Running the Tests

### Prerequisites

```bash
# Python 3.11+
python3 --version

# Install stress test dependencies
pip install -r requirements-stress.txt

# Install Playwright browsers
python3 -m playwright install chromium
```

### Quick Start

```bash
# Run complete stress test suite
./scripts/run_stress_test.sh
```

This script will:
1. Start Streamlit app on available port
2. Wait for app to be ready
3. Execute comprehensive Playwright tests
4. Generate HTML report with screenshots
5. Open report in browser
6. Clean up Streamlit process

### Manual Execution

```bash
# Start Streamlit manually
streamlit run project1_risk_framework/app.py --server.port=8501

# In another terminal, run tests
pytest tests/stress_agent.py \
    --base-url="http://localhost:8501" \
    --browser=chromium \
    --headed \
    -v
```

Use `--headed` to watch tests run in browser (helpful for debugging).

## Interpreting the Report

### Health Score (0-100)

- **90-100 (Excellent)**: Production-ready quality, minimal issues
- **70-89 (Good)**: Demo-quality with some polish needed
- **50-69 (Fair)**: Functional but needs significant improvements
- **<50 (Poor)**: Major issues impacting usability or credibility

**Scoring deductions:**
- Critical issue: -25 points
- High issue: -10 points
- Medium issue: -3 points
- Low issue: -1 point

### Issue Severity Levels

**Critical** (Must Fix Before Sharing)
- Breaks core functionality (can't perform risk assessment)
- Exposes sensitive data or security vulnerabilities
- Incorrect risk calculations or framework misattributions
- Unhandled errors causing blank screens

**High** (Fix Before Hiring Manager Review)
- Significantly degrades UX (confusing errors, unclear workflow)
- Missing governance rigor (no framework citations, opaque reasoning)
- Slow performance (>5s load, unresponsive UI)
- Missing disclaimers about demo nature

**Medium** (Polish Issues)
- Validation gaps (empty input allowed)
- Inconsistent UI styling
- Minor performance issues
- Missing tooltips or help text

**Low** (Nice-to-Haves)
- Typos or grammar improvements
- Additional accessibility features
- Verbose text that could be condensed
- Extra formatting polish

## What Senior Governance Professionals Care About

When reviewing this tool, experienced AI governance leaders will evaluate:

### 1. **Governance Rigor**
- Are framework citations accurate and up-to-date?
- Is the risk scoring methodology sound and transparent?
- Do policy controls map correctly to scenarios?
- Are there gaps in coverage (e.g., missing OWASP LLM Top 10)?

**Why it matters**: Credibility. If citations are wrong or reasoning is opaque, the tool loses trust.

### 2. **Transparency & Explainability**
- Can users understand WHY a risk tier was assigned?
- Are AI-generated recommendations clearly labeled as AI output?
- Are assumptions and limitations disclosed?

**Why it matters**: Governance is about informed decision-making. Black-box assessments are not useful.

### 3. **Professional Polish**
- Are there typos, broken features, or sloppy UI?
- Does the tool look like a serious prototype or a hackathon demo?
- Is error handling graceful, or do stack traces appear?

**Why it matters**: First impressions. Sloppy execution suggests lack of attention to detail.

### 4. **Technical Depth**
- Does the code show good judgment (error handling, state management)?
- Are edge cases handled thoughtfully?
- Is the architecture clean and maintainable?

**Why it matters**: This is a portfolio/hiring evaluation. Code quality reflects problem-solving skills.

### 5. **Humility & Framing**
- Does the tool appropriately frame itself as a demo, not production?
- Are limitations (simplified scoring, sample data) disclosed?
- Is there overconfidence in recommendations?

**Why it matters**: Governance professionals are wary of tools that overclaim. Humble, honest framing is more credible.

## Common Issues and Fixes

### Issue: "No textarea found for scenario input"
**Cause**: Streamlit not fully loaded, or app initialization failed  
**Fix**: Increase wait time in `wait_for_streamlit_ready()`, check app logs

### Issue: "No analysis output after clicking Analyze"
**Cause**: Missing OpenAI API key or API errors  
**Fix**: Set `OPENAI_API_KEY` environment variable or Streamlit secrets, enable demo mode

### Issue: "Rapid button clicks cause errors"
**Cause**: No debouncing or loading state  
**Fix**: Disable button while processing, add `st.spinner()` context

### Issue: "Framework citations missing or incorrect"
**Cause**: AI prompt not emphasizing frameworks, or policy packs incomplete  
**Fix**: Update AI system prompt, expand YAML policy pack citations

### Issue: "Export not found"
**Cause**: Download button not rendering after analysis  
**Fix**: Check conditional logic for showing download buttons

## Extending the Tests

To add new tests, edit `tests/stress_agent.py`:

```python
@pytest.mark.asyncio
async def test_my_new_scenario(page: Page):
    """Test description."""
    try:
        await wait_for_streamlit_ready(page)
        
        # Your test logic here
        
        # If issue found:
        screenshot = await take_screenshot(page, "issue_name")
        REPORT.add_issue(Issue(
            severity="High",  # Critical, High, Medium, Low
            category="Functional",  # Functional, UX, Performance, Governance, Polish
            title="Brief issue title",
            description="Detailed explanation of what's wrong",
            screenshot_path=screenshot,
            reproduction_steps=["Step 1", "Step 2", "Step 3"],
            recommendation="How to fix this",
            governance_impact="Why this matters for governance professionals"
        ))
        
    except Exception as e:
        print(f"Test error: {e}")
```

## CI Integration (Optional)

To run stress tests in GitHub Actions:

```yaml
# .github/workflows/stress-test.yml
name: Stress Test

on:
  workflow_dispatch:  # Manual trigger only
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  stress-test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-stress.txt
          python -m playwright install --with-deps chromium
      
      - name: Run stress tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: ./scripts/run_stress_test.sh
      
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: stress-test-report
          path: stress_test_reports/
```

## Known Limitations

This stress test suite is designed for local testing and demo evaluation. It does NOT:

- Test against production Streamlit Cloud (bot protection may block Playwright)
- Perform security penetration testing (use dedicated tools for that)
- Test at scale (concurrent users, load testing - use Locust/k6 for that)
- Validate against actual NIST/EU AI Act legal text (manual review required)

## Questions or Issues?

If tests fail unexpectedly:
1. Check `streamlit.log` for app errors
2. Run with `--headed` to watch browser interaction
3. Review screenshots in `stress_test_reports/screenshots/`
4. Check that all dependencies are installed correctly

---

**Remember**: This is a portfolio demonstration tool. The stress tests evaluate it as such - looking for polish, thoughtfulness, and governance judgment, not production-grade completeness.

