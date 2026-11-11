import argparse, json, sys
from agent_bridge.core import ADAPTERS, adapt_file, validate_record
from pathlib import Path

def main(argv=None):
    ap = argparse.ArgumentParser(prog="agent-bridge", description="Vendor-neutral policy/evidence adapters to Agent Auth Gateway + Agent Flight Recorder. Adapter layer only — it records and normalizes; it does not enforce policy.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("adapt"); a.add_argument("--target", required=True, choices=list(ADAPTERS)); a.add_argument("input"); a.add_argument("--output", "-o", required=True)
    v = sub.add_parser("validate"); v.add_argument("input")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "adapt":
            rec = adapt_file(args.target, args.input, args.output)
            print(json.dumps(rec, indent=2)); return 0
        if args.cmd == "validate":
            validate_record(json.loads(Path(args.input).read_text())); print("valid agent-bridge/evidence/v1 record"); return 0
    except (ValueError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr); return 2
    return 2
