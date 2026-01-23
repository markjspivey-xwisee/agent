# Context Graph Protocol (MVP Scaffold)

This repository is a scaffold for the Context Graph Protocol (CGP) and related specs.
It includes a minimal broker implementation to serve the golden-path context fragment
and record traversal traces.

## Repository Layout
- `spec/` — canonical contracts and protocol specs
- `docs/` — architecture guides and pillars
- `examples/` — golden-path payloads and negative cases
- `src/` — minimal broker implementation
- `traces/` — generated PROV trace records

## Quickstart (Local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.broker.app:app --reload
```

### Validate Examples
```bash
python scripts/validate_examples.py
```

### Validate Negative Cases
```bash
python scripts/validate_negative_cases.py
```

### Example Requests
```bash
curl -X POST http://127.0.0.1:8000/context \
  -H "Content-Type: application/json" \
  -d @examples/golden-path/request-context.json

curl -X POST http://127.0.0.1:8000/traverse \
  -H "Content-Type: application/json" \
  -d '{
    "context_id": "context:planner-123:2025-01-01T00:00:00Z",
    "affordance_id": "affordance:emit-plan",
    "params": {
      "planId": "plan-001",
      "summary": "Draft route plan for delivery",
      "steps": ["pickup", "route", "dropoff"]
    },
    "proofs": ["vc:planner-capability"],
    "proof_issuers": ["did:example:issuer-1"]
  }'
```
