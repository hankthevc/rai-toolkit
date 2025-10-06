# OWASP LLM Top 10 Crosswalk (Illustrative)

**Key Judgments**
- Links risk modifiers and safeguards to OWASP Large Language Model Top 10 categories for security teams.
- Emphasizes controls for prompt injection, insecure output handling, and supply chain transparency.
- Illustrative only—security engineers should validate coverage through penetration testing and threat modeling.

## Mapping Overview

| OWASP Category | Example Safeguard | Notes |
| --- | --- | --- |
| LLM01 Prompt Injection | Prompt hygiene and red-team testing control | Triggered when modifiers include Cyber or Disinformation. |
| LLM02 Insecure Output Handling | Human-in-the-loop review | Ensures critical outputs receive human validation. |
| LLM07 Sensitive Information Disclosure | PII handling safeguards | Applies when scenarios flag personal or regulated data. |
| LLM09 Model Theft | Inventory and access control | Requires logging and access governance for high-tier systems. |

## Usage Notes
- Use with security incident responders to map governance actions to familiar application security language.
- Update mappings as OWASP guidance evolves or new categories are published.
- Retain the illustrative disclaimer in any security review artifacts derived from this document.
