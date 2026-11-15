"""Command line.

    l2c index                       # codifiability index (Markdown); --format csv|json
    l2c rules                       # executable rules and the provisions they implement
    l2c run oecd_mtc.withholding_rate '{"income": "dividends", "recipient_is_company": true, "holding_share": 0.3, "holding_days": 400}'
    l2c run wto_dsu.timeline '{"consultations_requested": "2026-01-15", "panel_established": "2026-04-20"}'
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date

from . import REGISTRY, __version__, index


def _parse_dates(obj):
    if isinstance(obj, dict):
        return {k: _parse_dates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_parse_dates(v) for v in obj]
    if isinstance(obj, str) and len(obj) == 10 and obj[4] == "-" and obj[7] == "-":
        try:
            return date.fromisoformat(obj)
        except ValueError:
            return obj
    return obj


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="l2c", description="Legal-to-Code: international law rules as traceable code.")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("index", help="print the codifiability index")
    pi.add_argument("--format", choices=["md", "csv", "json"], default="md")
    sub.add_parser("rules", help="list executable rules")
    pr = sub.add_parser("run", help="run a rule with JSON arguments")
    pr.add_argument("rule")
    pr.add_argument("args", nargs="?", default="{}")
    pr.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    if a.cmd == "index":
        print({"md": index.to_markdown, "csv": index.to_csv, "json": index.to_json}[a.format]())
    elif a.cmd == "rules":
        for name, fn in sorted(REGISTRY.rules.items()):
            print(f"{name:<45} {', '.join(fn.provision_ids)}")
    else:
        fn = REGISTRY.rules.get(a.rule)
        if fn is None:
            print(f"error: unknown rule '{a.rule}'. See: l2c rules", file=sys.stderr)
            return 2
        try:
            kwargs = _parse_dates(json.loads(a.args))
            res = fn(**kwargs)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(res.to_dict(), indent=1, default=str) if a.json else res.explain())
    return 0


if __name__ == "__main__":
    sys.exit(main())
