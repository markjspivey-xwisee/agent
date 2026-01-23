# Affordances

Affordances are relational: they exist only for a specific agent in a specific context
with specific norms and proofs.

## Required Fields
- `rel`
- `actionType`
- `target`
- `inputShape`

## Optional Fields
- `policyRef`
- `causalSemanticsRef`
- `credentialRequirements`

## Parameter Shapes
Parameter schemas live in JSON Schema and/or SHACL. For example:
- `spec/emit-plan.params.schema.json`
- `spec/shacl/emit-plan-params.ttl`
