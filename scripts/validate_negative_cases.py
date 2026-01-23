from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT_DIR / "examples" / "golden-path"
NEGATIVE_DIR = EXAMPLES_DIR / "negative"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def parse_timestamp(value: str) -> datetime:
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value)


def validate_negative_cases() -> list[str]:
    failures: list[str] = []

    invalid_params = load_json(NEGATIVE_DIR / "invalid-params.json")
    if isinstance(invalid_params.get("planId"), str):
        failures.append("invalid-params.json should have non-string planId")

    missing_vc = load_json(NEGATIVE_DIR / "missing-vc.json")
    proofs = missing_vc.get("proofs")
    if proofs:
        failures.append("missing-vc.json should have empty proofs")

    untrusted = load_json(NEGATIVE_DIR / "untrusted-issuer.json")
    proof_issuers = untrusted.get("proof_issuers", [])
    allowlist = ["did:example:issuer-1"]
    if set(proof_issuers).intersection(set(allowlist)):
        failures.append("untrusted-issuer.json should not include allowlisted issuer")

    stale_context = load_json(NEGATIVE_DIR / "stale-context.json")
    expires_at = stale_context.get("expires_at")
    if not expires_at:
        failures.append("stale-context.json must include expires_at")
    else:
        expiry = parse_timestamp(expires_at)
        if expiry > datetime.now(timezone.utc):
            failures.append("stale-context.json expires_at should be in the past")

    return failures


def main() -> int:
    failures = validate_negative_cases()
    if failures:
        print("Negative case validation failed:")
        for item in failures:
            print(f"- {item}")
        return 1
    print("All negative cases validated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
