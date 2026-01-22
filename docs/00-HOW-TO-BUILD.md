# How to Build This System (In Order)

## Phase 1 — Contracts First (No Code)
1. Implement:
   - `spec/context-graph.schema.json`
   - AAT JSON specs
   - `spec/prov-trace.schema.json`
2. Validate golden-path JSON against schemas.
3. Write SHACL safety shapes.

**Stop if schemas are unstable.**

## Phase 2 — Context Broker (Read-Only)
1. Implement `/context` endpoint.
2. Verify DID proof-of-control (stub allowed).
3. Verify VCs (stub allowed).
4. Return golden-path Context Graph fragment.

**No execution yet.**

## Phase 3 — Traversal + Trace
1. Implement `/traverse`.
2. Validate affordance exists, params conform, credentials match.
3. Emit PROV trace.
4. Forward to mock target.

## Phase 4 — Negative Cases
Implement negative tests for missing VC, bad params, untrusted issuer, stale context.
