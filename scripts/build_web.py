"""Build the browser app into web/dist/ (static; runs the package with Pyodide).

    python scripts/build_web.py && python -m http.server -d web/dist 8000
"""

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB, DIST = ROOT / "web", ROOT / "web" / "dist"
sys.path[:0] = [str(ROOT), str(WEB)]

import bridge  # noqa: E402
from legal_to_code import RUBRIC, __version__, index  # noqa: E402

DEFAULTS = {
    "withholding": ("oecd_mtc.withholding_rate", {"income": "dividends", "beneficial_owner": True, "recipient_is_company": True,
                                                  "holding_share": 0.30, "holding_days": 400}),
    "construction": ("oecd_mtc.construction_pe", {"start": "2025-03-01", "end": "2026-04-15"}),
    "home_office": ("oecd_mtc.home_office_pe", {"share_of_working_time": 0.6}),
    "employment": ("employment_trips", {"trips": "2025-09-01 to 2025-12-09\n2026-01-01 to 2026-04-10",
                                        "fiscal_year_start": "2026-01-01", "fiscal_year_end": "2026-12-31",
                                        "employer_resident_in_work_state": False, "borne_by_pe_in_work_state": False}),
    "residence": ("oecd_mtc.residence_tiebreaker_individual", {"permanent_home": "both", "vital_interests": "undeterminable",
                                                               "habitual_abode": "A"}),
    "dsu": ("wto_dsu.timeline", {"consultations_requested": "2026-01-15", "panel_established": "2026-04-20",
                                 "panel_composed": "2026-06-01", "as_of": "2026-11-15"}),
}


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    bundle = {str(f.relative_to(ROOT)): f.read_text(encoding="utf-8")
              for f in sorted((ROOT / "legal_to_code").rglob("*.py")) if "__pycache__" not in f.parts}
    bundle["bridge.py"] = (WEB / "bridge.py").read_text(encoding="utf-8")
    results = {k: json.loads(bridge.run(rule, json.dumps(args))) for k, (rule, args) in DEFAULTS.items()}
    data = {"version": __version__, "rubric": RUBRIC, "stats": index.stats(), "provisions": index.rows(),
            "defaults": {k: {"rule": r, "args": a} for k, (r, a) in DEFAULTS.items()}, "results": results}
    (DIST / "bundle.json").write_text(json.dumps(bundle), encoding="utf-8")
    (DIST / "data.json").write_text(json.dumps(data, ensure_ascii=False, default=str), encoding="utf-8")
    shutil.copy2(WEB / "index.html", DIST / "index.html")
    print(f"Built {DIST}: {len(bundle)} code files, {len(data['provisions'])} provisions")


if __name__ == "__main__":
    main()
