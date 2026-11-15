# Contributing a provision or module

1. **Choose the provision and the version of the text.** For example, the 2017 OECD Model with the 2025 Commentary.
2. **Register it** in `legal_to_code/modules/<module>/provisions.py`. Include:
   - id
   - article
   - title
   - a summary in your own words
   - codifiability class (A/B/C) and a one-sentence rationale, using [the rubric](docs/method.md)
   - the ambiguities you met
   - a status note for later amendments
3. **Encode it** in `rules.py` with `@rule("<module>.<name>", ["<provision id>"])`.
   - Every test, judgment and conclusion goes through the trace.
   - Never default an evaluative element; leave it as `None` so it is reported.
4. **Add the rule's name** to the provision's `implemented_by`.
5. **Write tests** in `tests/`. Cover:
   - boundary values
   - a worked example
   - a missing-judgment case
6. **Check:**
   - `pytest`
   - `l2c index`, then update `docs/codifiability-index.md` with `l2c index > docs/codifiability-index.md`
   - `python scripts/build_web.py`

Keep summaries paraphrased; quote treaty text only briefly. Cite sources in the provision's docstring or status note.
