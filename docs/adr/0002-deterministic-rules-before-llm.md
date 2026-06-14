# ADR 0002: Run deterministic rules before the LLM

Status: Accepted

## Context

The project inspects fake banking transactions and explains the result with a
local LLM. Important classification decisions should not depend only on
generated text.

## Decision

Apply deterministic Python rules first in `src/banking_ai/rules.py`. The
`SUSPICIOUS` / `NORMAL` status is decided by the rules. The local Ollama model
only explains the already-decided result in plain language. Each rule returns a
structured `RuleFinding` with `rule_id`, `severity`, `reason`, and
`relevant_fields`.

## Consequences

- The status is predictable and testable without a model or network.
- The LangGraph node order is `load_transaction -> apply_rules ->
  generate_ai_explanation -> finalize_result`.
- The LLM prompt receives the triggered findings and their severity so the
  explanation stays consistent with the deterministic decision.
- This is a teaching pattern, not a production fraud-detection system.
