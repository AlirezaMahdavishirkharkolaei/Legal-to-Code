"""Browser bridge (Pyodide): run a rule from JSON and return JSON."""

import json
from datetime import date, timedelta

from legal_to_code import REGISTRY
from legal_to_code.cli import _parse_dates


def _trips_to_days(text: str) -> list:
    days = set()
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.replace("–", " to ").split(" to ")]
        start = date.fromisoformat(parts[0])
        end = date.fromisoformat(parts[1]) if len(parts) > 1 and parts[1] else start
        if end < start:
            raise ValueError(f"Trip ends before it starts: {line}")
        d = start
        while d <= end:
            days.add(d)
            d += timedelta(days=1)
    return sorted(days)


def run(name: str, args_json: str) -> str:
    args = json.loads(args_json)
    if name == "employment_trips":
        days = _trips_to_days(args.pop("trips", ""))
        fy_s, fy_e = date.fromisoformat(args["fiscal_year_start"]), date.fromisoformat(args["fiscal_year_end"])
        count = REGISTRY.rules["oecd_mtc.max_days_any_12_months"](days, fy_s, fy_e)
        emp = REGISTRY.rules["oecd_mtc.employment_income"](
            count.outcome, args.get("employer_resident_in_work_state", False), args.get("borne_by_pe_in_work_state", False))
        out = emp.to_dict()
        out["trace"] = count.to_dict()["trace"] + out["trace"]
        out["summary"] = f"{count.outcome} days in the worst twelve-month window. {emp.summary}"
        return json.dumps(out, default=str)
    res = REGISTRY.rules[name](**_parse_dates(args))
    return json.dumps(res.to_dict(), default=str)
