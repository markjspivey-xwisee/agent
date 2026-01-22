# Abstract Agent Types (AAT)

AATs define the allowed action surface for an agent role and prevent accidental
capability escalation.

## MVP AATs
- **Planner**: can propose plans, cannot actuate.
- **Executor**: can actuate approved actions.
- **Observer**: can read context, cannot traverse.

## Enforcement
- Broker must not emit affordances outside the agent’s AAT.
- SHACL safety shapes express forbidden action types for each AAT.
