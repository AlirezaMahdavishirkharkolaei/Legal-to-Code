# Legal-to-Code

[![tests](https://github.com/AlirezaMahdavishirkharkolaei/Legal-to-Code/actions/workflows/tests.yml/badge.svg)](https://github.com/AlirezaMahdavishirkharkolaei/Legal-to-Code/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Rules of international economic law as tested, traceable code, and a systematic answer to the question of which rules can be coded at all.**

Legal-to-Code is a research framework for *rules as code* in international law. Every provision it covers is:

1. **Classified** by codifiability:
   * **A – Computable:** code can apply the rule end to end.
   * **B – Structurable:** code can sequence the test, but a legal judgment remains.
   * **C – Not codifiable:** code can only document the rule.
2. **Implemented** as a rule that returns a result *and a trace*. Each step in the trace names the provision it applies, and the rule stops wherever a judgment is needed rather than guessing.
3. **Annotated** with the **ambiguities found while encoding it**. Translating law into code forces every condition to be explicit, so gaps and open textures in the drafting surface along the way. These notes are a research output in their own right.

The registry of classified provisions forms the **codifiability index**: [docs/codifiability-index.md](docs/codifiability-index.md), also available as CSV or JSON.

## What is covered (v0.1)

| Module | Provisions | Executable rules |
|---|---|---|
| **OECD Model Tax Convention** (2017, with the 2025 Commentary update) | Art. 4(2)–(3) residence tie-breakers · Art. 5(1), 5(3), 5(4)/(4.1), 5(5)–(6) permanent establishment, incl. the 2025 home-office guidance · Arts. 10(2), 11(2), 12(1) withholding limits · Art. 13(4) land-rich shares · Art. 15(2) 183-day rule · Art. 29(9) principal purpose test | 11 |
| **WTO Dispute Settlement Understanding** | Arts. 4.3, 4.7, 4.8, 6.1, 8.7, 12.8, 12.9, 16.4, 17.5, 17.14, 20, 21.3, 21.5, 22.2, 22.6, 25. The calculator flags the Appellate Body's lack of quorum since 11 December 2019 | 1 timeline calculator |
| **Linked projects** | GATS Arts. I:3, II, XVI:2, XVII, XIV, XIV bis ([GATS Reasoning Engine](https://github.com/AlirezaMahdavishirkharkolaei/wto-gats-reasoning-engine)) · GloBE Arts. 5.2, 5.3 and the Transitional CbCR Safe Harbour ([TaxRiskScan](https://github.com/AlirezaMahdavishirkharkolaei/Tax_Risk_AI)) | in those repositories |

Current index: **38 provisions** (22 A · 13 B · 3 C), with **37 documented ambiguities**.

## Try it

**Browser:** `web/` holds a static app with the tax-treaty calculators, the DSU timeline and an index explorer. It runs this package with Pyodide, so nothing leaves your browser.

* Build it locally with `python scripts/build_web.py`.
* Once GitHub Pages is enabled it is published at `https://alirezamahdavishirkharkolaei.github.io/Legal-to-Code/`.

**Command line** (Python 3.10+, no dependencies):

```bash
pip install git+https://github.com/AlirezaMahdavishirkharkolaei/Legal-to-Code
l2c rules
l2c run oecd_mtc.withholding_rate '{"income": "dividends", "beneficial_owner": true, "recipient_is_company": true, "holding_share": 0.3, "holding_days": 400}'
l2c run oecd_mtc.construction_pe '{"start": "2025-03-01", "end": "2026-04-15", "treaty": {"construction_pe_months": 6}}'
l2c run wto_dsu.timeline '{"consultations_requested": "2026-01-15", "panel_established": "2026-04-20"}'
l2c index --format csv > codifiability_index.csv
```

Example output:

```
oecd_mtc.withholding_rate: Dividends: source tax limited to 5%.
  - (info) Treaty profile: OECD Model (2017).
  - (judgment) Judgment supplied by user: The recipient is the beneficial owner of the income -> True [OECD-MTC:10(2)]
  - (test) Company recipient: True; direct holding 30% (threshold 25%); held 400 days (required 365, ...) [OECD-MTC:10(2)]
  - (conclusion) Qualifying dividend: maximum source tax 5%. [OECD-MTC:10(2)]
```

**Python:**

```python
from legal_to_code.modules.oecd_mtc import rules
r = rules.employment_income(days_in_any_12_months=190, employer_resident_in_work_state=False, borne_by_pe_in_work_state=False)
print(r.outcome, r.summary)
print(r.explain())
```

Bilateral treaties depart from the OECD Model. Pass the real treaty's figures as a `treaty` profile; the defaults reproduce the Model.

## Why this matters

* **For research:** encoding is a close reading. The index shows where international economic law is determinate and where it deliberately leaves room for judgment. It also exposes drafting gaps, such as the absence of any rule on non-working days in the DSU, and time limits that are hortatory and routinely exceeded.
* **For practice:** tax advisers, treasury teams and trade lawyers get transparent calculators whose every step is cited.
* **For governments and international organisations:** a worked example of "Rules as Code", the approach studied by the OECD Observatory of Public Sector Innovation, applied to treaty law.
* **For teaching:** students see the structure of a legal test and the point where judgment takes over.

## How it works

* [`core.py`](legal_to_code/core.py): `Provision`, the rubric, the `@rule` decorator that links code to provisions, and `Trace`/`Result`.
* [`modules/`](legal_to_code/modules): one package per instrument (`provisions.py` + `rules.py`).
* [`index.py`](legal_to_code/index.py): the codifiability index.
* Tests check every rule against the text, boundary values and worked examples, plus the registry's internal links.

The method and the rules for adding a provision are in [docs/method.md](docs/method.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Roadmap

* **Planned modules:**
  * UN Model Tax Convention
  * a treaty-network data layer (actual bilateral rates)
  * FTA rules of origin
  * Vienna Convention on the Law of Treaties (entry into force, reservations)
  * GATT Art. XX structure
* **Planned outputs:**
  * An executable version of the index for side-by-side comparison of Model vs. treaty
  * A research paper on the codifiability of international economic law

## Disclaimer

Research and teaching aid. Not legal or tax advice.

## Collaboration

**Mohammad Amir Modami** collaborated on the legal analysis and research behind this project.

## Citation

See [CITATION.cff](CITATION.cff).
