"""Core of the Legal-to-Code framework.

Three ideas:

* A **Provision** records a legal rule: where it comes from, a summary, how
  far it can be expressed as code (its codifiability class), and the
  ambiguities found while encoding it.
* A **rule** is a Python function linked to the provisions it implements.
  Calling it returns a **Result** carrying the outcome and a **trace**, so
  every conclusion can be followed back to the text.
* The **registry** collects every provision of every module, which gives the
  codifiability index (see ``index.py``).
"""

from __future__ import annotations

import functools
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable


class Codifiability(str, Enum):
    """Rubric used to classify every provision."""

    A = "A"  # computable
    B = "B"  # structurable
    C = "C"  # not codifiable

    @property
    def label(self) -> str:
        return RUBRIC[self.value]["label"]


RUBRIC = {
    "A": {
        "label": "Computable",
        "test": "Every condition is a determinate fact (date, amount, count, category) and the legal consequence "
                "follows mechanically. Code can apply the rule end to end.",
    },
    "B": {
        "label": "Structurable",
        "test": "The structure of the test is fixed, but at least one element is an open-textured standard that "
                "needs evaluative judgment (e.g. 'centre of vital interests', 'preparatory or auxiliary', 'like'). "
                "Code can sequence the test and record the judgment, not make it.",
    },
    "C": {
        "label": "Not codifiable",
        "test": "The outcome turns on purposive interpretation or open balancing with no stable decision structure "
                "(e.g. 'one of the principal purposes', 'object and purpose'). Code can document, not decide.",
    },
}


@dataclass(frozen=True)
class Provision:
    id: str                      # e.g. "OECD-MTC-2017:10(2)"
    instrument: str              # e.g. "OECD Model Tax Convention (2017)"
    article: str                 # e.g. "Art. 10(2)"
    title: str
    summary: str
    codifiability: Codifiability
    rationale: str               # why this class
    ambiguities: tuple[str, ...] = ()
    source_url: str = ""
    module: str = ""
    implemented_by: tuple[str, ...] = ()
    status_note: str = ""        # e.g. later amendments to be aware of
    external: str = ""           # implementation in another repository (URL)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["codifiability"] = self.codifiability.value
        d["codifiability_label"] = self.codifiability.label
        return d


@dataclass
class Step:
    text: str
    provision: str = ""
    kind: str = "info"  # info | test | conclusion | judgment | warning

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Result:
    rule: str
    outcome: Any
    summary: str
    trace: list[Step] = field(default_factory=list)
    provisions: list[str] = field(default_factory=list)
    judgments_needed: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "rule": self.rule,
            "outcome": self.outcome,
            "summary": self.summary,
            "trace": [s.to_dict() for s in self.trace],
            "provisions": self.provisions,
            "judgments_needed": self.judgments_needed,
        }

    def explain(self) -> str:
        lines = [f"{self.rule}: {self.summary}"]
        for s in self.trace:
            ref = f" [{s.provision}]" if s.provision else ""
            lines.append(f"  - ({s.kind}) {s.text}{ref}")
        for j in self.judgments_needed:
            lines.append(f"  ! judgment needed: {j}")
        return "\n".join(lines)


class Trace:
    """Collects steps while a rule runs."""

    def __init__(self) -> None:
        self.steps: list[Step] = []
        self.judgments: list[str] = []

    def info(self, text: str, provision: str = "") -> None:
        self.steps.append(Step(text, provision, "info"))

    def test(self, text: str, provision: str = "") -> None:
        self.steps.append(Step(text, provision, "test"))

    def conclude(self, text: str, provision: str = "") -> None:
        self.steps.append(Step(text, provision, "conclusion"))

    def warn(self, text: str, provision: str = "") -> None:
        self.steps.append(Step(text, provision, "warning"))

    def judgment(self, question: str, provision: str = "", answer: Any = None) -> None:
        """Record an evaluative element. If no answer is supplied it becomes an open judgment."""
        if answer is None:
            self.judgments.append(question)
            self.steps.append(Step(f"Judgment required: {question}", provision, "judgment"))
        else:
            self.steps.append(Step(f"Judgment supplied by user: {question} -> {answer}", provision, "judgment"))


class Registry:
    def __init__(self) -> None:
        self.provisions: dict[str, Provision] = {}
        self.rules: dict[str, Callable] = {}

    def add(self, *provisions: Provision) -> None:
        for p in provisions:
            if p.id in self.provisions:
                raise ValueError(f"duplicate provision id {p.id}")
            self.provisions[p.id] = p

    def rule(self, name: str, provisions: list[str]):
        """Decorator: register a rule and link it to the provisions it implements."""

        def deco(fn: Callable[..., tuple[Any, str]]):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs) -> Result:
                t = Trace()
                outcome, summary = fn(t, *args, **kwargs)
                return Result(name, outcome, summary, t.steps, list(provisions), t.judgments)

            wrapper.rule_name = name
            wrapper.provision_ids = list(provisions)
            self.rules[name] = wrapper
            return wrapper

        return deco

    def check_links(self) -> list[str]:
        """Rules must point at registered provisions, and implemented_by must name real rules."""
        problems = []
        for name, fn in self.rules.items():
            for pid in fn.provision_ids:
                if pid not in self.provisions:
                    problems.append(f"rule {name} cites unknown provision {pid}")
        for p in self.provisions.values():
            for r in p.implemented_by:
                if r not in self.rules:
                    problems.append(f"provision {p.id} names unknown rule {r}")
        return problems


REGISTRY = Registry()
rule = REGISTRY.rule
