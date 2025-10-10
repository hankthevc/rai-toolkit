# RAIS & Enterprise Updates - January 10, 2025

This document summarizes major enhancements to make the RAI Toolkit enterprise-ready and aligned with Microsoft RAIS (Responsible AI Standard).

---

## Must-Do Items ✅ COMPLETED

### 1. RAIS Alignment (Microsoft)
- ✅ **Added RAIS crosswalk document** (`docs/crosswalks/microsoft_rais.md`)
  - Maps toolkit artifacts to RAIS goals: A1 (Impact Assessment), A2 (Sensitive Use Triage), A3 (Fit for Purpose), T2 (Transparency Note), PS1/PS2 (Privacy/Security)
  - Includes illustrative gating rules for escalation
  - Clear caveats that this is based on public RAIS documentation only

- ✅ **Created Transparency Note exporter** (`common/utils/exporters_transparency_note.py`)
  - Generates RAIS T2-aligned stakeholder communication template
  - Includes system description, limitations, data handling, monitoring, and ownership sections
  - Integrated into app UI with download button

- ✅ **Sample Transparency Note** (`docs/samples/sample_transparency_note.md`)
  - Complete example for HealthAssist chatbot scenario
  - Shows how to populate all required sections

- ✅ **Sensitive use gating example** (`common/utils/risk_engine.py::check_sensitive_use_gating`)
  - Illustrative A2 (Sensitive/Restricted Use Triage) implementation
  - Detects biometric ID, irreversible decisions, dual-use risk, protected populations
  - Returns escalation flags and required approval levels

### 2. U.S. Federal Policy Updates
- ✅ **Updated to OMB M-25-21** (replaces M-24-10, effective Jan 2025)
  - Updated `common/policy_packs/us_omb_ai_policy.yaml`
  - Added note about M-25-22 (acquisition, replaces M-24-18)
  - Updated README crosswalk table

### 3. Tone & Positioning
- ✅ **Removed "vibecoded" language** from README
  - Replaced with: "Built with AI coding assistance (Cursor/Claude) to prioritize governance logic; test-backed and CI-gated"
  - Moved "About the Author" section to bottom of README
  - Made README product-first, not portfolio-first

### 4. Model Vendor Posture & Data Handling
- ✅ **Added Azure OpenAI env vars** in README Quickstart
  - Shows both OpenAI and Azure OpenAI configuration options
  - **Recommends Azure OpenAI for enterprise** deployments
  
- ✅ **Added Data Handling & Privacy section** to README
  - States no sensitive data stored, session-only assessment data
  - Clarifies what goes to OpenAI API vs. what stays local
  - Recommends Azure OpenAI for data residency and compliance

- ✅ **Updated SECURITY.md** with data handling statement
  - No collection/storage/logging of assessment data
  - AI analysis data flow clearly explained
  - Support window and dependency update policy

### 5. EU AI Act Precision
- ✅ **Added Official Journal reference** in README crosswalk table
  - Links to EUR-Lex L 178/2024
  - Notes Annex III high-risk categories and Article 52 transparency obligations
  - Emphasizes "illustrative examples, not full conformity process"

### 6. OWASP LLM Top-10 Versioning
- ✅ **Added 2025 reference** in README crosswalk table
  - Links to current OWASP LLM Top 10 page
  - Notes LLM01 (prompt injection), LLM06 (data leakage), LLM05 (supply chain)

### 7. Live Demo Reliability Note
- ✅ **Sleep warning surfaced at top** of README
  - Added ⏰ icon and "wakes in 30-60s" note next to demo link
  - Keeps existing note lower in README for completeness

### 8. Dependency Pinning & Supply-Chain Hygiene
- ✅ **Pinned all requirements** to exact versions (`requirements.txt`)
  - Changed `openai>=1.54.0` → `openai==1.54.3`

- ✅ **Added Dependabot config** (`.github/dependabot.yml`)
  - Weekly Python dependency checks
  - Monthly GitHub Actions checks
  - Groups minor/patch updates, separates major versions

---

## Should-Do Items ✅ COMPLETED

### 1. RAIS Artifacts in Code
- ✅ **Transparency Note exporter** (`common/utils/exporters_transparency_note.py`)
  - Shows how intake fields populate T2 artifact
  - Includes sections for capabilities, limitations, data handling, monitoring, ownership

- ✅ **Integrated into app** (`project1_risk_framework/app.py`)
  - Download button for Transparency Note (stub) alongside Decision Record
  - Both artifacts available for AI-driven and manual assessments

### 2. Restricted/Sensitive Use Gating Rule Example
- ✅ **Added `check_sensitive_use_gating()` function** to `risk_engine.py`
  - Generic gating pattern (no internal lists)
  - Flags biometric ID + real-time classification
  - Returns escalation reason and approval level (e.g., "Executive + Legal Sign-Off")
  - Called "illustrative RAIS gating" in docstring

### 3. One-Click Deploy
- ✅ **Added "Deploy to Streamlit Cloud" badge** in README
  - Links to Streamlit deploy page with instructions

- ✅ **Created Dockerfile** and `.dockerignore`
  - Minimal Python 3.11 image
  - Supports both OpenAI and Azure OpenAI env vars
  - Health check included
  - Docker run snippets in README

### 4. CITATION.cff
- ✅ **Added CITATION.cff** for proper academic/research citation
  - Includes all framework references (NIST, EU AI Act, ISO 42001, OWASP, MITRE, RAIS, OMB)
  - Enables GitHub's "Cite this repository" feature

### 5. README Hierarchy
- ✅ **Moved "About the Author" to bottom** of README
  - README now product-first (Quickstart → Features → Deployment → Documentation → Author)

### 6. Terminology Consistency
- ✅ **Standardized on:**
  - "safeguards" or "controls" (used interchangeably with policy pack context)
  - "risk tier" (Low/Medium/High/Critical)
  - "policy packs" (YAML-encoded governance frameworks)

---

## Additional Enhancements

### NIST GenAI Profile
- ✅ **Added note in README** crosswalk table
  - "Supports MAP-1.5 (supply chain), GOVERN-1.5 (data governance), NIST GenAI Profile risk areas"

### ISO/IEC 42001 AIMS Patterns
- ✅ **Added note in README** crosswalk table
  - "AIMS documentation patterns (risk log, transparency note, decision record)"
  - "Decision Record aligned to ISO audit expectations"

### Policy Framework Table
- ✅ **Created comprehensive crosswalk table** in README
  - Columns: Framework | Alignment | Key Artifacts Generated
  - Includes RAIS, NIST, EU AI Act, ISO 42001, OMB M-25-21, OWASP 2025, MITRE ATLAS, GDPR
  - Clear disclaimers about illustrative nature

---

## Files Created

1. `docs/crosswalks/microsoft_rais.md` - RAIS alignment documentation
2. `common/utils/exporters_transparency_note.py` - T2 artifact generator
3. `docs/samples/sample_transparency_note.md` - Example transparency note
4. `.github/dependabot.yml` - Dependency update automation
5. `CITATION.cff` - Academic citation metadata
6. `Dockerfile` - Container image for deployment
7. `.dockerignore` - Docker build optimization
8. `RAIS_ENTERPRISE_UPDATES.md` - This file

---

## Files Modified

1. `README.md` - RAIS table, Azure OpenAI, data handling, tone changes, author moved to bottom
2. `SECURITY.md` - Data handling statement, support window
3. `requirements.txt` - Pinned openai==1.54.3
4. `common/policy_packs/us_omb_ai_policy.yaml` - Updated to M-25-21
5. `common/utils/risk_engine.py` - Added `check_sensitive_use_gating()` function
6. `project1_risk_framework/app.py` - Added Transparency Note import and download buttons

---

## Deployment Checklist

For Microsoft or enterprise deployment, teams should:

1. ✅ Review RAIS crosswalk (`docs/crosswalks/microsoft_rais.md`)
2. ✅ Configure Azure OpenAI (not public OpenAI API)
3. ✅ Customize sensitive use gating rules (`risk_engine.py::check_sensitive_use_gating`)
4. ✅ Validate policy packs with legal/compliance teams
5. ✅ Complete Transparency Note template fields (stubs provided)
6. ✅ Set up Dependabot for security updates
7. ✅ Deploy via Docker or Streamlit Cloud
8. ⚠️ Do not process actual sensitive data without legal/privacy/security sign-off

---

## What's NOT Included (Intentionally)

Per user feedback, we did NOT add:
- ❌ **No-API-key path** - User confirmed "there's no reason anyone should need that"
- ❌ **Stress agent / Playwright testing** - Scrapped due to Streamlit Cloud bot protection

---

## References

- [Microsoft RAIS](https://www.microsoft.com/en-us/ai/responsible-ai)
- [OMB M-25-21](https://www.whitehouse.gov/omb/briefing-room/)
- [EU AI Act Official Journal](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)
- [OWASP LLM Top 10 (2025)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html)
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)

---

**Last Updated:** January 10, 2025  
**Status:** Ready for enterprise review and deployment validation

