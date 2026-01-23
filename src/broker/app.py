from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from jsonschema import Draft202012Validator

from src.trace.sink import FileTraceSink
ROOT_DIR = Path(__file__).resolve().parents[2]
EXAMPLES_DIR = ROOT_DIR / "examples" / "golden-path"
SPEC_DIR = ROOT_DIR / "spec"
TRACE_DIR = ROOT_DIR / "traces"
TRACE_SINK = FileTraceSink(TRACE_DIR)

CONTEXT_SCHEMA_PATH = SPEC_DIR / "context-graph.schema.json"
TRACE_SCHEMA_PATH = SPEC_DIR / "prov-trace.schema.json"
EMIT_PLAN_SCHEMA_PATH = SPEC_DIR / "emit-plan.params.schema.json"

CONTEXT_FRAGMENT_PATH = EXAMPLES_DIR / "context-fragment.json"

app = FastAPI(title="Context Graph Broker", version="0.1.0")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def validate_json(schema_path: Path, payload: dict[str, Any]) -> None:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda err: err.path)
    if errors:
        message = "; ".join(
            f"{list(error.path)}: {error.message}" for error in errors
        )
        raise HTTPException(status_code=400, detail=message)


def resolve_input_schema(input_shape: str) -> Path:
    if input_shape.endswith("emit-plan.params.schema.json"):
        return EMIT_PLAN_SCHEMA_PATH
    raise HTTPException(status_code=400, detail="Unknown inputShape")


def parse_timestamp(value: str) -> datetime:
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value)


@dataclass
class ContextBundle:
    context: dict[str, Any]
    affordances: list[dict[str, Any]]
    causal_semantics: list[dict[str, Any]]


def load_context_bundle() -> ContextBundle:
    fragment = load_json(CONTEXT_FRAGMENT_PATH)
    validate_json(CONTEXT_SCHEMA_PATH, fragment)
    return ContextBundle(
        context=fragment["context"],
        affordances=fragment["affordances"],
        causal_semantics=fragment.get("causalSemantics", []),
    )


@app.post("/context")
async def get_context(payload: dict[str, Any]) -> JSONResponse:
    agent_did = payload.get("agent_did")
    if not agent_did:
        raise HTTPException(status_code=400, detail="agent_did is required")

    bundle = load_context_bundle()
    if agent_did != bundle.context.get("agent_did"):
        raise HTTPException(status_code=403, detail="Unknown agent DID")

    response = {
        "context": bundle.context,
        "affordances": bundle.affordances,
        "causalSemantics": bundle.causal_semantics,
    }
    validate_json(CONTEXT_SCHEMA_PATH, response)
    return JSONResponse(content=response)


@app.post("/traverse")
async def traverse(payload: dict[str, Any]) -> JSONResponse:
    context_id = payload.get("context_id")
    affordance_id = payload.get("affordance_id")
    params = payload.get("params")
    proofs = payload.get("proofs")
    proof_issuers = payload.get("proof_issuers", [])

    if not context_id or not affordance_id:
        raise HTTPException(status_code=400, detail="context_id and affordance_id required")
    if params is None:
        raise HTTPException(status_code=400, detail="params are required")
    if not isinstance(proofs, list) or not proofs:
        raise HTTPException(status_code=400, detail="proofs must be a non-empty list")

    bundle = load_context_bundle()
    if context_id != bundle.context.get("id"):
        raise HTTPException(status_code=404, detail="Unknown context_id")

    expires_at = bundle.context.get("expires_at")
    if expires_at:
        expiry = parse_timestamp(expires_at)
        if expiry <= datetime.now(timezone.utc):
            raise HTTPException(status_code=403, detail="Context has expired")

    affordance = next(
        (item for item in bundle.affordances if item.get("id") == affordance_id),
        None,
    )
    if not affordance:
        raise HTTPException(status_code=404, detail="Unknown affordance_id")

    input_schema_path = resolve_input_schema(affordance["inputShape"])
    validate_json(input_schema_path, params)

    for requirement in affordance.get("credentialRequirements", []):
        schema_ref = requirement.get("schema")
        if schema_ref and schema_ref not in proofs:
            raise HTTPException(status_code=403, detail="Missing required credential")
        allowlist = requirement.get("issuerPolicy", {}).get("allowlist", [])
        if allowlist and not set(allowlist).intersection(set(proof_issuers)):
            raise HTTPException(status_code=403, detail="Untrusted credential issuer")

    trace_record = {
        "id": f"trace:{affordance_id}:{datetime.now(timezone.utc).isoformat()}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "context_id": bundle.context["id"],
        "agent_did": bundle.context["agent_did"],
        "affordance_id": affordance_id,
        "params": params,
        "proofs": proofs,
        "intervention": affordance.get("causalSemanticsRef"),
        "outcome": {"status": "accepted"},
        "target": affordance["target"],
    }

    validate_json(TRACE_SCHEMA_PATH, trace_record)
    TRACE_SINK.write(trace_record)

    return JSONResponse(content={"status": "ok", "trace_id": trace_record["id"]})
