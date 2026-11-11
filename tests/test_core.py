import pytest
from agent_bridge.core import adapt, validate_record, ADAPTERS

def test_two_adapters_only():
    assert set(ADAPTERS) == {"aag", "flight-recorder"}

def test_aag_adapter():
    r = adapt("aag", {"agent_id": "a1", "action": "payments.refund", "decision": "deny", "reason": "over limit", "id": "d1"})
    assert r["decision"] == "DENY" and r["source"] == "agent-auth-gateway"
    assert validate_record(r)

def test_flight_recorder_adapter():
    r = adapt("flight-recorder", {"agent_id": "a1", "event_type": "tool.call", "event_id": "e1"})
    assert r["kind"] == "recorded-event" and r["decision"] is None
    assert validate_record(r)

def test_unknown_target_rejected():
    with pytest.raises(ValueError):
        adapt("some-vendor", {})

def test_missing_fields_rejected():
    with pytest.raises(ValueError):
        adapt("aag", {"agent_id": "a1"})
