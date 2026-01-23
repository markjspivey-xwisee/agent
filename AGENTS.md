# AGENTS.md — Non-Negotiable Rules

These rules apply to all contributors (humans and agents).

## Absolute Invariants
1. **No global tool lists** — agents may only act via broker-provided affordances.
2. **Affordance absence = enforcement** — if an action is not afforded, it must not be attempted.
3. **AAT safety is structural** — illegal actions must not exist in the Context Graph.
4. **Credentials are explicit** — never infer authority; only verified VCs/VPs.
5. **Every action is traceable** — every traversal emits a PROV trace with proof binding.
6. **Causality is external** — causal reasoning belongs in ICausalEvaluator, not ad-hoc LLM logic.
7. **Meaning is not hard-coded** — affordance labels are conventions; trust documented effects only.

## Forbidden Patterns
- Hard-coded workflows
- Hidden permissions
- Silent side effects
- "Best guess" authority
- Action without provenance
- Agents deciding what they are allowed to do

## Definition of Done (MVP)
- Context Graph validates against schema.
- SHACL shapes pass.
- Golden-path example runs end-to-end.
- Negative tests fail correctly.
- PROV trace emitted for traversal.

## Testing
There are no automated tests yet. When added, document the exact commands here.

## PR Checklist (MVP)
- Update spec schemas and examples together.
- Keep `docs/ARCHITECTURE_INDEX.md` coverage table current.
