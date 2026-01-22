# Causal Affordance Spec (Stub)

Affordances may carry `causalSemanticsRef` to describe expected outcomes.

## Fields
- `intervention`: a label describing the action in `do(action, params)` terms.
- `outcomes`: possible outcomes and risk indicators.

## MVP Rule
No causal evaluation is required, but the reference MUST be present when defined
and the ICausalEvaluator interface MUST exist.
