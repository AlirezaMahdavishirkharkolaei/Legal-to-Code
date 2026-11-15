"""DSU provisions with time limits."""

from ...core import REGISTRY, Codifiability as C, Provision

DSU = "WTO Dispute Settlement Understanding (1994)"
URL = "https://www.wto.org/english/tratop_e/dispu_e/dsu_e.htm"
HORTATORY = "The time limit is phrased as 'shall generally' or 'should', and practice regularly exceeds it."


def P(pid, title, summary, cls, rationale, ambiguities=(), status_note=""):
    return Provision(f"WTO-DSU:{pid}", DSU, f"Art. {pid}", title, summary, cls, rationale, tuple(ambiguities), URL,
                     "wto_dsu", ("wto_dsu.timeline",), status_note)


REGISTRY.add(
    P("4.3", "Reply to and entry into consultations",
      "The responding Member replies within 10 days of receiving a request for consultations and enters into consultations "
      "within 30 days; otherwise the complainant may proceed directly to request a panel.",
      C.A, "Fixed day counts from a dated event."),
    P("4.7", "Request for a panel after consultations",
      "If consultations fail to settle the dispute within 60 days after receipt of the request, the complainant may "
      "request a panel (earlier if both parties consider that consultations have failed).",
      C.A, "Fixed day count; the early-request exception depends on a joint position recorded as an input."),
    P("4.8", "Urgent cases",
      "In cases of urgency, including perishable goods, consultations start within 10 days and a panel may be requested "
      "if they fail within 20 days.",
      C.B, "The time limits are fixed but whether a case is 'urgent' is evaluative.",
      ["'Cases of urgency' is not defined beyond the perishable-goods example."]),
    P("6.1", "Establishment of a panel",
      "A panel is established at the latest at the DSB meeting following the one at which the request first appears as "
      "an item, unless the DSB decides by consensus not to.",
      C.A, "Negative consensus makes establishment automatic at the second meeting.",
      ["The date depends on the DSB meeting calendar, which the code takes as input."]),
    P("8.7", "Composition of the panel by the Director-General",
      "If panelists are not agreed within 20 days after establishment, either party may ask the Director-General, who "
      "appoints them within 10 days of the request being transmitted to the DSB Chair.",
      C.A, "Fixed day counts."),
    P("12.8", "Duration of panel proceedings",
      "From composition and terms of reference to the final report to the parties: generally no more than 6 months "
      "(3 months in urgent cases).",
      C.A, "Fixed period; the legal consequence of exceeding it is only an obligation to inform the DSB (Art. 12.9).",
      [HORTATORY]),
    P("12.9", "Maximum period for panel reports",
      "If the panel cannot report within 6 months it informs the DSB; the period from establishment to circulation "
      "should in no case exceed 9 months.",
      C.A, "Fixed period, hortatory in effect.", [HORTATORY]),
    P("16.4", "Adoption of panel reports",
      "Within 60 days after circulation the report is adopted at a DSB meeting unless a party notifies an appeal or the DSB "
      "decides by consensus not to adopt; it is not considered for adoption until 20 days after circulation (Art. 16.1).",
      C.A, "Fixed window; adoption by negative consensus.",
      ["Since 11 December 2019 the Appellate Body has had no quorum. An appeal 'into the void' prevents adoption "
       "indefinitely, so the code can compute the Art. 16.4 window but not predict adoption."],
      "Appellate Body not operational since 11 December 2019; some Members use the Multi-Party Interim Appeal "
      "Arbitration Arrangement (MPIA) under Art. 25."),
    P("17.5", "Duration of appellate proceedings",
      "Generally no more than 60 days from notice of appeal to circulation, and in no case more than 90 days.",
      C.A, "Fixed period.", [HORTATORY, "Inapplicable in practice while the Appellate Body has no quorum."]),
    P("17.14", "Adoption of Appellate Body reports",
      "Adopted by the DSB and unconditionally accepted by the parties unless the DSB decides by consensus not to, within "
      "30 days following circulation.",
      C.A, "Fixed period, negative consensus."),
    P("20", "Overall time frame",
      "From establishment of the panel to DSB consideration of the report: generally no more than 9 months without appeal, "
      "12 months with appeal.",
      C.A, "Fixed periods.", [HORTATORY]),
    P("21.3", "Reasonable period of time for implementation",
      "The Member concerned states its intentions within 30 days after adoption. If immediate compliance is impracticable "
      "it has a reasonable period of time, which arbitration under Art. 21.3(c) (within 90 days of adoption) determines "
      "with a guideline of no more than 15 months.",
      C.B, "The procedural steps are fixed, but the length of the reasonable period is an evaluative determination.",
      ["The 15-month figure is a 'guideline' that may be shorter or longer 'depending upon the particular circumstances'."]),
    P("21.5", "Compliance proceedings",
      "Disagreement on compliance is decided by recourse to the dispute settlement procedures, wherever possible by the "
      "original panel, which circulates its report within 90 days of referral.",
      C.A, "Fixed period.",
      [HORTATORY, "The sequencing of Arts. 21.5 and 22 is not settled in the text; parties agree sequencing arrangements."]),
    P("22.2", "Compensation and suspension of concessions",
      "If the Member fails to comply within the reasonable period, it negotiates compensation on request; if none is "
      "agreed within 20 days after the expiry of that period, the complainant may request authorization to suspend "
      "concessions.",
      C.A, "Fixed day count from the end of the reasonable period."),
    P("22.6", "Authorization to suspend and Art. 22.6 arbitration",
      "The DSB grants authorization within 30 days of the expiry of the reasonable period unless it decides by consensus "
      "to reject; an objection to the level goes to arbitration, completed within 60 days after expiry of the period.",
      C.B, "The time limits are fixed; the level of suspension (equivalence with nullification) is an economic assessment.",
      ["The 30-day and 60-day limits run from the same date, which practice has had to reconcile."]),
    P("25", "Arbitration as an alternative means",
      "Parties may agree to arbitration as an alternative means of dispute settlement; awards are notified to the DSB.",
      C.C, "Procedure and timing depend entirely on the parties' agreement (e.g. the MPIA).", (),
      "Basis of the MPIA used by a group of Members while the Appellate Body is not operational."),
)
