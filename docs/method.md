# Method

## 1. Unit of analysis

The unit of analysis is a **provision**: an article, paragraph or sub-paragraph that states one legal test. Each provision gets a stable identifier, `INSTRUMENT:article`, for example `OECD-MTC:10(2)` or `WTO-DSU:16.4`.

## 2. The codifiability rubric

| Class | Test | What the code does |
|---|---|---|
| **A – Computable** | Every condition is a determinate fact (date, amount, count, category) and the consequence follows mechanically | Applies the rule end to end |
| **B – Structurable** | The structure of the test is fixed, but at least one element is an open-textured standard | Sequences the test, records the judgment as an input, and stops if it is missing |
| **C – Not codifiable** | The outcome turns on purposive interpretation or open balancing, with no stable decision structure | Documents the test and its elements |

Classification rules:

1. Classify the provision as drafted, not as applied in practice. Where they diverge (for example hortatory DSU time limits), record the divergence as an ambiguity.
2. If a single open element exists, the class is at least B, even if everything else is numeric. *Exception:* an open element confined to classifying the input (e.g. "is this payment a royalty?") keeps the class at A. The classification question is recorded as an ambiguity, and the code takes the answer as input.
3. Every classification carries a one-sentence **rationale**.

## 3. Encoding workflow

For each provision:

1. **Read** the provision, its Commentary or travaux, and the leading interpretations.
2. **Register** it: summary, class, rationale, and the source and version of the text (e.g. 2017 Model with 2025 Commentary).
3. **Encode** the rule as a function decorated with `@rule(name, [provision ids])`:
   * Record each test with `t.test`, each conclusion with `t.conclude`, and each risk with `t.warn`.
   * Route every evaluative element through `t.judgment`. With no answer supplied, it becomes an open judgment and the rule returns an undetermined outcome.
4. **Record the ambiguities** met while encoding: undefined terms, counting conventions, conflicts between versions, and gaps.
5. **Test:**
   * boundary values (e.g. exactly 12 months, exactly 25%, 364 vs. 365 days)
   * worked examples from the Commentary or case law
   * a test that the trace cites the provision

## 4. What counts as an ambiguity

* An undefined term the rule depends on (e.g. "beneficial owner").
* A counting or measurement convention the text does not fix (days of presence, non-working days, valuation method).
* A divergence between versions of the text (pre-2017 vs. 2017 Model; MLI options).
* A divergence between text and practice (hortatory time limits; the Appellate Body's lack of quorum).
* A gap: a situation the text does not address.

## 5. Traceability

A `Result` contains:

* the outcome
* a summary
* the ordered trace of steps, each with a provision id
* the list of judgments still needed

No conclusion is produced without a trace.

## 6. Linked implementations

Provisions implemented in other repositories are registered with an `external` link. This way the index covers the whole body of work: the GATS Reasoning Engine and TaxRiskScan.
