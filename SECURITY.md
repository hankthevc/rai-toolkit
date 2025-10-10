# Security Policy

## Key Judgments
- This toolkit prioritizes defensive, governance-focused analysis. It does not expose or encourage offensive techniques.
- **This is a learning prototype.** It is not intended for processing actual sensitive data or production use.
- Security vulnerabilities should be reported privately so fixes can be prepared before public disclosure.

## Data Handling & Privacy

**No sensitive data collection:** The live demo runs as a server-side Streamlit session. Assessment data exists only for the session and is not persisted to a database.

**AI analysis data flow:**
- When using AI-powered analysis, scenario descriptions are sent to OpenAI API
- Risk calculations happen server-side during your session
- Nothing is permanently stored

**For local deployments:**
- Run locally to control data flow entirely
- Review OpenAI's terms of service before sending any data to their API
- Do not process actual sensitive or production data with this prototype

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

**For non-sensitive bugs:** Open a GitHub Issue with reproduction steps.

**For potential security vulnerabilities:** Email <security@users.noreply.github.com> with the subject line `RAI-Toolkit Vulnerability Report`.

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
