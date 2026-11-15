"""Rules implementing the OECD Model provisions registered in ``provisions.py``.

Every rule receives a ``Trace`` as its first argument (added by the ``@rule``
decorator), records each test it applies, and returns (outcome, summary).
Evaluative elements are never guessed: callers pass the judgment (True/False),
or leave it as None and it is reported as a judgment still needed.
"""

from __future__ import annotations

import calendar
from dataclasses import asdict, dataclass
from datetime import date, timedelta

from ...core import rule

P = "OECD-MTC:"


@dataclass(frozen=True)
class TreatyProfile:
    """Treaty-specific figures. Defaults reproduce the OECD Model (2017)."""

    name: str = "OECD Model (2017)"
    dividends_qualifying_rate: float | None = 0.05
    dividends_other_rate: float | None = 0.15
    dividends_holding_threshold: float = 0.25
    dividends_holding_days: int = 365
    interest_rate: float | None = 0.10
    royalties_rate: float | None = 0.0   # 0.0 = taxable only in the residence State
    construction_pe_months: int = 12
    employment_days: int = 183

    @classmethod
    def from_dict(cls, d: dict | None) -> "TreatyProfile":
        if not d:
            return cls()
        known = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**known)

    def to_dict(self) -> dict:
        return asdict(self)


def _pct(x: float | None) -> str:
    return "domestic rate (no treaty limit)" if x is None else f"{x:.0%}"


def _add_months(d: date, months: int) -> date:
    m = d.month - 1 + months
    y = d.year + m // 12
    m = m % 12 + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


# ---------------------------------------------------------------- Art. 4

@rule("oecd_mtc.residence_tiebreaker_individual", [P + "4(2)"])
def residence_tiebreaker_individual(t, permanent_home: str, vital_interests: str | None = None,
                                    habitual_abode: str | None = None, nationality: str | None = None):
    """Each argument is 'A', 'B', 'both' or 'neither' (vital_interests: 'A', 'B' or 'undeterminable')."""
    a = P + "4(2)"
    t.test(f"(a) Permanent home available in: {permanent_home}", a)
    if permanent_home in ("A", "B"):
        t.conclude(f"Resident of State {permanent_home} (permanent home in one State only).", a)
        return permanent_home, f"Treaty resident of State {permanent_home} under Art. 4(2)(a), permanent home."
    if permanent_home == "both":
        if vital_interests is None:
            t.judgment("In which State are the individual's personal and economic relations closer (centre of vital interests)?", a)
            return None, "Undetermined: the centre of vital interests must be assessed."
        t.judgment("Centre of vital interests", a, vital_interests)
        if vital_interests in ("A", "B"):
            t.conclude(f"Resident of State {vital_interests} (centre of vital interests).", a)
            return vital_interests, f"Treaty resident of State {vital_interests} under Art. 4(2)(a), centre of vital interests."
        t.info("The centre of vital interests cannot be determined: go to habitual abode.", a)
    else:
        t.info("No permanent home in either State: go to habitual abode.", a)
    if habitual_abode is None:
        t.judgment("Where does the individual have an habitual abode (both, neither, A or B)?", a)
        return None, "Undetermined: habitual abode must be established."
    t.test(f"(b) Habitual abode in: {habitual_abode}", a)
    if habitual_abode in ("A", "B"):
        t.conclude(f"Resident of State {habitual_abode} (habitual abode).", a)
        return habitual_abode, f"Treaty resident of State {habitual_abode} under Art. 4(2)(b)."
    if nationality is None:
        t.judgment("Of which State(s) is the individual a national?", a)
        return None, "Undetermined: nationality must be established."
    t.test(f"(c) National of: {nationality}", a)
    if nationality in ("A", "B"):
        t.conclude(f"Resident of State {nationality} (nationality).", a)
        return nationality, f"Treaty resident of State {nationality} under Art. 4(2)(c)."
    t.conclude("No test resolves residence: the competent authorities settle the question by mutual agreement.", a)
    return "MAP", "Residence to be settled by mutual agreement under Art. 4(2)(d)."


@rule("oecd_mtc.residence_tiebreaker_entity", [P + "4(3)"])
def residence_tiebreaker_entity(t):
    t.info("Since 2017 the Model has no automatic tie-breaker for persons other than individuals.", P + "4(3)")
    t.judgment("Competent authorities' determination by mutual agreement (place of effective management, incorporation, other factors)", P + "4(3)")
    return "MAP", "Residence of a dual-resident entity is settled by mutual agreement; absent agreement, no treaty relief except as agreed."


# ---------------------------------------------------------------- Art. 5

@rule("oecd_mtc.construction_pe", [P + "5(3)"])
def construction_pe(t, start: date, end: date, treaty: dict | None = None):
    tp = TreatyProfile.from_dict(treaty)
    p = P + "5(3)"
    threshold = _add_months(start, tp.construction_pe_months)
    t.test(f"Site from {start.isoformat()} to {end.isoformat()}; threshold: more than {tp.construction_pe_months} months "
           f"(beyond {threshold.isoformat()}).", p)
    is_pe = end > threshold
    t.conclude("The site lasts more than the threshold: it constitutes a permanent establishment." if is_pe
               else "The site does not exceed the threshold: no permanent establishment under Art. 5(3).", p)
    t.warn("Check for contract-splitting between closely related enterprises (principal purpose test, Art. 29(9)).", P + "29(9)")
    return is_pe, ("PE: the construction site exceeds " if is_pe else "No PE: the construction site does not exceed ") + \
        f"{tp.construction_pe_months} months."


@rule("oecd_mtc.home_office_pe", [P + "5(1)"])
def home_office_pe(t, share_of_working_time: float, commercial_reason: bool | None = None):
    """share_of_working_time: highest share of total working time spent at the home/other relevant place in any 12-month period."""
    p = P + "5(1)"
    t.test(f"Share of working time at the home or other relevant place in any 12-month period: {share_of_working_time:.0%} "
           "(2025 Commentary threshold: 50%).", p)
    if share_of_working_time < 0.5:
        t.conclude("Below 50%: the place will generally not be a place of business of the enterprise.", p)
        return False, "Generally no PE: work from that place is below 50% of working time."
    if commercial_reason is None:
        t.judgment("Is there a commercial reason for the activity being carried on in that State (e.g. meeting customers there)?", p)
        return None, "Possible PE: at or above 50% of working time; depends on whether there is a commercial reason."
    t.judgment("Commercial reason for the activity in that State", p, commercial_reason)
    if commercial_reason:
        t.conclude("At or above 50% with a commercial reason: the place may be a fixed place of business; apply the other "
                   "Art. 5 conditions (including preparatory or auxiliary).", p)
        return True, "PE likely: at or above 50% of working time and a commercial reason (subject to Art. 5(4))."
    t.conclude("At or above 50% but no commercial reason (e.g. personal choice or retention): generally not a place of business.", p)
    return False, "Generally no PE: no commercial reason for the work being done in that State."


@rule("oecd_mtc.fixed_place_pe", [P + "5(1)", P + "5(4)"])
def fixed_place_pe(t, place_at_disposal: bool | None = None, fixed: bool | None = None,
                   business_carried_on_through_it: bool | None = None, preparatory_or_auxiliary: bool | None = None,
                   cohesive_operation_with_related: bool | None = None):
    elements = [("A place of business at the disposal of the enterprise", place_at_disposal, P + "5(1)"),
                ("A sufficient degree of permanence ('fixed')", fixed, P + "5(1)"),
                ("Business wholly or partly carried on through it", business_carried_on_through_it, P + "5(1)")]
    for text, v, ref in elements:
        t.judgment(text, ref, v)
        if v is False:
            t.conclude(f"Not satisfied: {text.lower()}.", ref)
            return False, f"No PE under Art. 5(1): {text.lower()} is lacking."
    if any(v is None for _, v, _ in elements):
        return None, "Undetermined: the Art. 5(1) elements need assessment."
    t.judgment("Activities are only preparatory or auxiliary (Art. 5(4))", P + "5(4)", preparatory_or_auxiliary)
    if preparatory_or_auxiliary is None:
        return None, "Art. 5(1) satisfied; whether the Art. 5(4) exception applies needs assessment."
    if preparatory_or_auxiliary:
        t.judgment("Complementary functions with closely related enterprises form a cohesive business operation (Art. 5(4.1))",
                   P + "5(4)", cohesive_operation_with_related)
        if cohesive_operation_with_related:
            t.conclude("Anti-fragmentation rule: the exception does not apply.", P + "5(4)")
            return True, "PE: Art. 5(4) exception excluded by the anti-fragmentation rule."
        if cohesive_operation_with_related is None:
            return None, "Preparatory or auxiliary, but the anti-fragmentation rule needs assessment."
        t.conclude("Preparatory or auxiliary activities: no PE.", P + "5(4)")
        return False, "No PE: activities are preparatory or auxiliary."
    t.conclude("Fixed place of business PE.", P + "5(1)")
    return True, "PE under Art. 5(1)."


@rule("oecd_mtc.dependent_agent_pe", [P + "5(5)-(6)"])
def dependent_agent_pe(t, acts_on_behalf: bool | None = None, habitually_concludes_or_principal_role: bool | None = None,
                       independent_agent_ordinary_course: bool | None = None,
                       works_exclusively_for_related: bool | None = None):
    p = P + "5(5)-(6)"
    for text, v in [("Acts on behalf of the enterprise", acts_on_behalf),
                    ("Habitually concludes contracts or plays the principal role leading to their routine conclusion",
                     habitually_concludes_or_principal_role)]:
        t.judgment(text, p, v)
        if v is False:
            return False, f"No dependent agent PE: not satisfied - {text.lower()}."
    if acts_on_behalf is None or habitually_concludes_or_principal_role is None:
        return None, "Undetermined: the Art. 5(5) conditions need assessment."
    if works_exclusively_for_related:
        t.conclude("Acting exclusively or almost exclusively for closely related enterprises: not an independent agent.", p)
        return True, "Dependent agent PE (the independent-agent exception is unavailable)."
    t.judgment("Independent agent acting in the ordinary course of business (Art. 5(6))", p, independent_agent_ordinary_course)
    if independent_agent_ordinary_course is None:
        return None, "Art. 5(5) satisfied; the independent-agent exception needs assessment."
    if independent_agent_ordinary_course:
        return False, "No PE: independent agent acting in the ordinary course of business."
    t.conclude("Dependent agent PE.", p)
    return True, "Dependent agent PE under Art. 5(5)."


# ---------------------------------------------------------------- Arts. 10-12

@rule("oecd_mtc.withholding_rate", [P + "10(2)", P + "11(2)", P + "12(1)"])
def withholding_rate(t, income: str, beneficial_owner: bool | None = None, recipient_is_company: bool = False,
                     holding_share: float = 0.0, holding_days: int = 0, treaty: dict | None = None):
    """Maximum source-State tax rate for 'dividends', 'interest' or 'royalties'."""
    tp = TreatyProfile.from_dict(treaty)
    t.info(f"Treaty profile: {tp.name}.")
    ref = {"dividends": P + "10(2)", "interest": P + "11(2)", "royalties": P + "12(1)"}.get(income)
    if ref is None:
        raise ValueError("income must be 'dividends', 'interest' or 'royalties'")
    t.judgment("The recipient is the beneficial owner of the income", ref, beneficial_owner)
    if beneficial_owner is False:
        t.conclude("Not the beneficial owner: the treaty limit does not apply (look through to the beneficial owner).", ref)
        return None, "No treaty limit: the recipient is not the beneficial owner."
    caveat = " (assuming beneficial ownership)" if beneficial_owner is None else ""
    if income == "dividends":
        qualifies = recipient_is_company and holding_share >= tp.dividends_holding_threshold and \
            holding_days >= tp.dividends_holding_days
        t.test(f"Company recipient: {recipient_is_company}; direct holding {holding_share:.0%} "
               f"(threshold {tp.dividends_holding_threshold:.0%}); held {holding_days} days "
               f"(required {tp.dividends_holding_days}, period including the payment date).", ref)
        rate = tp.dividends_qualifying_rate if qualifies else tp.dividends_other_rate
        t.conclude(f"{'Qualifying' if qualifies else 'Portfolio/other'} dividend: maximum source tax {_pct(rate)}.", ref)
        return rate, f"Dividends: source tax limited to {_pct(rate)}{caveat}."
    if income == "interest":
        t.conclude(f"Interest: maximum source tax {_pct(tp.interest_rate)}.", ref)
        return tp.interest_rate, f"Interest: source tax limited to {_pct(tp.interest_rate)}{caveat}."
    if tp.royalties_rate == 0.0:
        t.conclude("Royalties: taxable only in the State of residence of the beneficial owner.", ref)
        return 0.0, f"Royalties: no source tax (residence taxation only){caveat}."
    t.conclude(f"Royalties: maximum source tax {_pct(tp.royalties_rate)} under this treaty (departs from the Model).", ref)
    return tp.royalties_rate, f"Royalties: source tax limited to {_pct(tp.royalties_rate)}{caveat}."


# ---------------------------------------------------------------- Art. 13(4)

@rule("oecd_mtc.land_rich_gains", [P + "13(4)"])
def land_rich_gains(t, max_immovable_share_365d: float):
    p = P + "13(4)"
    t.test(f"Highest share of value derived from immovable property in the 365 days before alienation: "
           f"{max_immovable_share_365d:.0%} (threshold: more than 50%).", p)
    taxable = max_immovable_share_365d > 0.5
    t.conclude("The State where the property is situated may tax the gain." if taxable
               else "Art. 13(4) does not apply; see Art. 13(5) (residence taxation).", p)
    return taxable, ("Source taxation allowed" if taxable else "No source taxation under Art. 13(4)") + \
        f" ({max_immovable_share_365d:.0%} immovable-property value)."


# ---------------------------------------------------------------- Art. 15

@rule("oecd_mtc.max_days_any_12_months", [P + "15(2)"])
def max_days_any_12_months(t, presence_days: list, fiscal_year_start: date, fiscal_year_end: date):
    """Highest number of presence days in any 12-month period commencing or ending in the fiscal year."""
    p = P + "15(2)"
    days = sorted({d if isinstance(d, date) else date.fromisoformat(str(d)) for d in presence_days})
    t.info("Counting convention: each calendar day with any physical presence counts (part-days included).", p)
    best, best_window = 0, None
    starts = set()
    d = fiscal_year_start
    while d <= fiscal_year_end:
        starts.add(d)  # windows commencing in the fiscal year
        starts.add(_add_months(d + timedelta(days=1), -12))  # windows ending on d
        d += timedelta(days=1)
    for s in starts:
        e = _add_months(s, 12) - timedelta(days=1)
        n = sum(1 for x in days if s <= x <= e)
        if n > best:
            best, best_window = n, (s, e)
    if best_window:
        t.conclude(f"Maximum {best} days, in the window {best_window[0].isoformat()} to {best_window[1].isoformat()}.", p)
    return best, f"{best} days of presence in the worst twelve-month window."


@rule("oecd_mtc.employment_income", [P + "15(2)"])
def employment_income(t, days_in_any_12_months: int, employer_resident_in_work_state: bool,
                      borne_by_pe_in_work_state: bool, treaty: dict | None = None):
    tp = TreatyProfile.from_dict(treaty)
    p = P + "15(2)"
    a = days_in_any_12_months <= tp.employment_days
    t.test(f"(a) Presence {days_in_any_12_months} days; limit {tp.employment_days} days in any twelve-month period: "
           f"{'met' if a else 'not met'}.", p)
    b = not employer_resident_in_work_state
    t.test(f"(b) Paid by or on behalf of an employer not resident in the work State: {'met' if b else 'not met'}.", p)
    c = not borne_by_pe_in_work_state
    t.test(f"(c) Not borne by a PE of the employer in the work State: {'met' if c else 'not met'}.", p)
    if a and b and c:
        t.conclude("All three conditions met: taxable only in the State of residence.", p)
        return "residence_only", "Taxable only in the residence State (Art. 15(2) exemption applies)."
    t.conclude("At least one condition fails: the State where the work is exercised may tax.", p)
    return "work_state_may_tax", "The work State may tax the remuneration (Art. 15(1)); the residence State gives relief (Art. 23)."


# ---------------------------------------------------------------- Art. 29(9)

@rule("oecd_mtc.principal_purpose_test", [P + "29(9)"])
def principal_purpose_test(t, principal_purpose: bool | None = None, consistent_with_object_and_purpose: bool | None = None):
    p = P + "29(9)"
    t.info("Codifiability class C: the engine documents the two-limb test; it cannot apply it.", p)
    t.judgment("Is it reasonable to conclude that obtaining the benefit was one of the principal purposes?", p, principal_purpose)
    if principal_purpose is None:
        return None, "Undetermined: the principal-purpose limb requires a judgment on all relevant facts."
    if principal_purpose is False:
        return "benefit_granted", "Benefit not denied by the PPT: obtaining it was not a principal purpose."
    t.judgment("Would granting the benefit accord with the object and purpose of the relevant provisions?", p,
               consistent_with_object_and_purpose)
    if consistent_with_object_and_purpose is None:
        return None, "Principal purpose established; the object-and-purpose exception requires a judgment."
    if consistent_with_object_and_purpose:
        return "benefit_granted", "Benefit granted: in accordance with the object and purpose of the provisions."
    return "benefit_denied", "Benefit denied under the principal purpose test."
