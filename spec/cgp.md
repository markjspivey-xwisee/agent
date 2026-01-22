# Context Graph Protocol (CGP)

## 1. Overview
CGP defines how agents request context fragments and traverse affordances using
verifiable proofs and policy checks.

## 2. Endpoints

### 2.1 POST /context
Returns a Context Graph fragment.

**Inputs**
- `agent_did` (required)
- `verifiable_presentation` (optional)
- `resource_scope` (optional)
- `evidence` (optional)

**Outputs**
- Context Graph fragment (see `spec/context-graph.schema.json`).

### 2.2 POST /traverse
Optional for MVP if traversal is client-side. If supported, it accepts:
- `context_id`
- `affordance_id`
- `params`
- `proofs`

Server MUST:
- validate affordance exists in context
- validate params against `inputShape`
- evaluate policy/credentials
- emit PROV trace and forward to target

## 3. Verification Requirements
- DID proof-of-control verification.
- VC/VP verification via `IVerifier`.
- Issuer trust policy evaluation (allowlist for MVP).

## 4. Affordance Derivation
MVP uses **Enumerated Mode**: broker explicitly lists affordances after evaluation.
Derived mode is future work.

## 5. Hypermedia Constraint
Agents MUST discover actions at runtime via affordances; no global tool list exists.
