from datetime import date, timedelta

import pytest

import legal_to_code as l2c
from legal_to_code import index
from legal_to_code.cli import main
from legal_to_code.core import Codifiability
from legal_to_code.modules.oecd_mtc import rules as mtc
from legal_to_code.modules.wto_dsu.rules import timeline


# --- framework -----------------------------------------------------------------------

def test_registry_links_are_consistent():
    assert l2c.REGISTRY.check_links() == []


def test_every_provision_is_classified_and_justified():
    for p in l2c.REGISTRY.provisions.values():
        assert isinstance(p.codifiability, Codifiability) and p.rationale and p.summary
        assert p.implemented_by or p.external, f"{p.id} has no implementation"


def test_every_rule_returns_a_traced_result():
    r = mtc.land_rich_gains(0.6)
    assert r.outcome is True and r.trace and r.trace[-1].kind == "conclusion"
    assert r.provisions == ["OECD-MTC:13(4)"]


def test_index_outputs():
    s = index.stats()
    assert s["provisions"] == len(l2c.REGISTRY.provisions) >= 35
    assert sum(s["by_class"].values()) == s["provisions"] and s["ambiguities"] > 25
    assert index.to_csv().splitlines()[0].startswith("id,instrument")
    assert "Codifiability index" in index.to_markdown()


# --- OECD Model: Art. 4 ------------------------------------------------------------------

@pytest.mark.parametrize("kwargs, expected", [
    ({"permanent_home": "A"}, "A"),
    ({"permanent_home": "both", "vital_interests": "B"}, "B"),
    ({"permanent_home": "both", "vital_interests": "undeterminable", "habitual_abode": "A"}, "A"),
    ({"permanent_home": "neither", "habitual_abode": "B"}, "B"),
    ({"permanent_home": "neither", "habitual_abode": "both", "nationality": "A"}, "A"),
    ({"permanent_home": "neither", "habitual_abode": "neither", "nationality": "both"}, "MAP"),
])
def test_tiebreaker_cascade(kwargs, expected):
    assert mtc.residence_tiebreaker_individual(**kwargs).outcome == expected


def test_tiebreaker_reports_open_judgment():
    r = mtc.residence_tiebreaker_individual("both")
    assert r.outcome is None and r.judgments_needed


# --- Art. 5 ---------------------------------------------------------------------------------

def test_construction_pe_is_strictly_more_than_twelve_months():
    assert mtc.construction_pe(date(2025, 3, 1), date(2026, 3, 1)).outcome is False
    assert mtc.construction_pe(date(2025, 3, 1), date(2026, 3, 2)).outcome is True
    assert mtc.construction_pe(date(2025, 3, 1), date(2025, 10, 1), treaty={"construction_pe_months": 6}).outcome is True


def test_home_office_2025_commentary():
    assert mtc.home_office_pe(0.4).outcome is False
    assert mtc.home_office_pe(0.6).outcome is None
    assert mtc.home_office_pe(0.6, commercial_reason=True).outcome is True
    assert mtc.home_office_pe(0.6, commercial_reason=False).outcome is False


def test_fixed_place_and_anti_fragmentation():
    base = dict(place_at_disposal=True, fixed=True, business_carried_on_through_it=True)
    assert mtc.fixed_place_pe(**base, preparatory_or_auxiliary=False).outcome is True
    assert mtc.fixed_place_pe(**base, preparatory_or_auxiliary=True, cohesive_operation_with_related=False).outcome is False
    assert mtc.fixed_place_pe(**base, preparatory_or_auxiliary=True, cohesive_operation_with_related=True).outcome is True
    assert mtc.fixed_place_pe(place_at_disposal=False).outcome is False


def test_dependent_agent():
    assert mtc.dependent_agent_pe(True, True, works_exclusively_for_related=True).outcome is True
    assert mtc.dependent_agent_pe(True, True, independent_agent_ordinary_course=True).outcome is False


# --- Arts. 10-12 ---------------------------------------------------------------------------------

def test_dividend_rates():
    q = dict(recipient_is_company=True, holding_share=0.25, holding_days=365, beneficial_owner=True)
    assert mtc.withholding_rate("dividends", **q).outcome == 0.05
    assert mtc.withholding_rate("dividends", **{**q, "holding_days": 364}).outcome == 0.15
    assert mtc.withholding_rate("dividends", **{**q, "holding_share": 0.24}).outcome == 0.15
    assert mtc.withholding_rate("dividends", **{**q, "recipient_is_company": False}).outcome == 0.15


def test_interest_royalties_and_treaty_profile():
    assert mtc.withholding_rate("interest").outcome == 0.10
    assert mtc.withholding_rate("royalties").outcome == 0.0
    assert mtc.withholding_rate("royalties", treaty={"royalties_rate": 0.05}).outcome == 0.05
    assert mtc.withholding_rate("interest", beneficial_owner=False).outcome is None
    with pytest.raises(ValueError):
        mtc.withholding_rate("fees")


# --- Arts. 13(4), 15, 29 -------------------------------------------------------------------------

def test_land_rich_threshold_is_more_than_half():
    assert mtc.land_rich_gains(0.5).outcome is False and mtc.land_rich_gains(0.51).outcome is True


def test_183_day_rolling_window_crosses_fiscal_years():
    # 100 days at the end of 2025 + 100 days at the start of 2026: each calendar year < 183,
    # but a twelve-month window ending in 2026 contains all 200.
    days = [date(2025, 9, 1) + timedelta(days=i) for i in range(100)] + \
           [date(2026, 1, 1) + timedelta(days=i) for i in range(100)]
    r = mtc.max_days_any_12_months(days, date(2026, 1, 1), date(2026, 12, 31))
    assert r.outcome == 200
    assert mtc.employment_income(r.outcome, False, False).outcome == "work_state_may_tax"
    assert mtc.employment_income(150, False, False).outcome == "residence_only"
    assert mtc.employment_income(150, True, False).outcome == "work_state_may_tax"


def test_ppt_is_documented_not_decided():
    assert mtc.principal_purpose_test().outcome is None
    assert mtc.principal_purpose_test(True, False).outcome == "benefit_denied"
    assert mtc.principal_purpose_test(True, True).outcome == "benefit_granted"


# --- WTO DSU -------------------------------------------------------------------------------------

def test_dsu_consultation_deadlines():
    r = timeline("2026-01-15", as_of="2026-01-01")
    d = {m["label"]: m["date"] for m in r.outcome}
    assert d["Reply to the request for consultations"] == "2026-01-25"
    assert d["Consultations to begin"] == "2026-02-14"
    assert d["Panel may be requested if consultations fail"] == "2026-03-16"


def test_dsu_urgent_and_later_stages():
    r = timeline("2026-01-15", urgent=True, panel_composed="2026-03-01", reports_adopted="2026-10-01",
                 rpt_expires="2027-06-01", as_of="2026-01-01")
    d = {m["label"]: m["date"] for m in r.outcome}
    assert d["Panel may be requested if consultations fail (urgent case)"] == "2026-02-04"
    assert d["Final report to the parties (guideline)"] == "2026-06-01"  # 3 months in urgent cases
    assert d["Member states its implementation intentions"] == "2026-10-31"
    assert d["Reasonable period: 15-month guideline for the arbitrator"] == "2028-01-01"
    assert d["Art. 22.6 arbitration to be completed (if level contested)"] == "2027-07-31"


def test_dsu_flags_appellate_body_paralysis():
    r = timeline("2024-01-10", panel_report_circulated="2025-05-01", appeal_notified="2025-06-01", as_of="2026-11-15")
    assert any(s.kind == "warning" and "into the void" in s.text for s in r.trace)


# --- CLI -------------------------------------------------------------------------------------------

def test_cli(capsys):
    assert main(["rules"]) == 0
    assert "wto_dsu.timeline" in capsys.readouterr().out
    assert main(["run", "oecd_mtc.construction_pe", '{"start": "2025-01-01", "end": "2026-06-01"}']) == 0
    assert "PE" in capsys.readouterr().out
    assert main(["run", "nope"]) == 2
    assert main(["index", "--format", "csv"]) == 0
