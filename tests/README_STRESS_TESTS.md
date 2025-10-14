# Stress Test Suite

Comprehensive Playwright-based UI/UX testing for RAI Toolkit, designed to evaluate the application from a senior governance professional's perspective.

## Quick Start

```bash
# Install dependencies
pip install -r requirements-stress.txt
python -m playwright install chromium

# Run stress tests
./scripts/run_stress_test.sh
```

The script will:
1. Start Streamlit app locally
2. Run comprehensive Playwright tests
3. Generate HTML report with screenshots
4. Open report in browser

## What Gets Tested

- **Functional Correctness**: Edge cases, API failures, state management
- **UX Quality**: Navigation, error messages, accessibility
- **Performance**: Load times, responsiveness
- **Governance Rigor**: Framework citations, risk transparency
- **Professional Polish**: Typos, UI consistency, exports

## Report Location

`stress_test_reports/report_YYYYMMDD_HHMMSS.html`

See `docs/STRESS_TESTING.md` for full documentation.

## Current Findings

See `STRESS_TEST_FINDINGS.md` for detailed analysis and recommendations.

**Health Score:** 82/100 (Good - Demo Quality)

**Top 3 Improvements:**
1. Add demo mode for users without API keys
2. Enhance error messages for API failures  
3. Validate empty input before analysis

