# Engine Interfaces (Stable Contracts)

These interfaces prevent hard-coding today’s assumptions into tomorrow’s architecture.

## IVerifier
- Responsibility: DID proof-of-control verification and VC/VP verification.
- Inputs: `agent_did`, `verifiable_presentation` (or reference).
- Outputs: verified claims + proof metadata.

## IPolicyEngine
- Responsibility: evaluate policy rules (ODRL-ish) to decide affordance existence.
- Inputs: context, claims, policy reference, evidence.
- Outputs: allow/deny + rationale.

## ICausalEvaluator
- Responsibility: evaluate predicted outcomes for an intervention.
- Inputs: affordance, params, evidence.
- Outputs: predicted outcomes + risk metrics.

## ITraceSink
- Responsibility: persist PROV trace records.
- Inputs: trace object.
- Outputs: durable trace ID.
