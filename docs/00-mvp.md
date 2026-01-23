# MVP Scope and Non-Goals

## Non-Negotiable MVP Scope
- A **Context Broker** returns a Context Graph fragment for an agent DID.
- **Affordances are VC-gated** (at least one capability VC required).
- Each affordance includes:
  - `rel`
  - `actionType`
  - `target`
  - `inputShape`
  - optional `policyRef`
  - optional `causalSemanticsRef`
- Traversal produces a **PROV trace record**.
- One execution target is supported end-to-end:
  - **HTTP POST** tool router (fastest MVP path).

## Explicit Non-Goals
- No full DID method zoo (support 1–2 resolver backends).
- No full do-calculus engine (only causal references + pluggable evaluator).
- No global knowledge graph (only context graph fragments).

## Why This Exists
This document prevents scope creep and ensures coding agents implement to contract.
