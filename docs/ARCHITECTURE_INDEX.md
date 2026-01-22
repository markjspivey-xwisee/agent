# Architecture & Spec Index

This document is the source-of-truth checklist. No pillar may be omitted.

## Fundamental Pillars Checklist

### A) Abstract Agent Types (AAT)
- AAT definitions (allowed/forbidden action types, invariants, required trace rules).
- AAT-to-affordance rule: broker must not emit affordances outside the AAT.
- AAT composition/refinement notes (stub acceptable for MVP).

### B) Context Graphs
- Context nodes include agent DID, capabilities, constraints, timestamps, scope.
- Affordances are hypermedia controls: `rel`, `actionType`, `target`, params, effects.
- Affordances appear/disappear based on context + proofs + policy.

### C) Hypermedia Orientation (HATEOAS)
- No global tool list to agents.
- Agent must consume only broker-provided affordances.
- “Discover at runtime” language is explicit in specs.

### D) Affordance Theory
- Affordances are relational (agent × environment × norms).
- Capabilities/constraints live in context.
- Parameters are typed forms (JSON Schema/SHACL).

### E) Causality
- Affordances may carry `causalSemanticsRef`.
- Explicit intervention label (`do(action, params)` is referenced).
- ICausalEvaluator exists, even if stubbed.

### F) Policy
- Deontic layer (permit/deny/duty) governs affordance existence.
- Outcome constraints use causal predictions to gate traversal/escalation.

### G) Provenance & Audit (PROV)
- Every traversal yields an immutable trace.
- Trace binds context snapshot, affordance, proofs, parameters, outcomes.

### H) Decentralization (DIDs/VCs)
- Agent identity is DID.
- Capability gating uses VC/VP verification.
- OID4VCI and DIDComm are target types in the schema.

### I) Emergent Semiotics
- `rel` labels treated as conventions with versions.
- Log usage outcomes to measure drift and stability.
- Semantics observatory spec stub exists.

### J) Threat Model & Safety Invariants
- Covers stale context replay, proof replay, confused deputy, proof stripping,
  trace omission, capability escalation via mislabeled affordances.

## Spec-to-Code Coverage Table (Required)
| Pillar | Spec | Schema/Shape | Example | Test |
| --- | --- | --- | --- | --- |
| AAT | `spec/aat/*.json` | `spec/shacl/aat-safety.ttl` | `examples/golden-path/context-fragment.json` | `tests/negative/README.md` |
| Context Graph | `spec/cgp.md` | `spec/context-graph.schema.json` | `examples/golden-path/context-fragment.json` | `tests/negative/README.md` |
| Hypermedia | `docs/hypermedia-principles.md` | `spec/context-graph.schema.json` | `examples/golden-path/context-fragment.json` | `tests/negative/README.md` |
| Affordances | `docs/affordances.md` | `spec/shacl/affordance.ttl` | `examples/golden-path/context-fragment.json` | `tests/negative/README.md` |
| Causality | `spec/causal-affordance.md` | `spec/context-graph.schema.json` | `examples/golden-path/context-fragment.json` | `tests/negative/README.md` |
| Policy | `docs/policy.md` | `spec/context-graph.schema.json` | `examples/golden-path/context-fragment.json` | `tests/negative/README.md` |
| Provenance | `docs/prov.md` | `spec/prov-trace.schema.json` | `examples/golden-path/prov-trace.json` | `tests/negative/README.md` |
| Identity | `docs/decentralized-identity.md` | `spec/context-graph.schema.json` | `examples/golden-path/context-fragment.json` | `tests/negative/README.md` |
| Semiotics | `docs/semiotics.md` | `spec/telemetry.md` | `examples/golden-path/context-fragment.json` | `tests/negative/README.md` |
| Threat Model | `docs/20-threat-model.md` | `docs/20-threat-model.md` | `examples/golden-path/negative/README.md` | `tests/negative/README.md` |

**No pull request may be merged unless this table is updated.**
