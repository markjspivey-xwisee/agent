# Task Breakdown (MVP)

1. Implement schema validators (Context + Affordance + Params).
2. Implement DID verification stub (pluggable; mock DID resolver).
3. Implement VC verification stub (accept pre-verified VP).
4. Implement policy allowlist (trusted issuer + required schema).
5. Implement `/context` broker to return golden-path fragment.
6. Implement `/traverse` that:
   - validates affordance exists in context
   - validates params against input shape
   - records PROV trace (with proof references)
   - calls HTTP target
7. Add negative tests (missing VC, bad params, untrusted issuer, stale context).
