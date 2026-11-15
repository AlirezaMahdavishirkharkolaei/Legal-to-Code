"""Provisions implemented in companion repositories, registered here so the codifiability index covers them."""

from ..core import REGISTRY, Codifiability as C, Provision

GATS_REPO = "https://github.com/AlirezaMahdavishirkharkolaei/wto-gats-reasoning-engine"
TRS_REPO = "https://github.com/AlirezaMahdavishirkharkolaei/Tax_Risk_AI"
GATS = "General Agreement on Trade in Services (1994)"
GLOBE = "OECD GloBE Model Rules (2021) and Administrative Guidance"


def G(pid, article, title, summary, cls, rationale, amb=()):
    return Provision(f"GATS:{pid}", GATS, article, title, summary, cls, rationale, tuple(amb),
                     "https://www.wto.org/english/docs_e/legal_e/26-gats_01_e.htm", "gats", (), "", GATS_REPO)


def O(pid, article, title, summary, cls, rationale, amb=()):
    return Provision(f"GloBE:{pid}", GLOBE, article, title, summary, cls, rationale, tuple(amb), "", "globe", (), "", TRS_REPO)


REGISTRY.add(
    G("I:3(b)", "Art. I:3(b)-(c)", "Services supplied in the exercise of governmental authority",
      "Excluded if supplied neither on a commercial basis nor in competition with one or more suppliers.",
      C.B, "'Commercial basis' and 'in competition' are evaluative."),
    G("II", "Art. II:1", "Most-favoured-nation treatment",
      "No less favourable treatment of services and suppliers of any Member than like ones of any other country.",
      C.B, "Likeness and less favourable treatment are evaluative.", ["De facto discrimination requires an effects analysis."]),
    G("XVI:2", "Art. XVI:2", "Market access: prohibited measure types",
      "Six exhaustively listed types of limitation in committed sectors, unless scheduled.",
      C.A, "A closed list of measure types; classification of a measure is mostly categorical.",
      ["Whether a total ban is a 'zero quota' was resolved by interpretation (US - Gambling), not by the text."]),
    G("XVII", "Art. XVII", "National treatment",
      "No less favourable treatment than domestic like services and suppliers in committed sectors.",
      C.B, "Likeness and modification of the conditions of competition are evaluative."),
    G("XIV", "Art. XIV(a)-(e)", "General exceptions: paragraphs and necessity",
      "Closed list of objectives; necessity as weighing and balancing with a reasonably available alternative.",
      C.B, "The structure is fixed; necessity is a weighing exercise.",
      ["'Public order' carries a qualifying footnote (fn. 5) absent from GATT Art. XX."]),
    G("XIV-chapeau", "Art. XIV chapeau", "Chapeau",
      "No arbitrary or unjustifiable discrimination where like conditions prevail; no disguised restriction.",
      C.B, "Two fixed limbs, each requiring an evaluative assessment of how the measure is applied."),
    G("XIVbis", "Art. XIV bis", "Security exceptions",
      "Measures the Member considers necessary for essential security interests in listed circumstances.",
      C.B, "Listed circumstances are reviewable; the necessity element is largely self-judging, subject to good faith."),
    O("5.2", "Art. 5.2", "Top-up tax percentage",
      "Minimum rate (15%) minus the jurisdictional effective tax rate.",
      C.A, "Arithmetic on determinate inputs.", ["Computing the GloBE ETR itself requires extensive adjustments to accounts."]),
    O("5.3", "Art. 5.3 and 9.2", "Substance-based income exclusion",
      "Percentage of eligible payroll costs and tangible assets, with transitional rates.",
      C.A, "Rates and bases are determinate.", ["Eligibility of costs and assets requires classification choices."]),
    O("TCSH", "Administrative Guidance (Dec. 2022)", "Transitional CbCR Safe Harbour",
      "De minimis, simplified ETR and routine profits tests on CbCR data.",
      C.A, "Fixed thresholds applied to reported figures.", ["Requires 'qualified' CbCR and financial statements."]),
)
