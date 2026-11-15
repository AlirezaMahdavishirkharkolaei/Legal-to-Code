"""DSU timeline calculator.

Give the dates of the events that have happened; the rule returns every time limit that follows from them, with
its basis in the DSU. Periods are counted in calendar days from the event date (the DSU does not say how to treat
non-working days; WTO practice moves a deadline falling on a non-working day to the next working day, which is
flagged rather than applied).
"""

from __future__ import annotations

import calendar
from datetime import date, timedelta

from ...core import rule

P = "WTO-DSU:"
AB_PARALYSED_SINCE = date(2019, 12, 11)


def _d(x) -> date | None:
    if x is None or x == "":
        return None
    return x if isinstance(x, date) else date.fromisoformat(str(x))


def _months(d: date, n: int) -> date:
    m = d.month - 1 + n
    y = d.year + m // 12
    m = m % 12 + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


@rule("wto_dsu.timeline", [P + p for p in ("4.3", "4.7", "4.8", "6.1", "8.7", "12.8", "12.9", "16.4", "17.5",
                                          "17.14", "20", "21.3", "21.5", "22.2", "22.6")])
def timeline(t, consultations_requested, urgent: bool = False, panel_established=None, panel_composed=None,
             panel_report_circulated=None, appeal_notified=None, ab_report_circulated=None, reports_adopted=None,
             rpt_expires=None, compliance_referral=None, as_of=None):
    """Return a list of milestones: {label, date, basis, kind, status}."""
    req = _d(consultations_requested)
    est, comp, circ = _d(panel_established), _d(panel_composed), _d(panel_report_circulated)
    appeal, abc, adopt = _d(appeal_notified), _d(ab_report_circulated), _d(reports_adopted)
    rpt, ref21_5 = _d(rpt_expires), _d(compliance_referral)
    today = _d(as_of) or date.today()
    m: list[dict] = []

    def add(label, when, pid, kind="deadline", note=""):
        if when is None:
            return
        status = "passed" if when < today else ("today" if when == today else "upcoming")
        m.append({"label": label, "date": when.isoformat(), "basis": P + pid, "kind": kind, "status": status, "note": note})
        t.test(f"{label}: {when.isoformat()} ({status})", P + pid)

    if urgent:
        add("Consultations to begin (urgent case)", req + timedelta(days=10), "4.8")
        add("Panel may be requested if consultations fail (urgent case)", req + timedelta(days=20), "4.8", "earliest")
    else:
        add("Reply to the request for consultations", req + timedelta(days=10), "4.3")
        add("Consultations to begin", req + timedelta(days=30), "4.3",
            note="If missed, the complainant may request a panel directly.")
        add("Panel may be requested if consultations fail", req + timedelta(days=60), "4.7", "earliest",
            note="Earlier if both parties consider that consultations have failed.")
    if est:
        add("Either party may ask the Director-General to compose the panel", est + timedelta(days=20), "8.7", "earliest")
        add("Panel report should be circulated (outer limit)", _months(est, 9), "12.9")
        add("DSB consideration of the report, no appeal (guideline)", _months(est, 9), "20", "guideline")
        add("DSB consideration of the report, with appeal (guideline)", _months(est, 12), "20", "guideline")
    if comp:
        add("Final report to the parties (guideline)", _months(comp, 3 if urgent else 6), "12.8", "guideline")
    if circ:
        add("Earliest DSB consideration for adoption", circ + timedelta(days=20), "16.4", "earliest")
        add("Adoption unless appealed (end of window)", circ + timedelta(days=60), "16.4")
        if circ >= AB_PARALYSED_SINCE and not appeal:
            t.warn("The Appellate Body has had no quorum since 11 December 2019: an appeal would leave the report "
                   "unadopted unless the parties use MPIA or other Art. 25 arbitration.", P + "16.4")
    if appeal:
        add("Appellate report (generally)", appeal + timedelta(days=60), "17.5", "guideline")
        add("Appellate report (in no case later than)", appeal + timedelta(days=90), "17.5")
        if appeal >= AB_PARALYSED_SINCE:
            t.warn("Appeal notified while the Appellate Body has no quorum: these limits cannot run in practice "
                   "(appeal 'into the void').", P + "17.5")
    if abc:
        add("Adoption of the Appellate Body report", abc + timedelta(days=30), "17.14")
    if adopt:
        add("Member states its implementation intentions", adopt + timedelta(days=30), "21.3")
        add("Art. 21.3(c) arbitration award due (if requested)", adopt + timedelta(days=90), "21.3")
        add("Reasonable period: 15-month guideline for the arbitrator", _months(adopt, 15), "21.3", "guideline")
    if rpt:
        add("Compensation talks: suspension may be requested if none agreed", rpt + timedelta(days=20), "22.2", "earliest")
        add("DSB authorization of suspension (absent consensus against)", rpt + timedelta(days=30), "22.6")
        add("Art. 22.6 arbitration to be completed (if level contested)", rpt + timedelta(days=60), "22.6")
    if ref21_5:
        add("Art. 21.5 compliance panel report", ref21_5 + timedelta(days=90), "21.5", "guideline")

    t.info("Calendar days; a deadline on a non-working day usually moves to the next working day in practice (not applied).")
    m.sort(key=lambda x: x["date"])
    nxt = next((x for x in m if x["status"] in ("upcoming", "today")), None)
    summary = (f"Next: {nxt['label']} on {nxt['date']} ({nxt['basis']})." if nxt
               else f"All {len(m)} computed time limits have passed as of {today.isoformat()}.")
    return m, summary
