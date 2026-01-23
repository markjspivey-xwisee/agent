from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT_DIR / "examples" / "golden-path"
SPEC_DIR = ROOT_DIR / "spec"



def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def is_string(value: Any) -> bool:
    return isinstance(value, str)


def require_field(payload: dict[str, Any], key: str, errors: list[str]) -> Any:
    if key not in payload:
        errors.append(f"missing required field '{key}'")
        return None
    return payload[key]


def validate_context_fragment(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    context = require_field(payload, "context", errors)
    affordances = require_field(payload, "affordances", errors)

    if isinstance(context, dict):
        for field in ["id", "agent_did", "generated_at", "scope"]:
            value = require_field(context, field, errors)
            if value is not None and not is_string(value):
                errors.append(f"context.{field} must be a string")
        expires_at = context.get("expires_at")
        if expires_at is not None and not is_string(expires_at):
            errors.append("context.expires_at must be a string")
        capabilities = context.get("capabilities")
        if capabilities is not None and not isinstance(capabilities, list):
            errors.append("context.capabilities must be a list")

    if isinstance(affordances, list):
        for index, affordance in enumerate(affordances):
            if not isinstance(affordance, dict):
                errors.append(f"affordances[{index}] must be an object")
                continue
            for field in ["id", "rel", "actionType", "target", "inputShape"]:
                value = require_field(affordance, field, errors)
                if value is not None and field != "target" and not is_string(value):
                    errors.append(f"affordances[{index}].{field} must be a string")
            target = affordance.get("target")
            if target is not None and not isinstance(target, dict):
                errors.append(f"affordances[{index}].target must be an object")

    return errors


def validate_emit_plan_params(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    plan_id = require_field(payload, "planId", errors)
    summary = require_field(payload, "summary", errors)
    steps = require_field(payload, "steps", errors)

    if plan_id is not None and not is_string(plan_id):
        errors.append("planId must be a string")
    if summary is not None and not is_string(summary):
        errors.append("summary must be a string")
    if steps is not None and not isinstance(steps, list):
        errors.append("steps must be a list")
    return errors


def validate_trace(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in [
        "id",
        "timestamp",
        "context_id",
        "agent_did",
        "affordance_id",
        "params",
        "proofs",
        "target",
    ]:
        value = require_field(payload, field, errors)
        if value is not None and field in {"id", "timestamp", "context_id", "agent_did", "affordance_id"}:
            if not is_string(value):
                errors.append(f"{field} must be a string")
    proofs = payload.get("proofs")
    if proofs is not None and not isinstance(proofs, list):
        errors.append("proofs must be a list")
    return errors


def main() -> int:
    failures: list[str] = []

    context_fragment = load_json(EXAMPLES_DIR / "context-fragment.json")
    failures.extend(
        f"context-fragment.json {msg}" for msg in validate_context_fragment(context_fragment)
    )

    emit_plan_params = load_json(EXAMPLES_DIR / "emit-plan.params.json")
    failures.extend(
        f"emit-plan.params.json {msg}" for msg in validate_emit_plan_params(emit_plan_params)
    )

    prov_trace = load_json(EXAMPLES_DIR / "prov-trace.json")
    failures.extend(
        f"prov-trace.json {msg}" for msg in validate_trace(prov_trace)
    )

    if failures:
        print("Schema validation failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("All example payloads validated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
