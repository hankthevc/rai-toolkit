# Security Policy

## Key Judgments
- This toolkit prioritizes defensive, governance-focused analysis. It does not expose or encourage offensive techniques.
- Security vulnerabilities should be reported privately so fixes can be prepared before public disclosure.
- **This is a demonstration tool.** It is not intended for processing actual sensitive data or production use without validation by legal, privacy, and security teams.

## Data Handling & Privacy

**No sensitive data collection:** This application does not collect, store, or log assessment text or user inputs. All assessment data exists only in browser memory during your session.

**AI analysis data flow:**
- When using AI-powered analysis, scenario descriptions are sent to OpenAI API (or Azure OpenAI if configured)
- No assessment data is persisted to a database by this application
- Risk calculations and policy matching happen locally in your browser

**For production deployments:**
- Use Azure OpenAI for data residency and compliance guarantees
- Run locally (no external API calls except when AI analysis is used)
- For air-gapped environments: disable AI analysis and use manual form input only
- Validate with legal, privacy, and security teams before processing actual sensitive data

## Support Window

**Tested environment:**
- Python 3.11+
- Dependencies pinned in `requirements.txt`
- GitHub Actions CI validates all commits to `main`

**Support commitment:**
- Bug fixes for security issues: Best effort within 10 business days
- Dependency updates: Quarterly review of pinned versions
- This is a demonstration project; enterprise support is not provided

## Reporting a Vulnerability
Email security issues to <hankthevc@users.noreply.github.com> with the subject line `RAI-Toolkit Vulnerability Report`.

Please include:
- Description of the issue and potential impact
- Steps to reproduce (if available)
- Suggested mitigations or references
- Your contact information for follow-up

We aim to acknowledge new reports within five business days and share remediation timelines within ten business days.

## Disclosure Expectations
- Please do not create public issues for security findings until a fix is released.
- Avoid tests that could degrade availability or compromise user data.
- We will credit reporters in release notes upon request.
