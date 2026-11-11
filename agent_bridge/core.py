import json
from pathlib import Path

# Exactly two validated adapters in v0.1.0. Adding one requires tests here first.
ADAPTERS = ("aag", "flight-recorder")

def _require(obj, fields, source):
    missing = [f for f in fields if f not in obj]
    if missing:
        raise ValueError(f"{source} record missing required fields: {missing}")

def adapt_aag(obj):
    """Normalize an Agent Auth Gateway decision record."""
    _require(obj, ["agent_id", "action", "decision"], "aag")
    return {
        "schema": "agent-bridge/evidence/v1",
        "source": "agent-auth-gateway",
        "kind": "policy-decision",
        "agent_id": obj["agent_id"],
        "action": obj["action"],
        "decision": str(obj["decision"]).upper(),
        "reason": obj.get("reason"),
        "timestamp": obj.get("timestamp"),
        "raw_ref": obj.get("id"),
    }

def adapt_flight_recorder(obj):
    """Normalize an Agent Flight Recorder event record."""
    _require(obj, ["agent_id", "event_type"], "flight-recorder")
    return {
        "schema": "agent-bridge/evidence/v1",
        "source": "agent-flight-recorder",
        "kind": "recorded-event",
        "agent_id": obj["agent_id"],
        "action": obj["event_type"],
        "decision": None,
        "reason": obj.get("summary"),
        "timestamp": obj.get("timestamp"),
        "raw_ref": obj.get("event_id"),
    }

_FUNCS = {"aag": adapt_aag, "flight-recorder": adapt_flight_recorder}

def adapt(target, obj):
    if target not in _FUNCS:
        raise ValueError(f"unknown adapter target: {target!r}; validated targets: {sorted(_FUNCS)}")
    return _FUNCS[target](obj)

def adapt_file(target, src, out):
    obj = json.loads(Path(src).read_text())
    record = adapt(target, obj)
    Path(out).write_text(json.dumps(record, indent=2) + "\n")
    return record

def validate_record(obj):
    required = ["schema", "source", "kind", "agent_id", "action"]
    _require(obj, required, "evidence")
    if obj["schema"] != "agent-bridge/evidence/v1":
        raise ValueError(f"unsupported schema: {obj['schema']!r}")
    return True
