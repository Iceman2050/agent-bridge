# AgentBridge

A vendor-neutral **adapter layer** that normalizes policy decisions and
recorded events from two Ingenious AI systems into one evidence schema:

- **Agent Auth Gateway** decisions → `agent-bridge/evidence/v1` policy-decision records
- **Agent Flight Recorder** events → `agent-bridge/evidence/v1` recorded-event records

Exactly **two validated adapters** ship in v0.1.0. Unknown targets are rejected,
and records missing required fields fail loudly instead of being guessed at.

## Connects to

- **Agent Auth Gateway** — https://authgateway.getingeniousai.com
- **Agent Flight Recorder** — https://flightrecorder.getingeniousai.com

## Install

```bash
pip install -e .
```

## Use

```bash
agent-bridge adapt --target aag decision.json --output evidence.json
agent-bridge adapt --target flight-recorder event.json --output evidence.json
agent-bridge validate evidence.json
```

## What this is — and is not

AgentBridge is an adapter and normalization layer. It **records and translates**
decisions and events produced elsewhere. It does not itself enforce policy,
block actions, or sit in the execution path: monitoring and recording are
never enforcement, and this README does not claim otherwise. Enforcement, where
it exists, belongs to the gateway that made the decision.

## Limitations

- Two adapters only (listed above); other vendors are out of scope for v0.1.0.
- Normalization is field-level; semantic equivalence between vendors is not claimed.
- Timestamps and reasons are carried through as supplied, not independently verified.

Built by Ingenious AI — https://getingeniousai.com
