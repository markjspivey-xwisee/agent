# Threat Model (MVP)

## Key Risks
- **Replay attacks on VPs**: stale presentations reused to obtain affordances.
- **Stale contexts**: old context fragments used after constraints change.
- **Confused deputy**: planner afforded executor-only actions.
- **Proof stripping**: traversal attempted without proofs.
- **Logging gaps**: trace emitted without binding to proofs.

## Mitigations (MVP)
- Nonce + timestamp binding on proofs (VPs or signed requests).
- Context expiry timestamps and enforcement in broker.
- AAT safety shapes: no executor affordances for planner agents.
- Require proofs for traversal and bind to trace record.
- Trace schema includes proof references.
