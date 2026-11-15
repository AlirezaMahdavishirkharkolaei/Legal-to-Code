"""The codifiability index: every registered provision, its class, rationale and the ambiguities found."""

from __future__ import annotations

import csv
import io
import json
from collections import Counter

from .core import REGISTRY, RUBRIC


def rows() -> list[dict]:
    out = []
    for p in sorted(REGISTRY.provisions.values(), key=lambda p: (p.instrument, p.id)):
        d = p.to_dict()
        d["ambiguity_count"] = len(p.ambiguities)
        d["implemented"] = bool(p.implemented_by or p.external)
        out.append(d)
    return out


def stats() -> dict:
    r = rows()
    by_class = Counter(x["codifiability"] for x in r)
    by_instrument: dict[str, Counter] = {}
    for x in r:
        by_instrument.setdefault(x["instrument"], Counter())[x["codifiability"]] += 1
    return {
        "provisions": len(r),
        "by_class": {k: by_class.get(k, 0) for k in "ABC"},
        "by_instrument": {k: {c: v.get(c, 0) for c in "ABC"} for k, v in by_instrument.items()},
        "ambiguities": sum(x["ambiguity_count"] for x in r),
        "rules": len(REGISTRY.rules),
    }


def to_csv() -> str:
    buf = io.StringIO()
    cols = ["id", "instrument", "article", "title", "codifiability", "codifiability_label", "rationale",
            "ambiguity_count", "ambiguities", "implemented_by", "external", "status_note"]
    w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for x in rows():
        x = dict(x)
        x["ambiguities"] = " | ".join(x["ambiguities"])
        x["implemented_by"] = " | ".join(x["implemented_by"])
        w.writerow(x)
    return buf.getvalue()


def to_json() -> str:
    return json.dumps({"rubric": RUBRIC, "stats": stats(), "provisions": rows()}, indent=1, ensure_ascii=False)


def to_markdown() -> str:
    s = stats()
    lines = ["# Codifiability index", "",
             f"{s['provisions']} provisions · {s['rules']} executable rules · {s['ambiguities']} documented ambiguities", "",
             "## Rubric", ""]
    for k, v in RUBRIC.items():
        lines.append(f"- **{k} — {v['label']}:** {v['test']}")
    lines += ["", "## Summary", "", "| Instrument | A | B | C |", "|---|---|---|---|"]
    for inst, c in s["by_instrument"].items():
        lines.append(f"| {inst} | {c['A']} | {c['B']} | {c['C']} |")
    lines.append(f"| **All** | **{s['by_class']['A']}** | **{s['by_class']['B']}** | **{s['by_class']['C']}** |")
    current = None
    for x in rows():
        if x["instrument"] != current:
            current = x["instrument"]
            lines += ["", f"## {current}", ""]
        impl = ", ".join(f"`{r}`" for r in x["implemented_by"]) or (f"[external]({x['external']})" if x["external"] else "—")
        lines.append(f"### {x['article']} — {x['title']} · class {x['codifiability']} ({x['codifiability_label']})")
        lines += ["", x["summary"], "", f"*Why:* {x['rationale']}  ", f"*Implemented by:* {impl}"]
        if x["ambiguities"]:
            lines += ["", "*Ambiguities found:*"] + [f"- {a}" for a in x["ambiguities"]]
        if x["status_note"]:
            lines += ["", f"*Status:* {x['status_note']}"]
        lines.append("")
    return "\n".join(lines)
