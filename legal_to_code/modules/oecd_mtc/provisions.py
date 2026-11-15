"""Provisions of the OECD Model encoded in this module, with their codifiability class and the ambiguities found."""

from ...core import REGISTRY, Codifiability as C, Provision

MTC = "OECD Model Tax Convention (2017)"
NOTE_2025 = ("The 2025 Update (approved 18 Nov 2025) added Commentary on cross-border work from a home or other relevant "
             "place (Art. 5), an optional natural-resources provision, and changes to Arts. 9, 25 and 26 Commentary.")


def P(pid, article, title, summary, cls, rationale, ambiguities=(), implemented_by=(), status_note=""):
    return Provision(f"OECD-MTC:{pid}", MTC, article, title, summary, cls, rationale, tuple(ambiguities),
                     "", "oecd_mtc", tuple(implemented_by), status_note)


REGISTRY.add(
    P("4(2)", "Art. 4(2)", "Tie-breaker for dual-resident individuals",
      "Successive tests: permanent home available; centre of vital interests (closer personal and economic relations); "
      "habitual abode; nationality; otherwise mutual agreement.",
      C.B, "The cascade is fixed and the first, third and fourth tests are factual, but 'centre of vital interests' "
           "requires weighing personal and economic ties.",
      ["'Permanent home available' depends on the quality of the dwelling and its availability, not ownership: a factual "
       "but open threshold.",
       "No weighting is given between personal and economic relations in the vital-interests test.",
       "'Habitual abode' has no day-count; the Commentary refers to frequency, duration and regularity of stays over a "
       "sufficient period."],
      ["oecd_mtc.residence_tiebreaker_individual"]),
    P("4(3)", "Art. 4(3)", "Dual-resident persons other than individuals",
      "The competent authorities endeavour to determine residence by mutual agreement, having regard to place of "
      "effective management, place of incorporation and other relevant factors; failing agreement, no treaty relief "
      "except as agreed.",
      C.C, "The outcome is left to negotiation between the competent authorities, with no decision rule.",
      ["Pre-2017 treaties use place of effective management as an automatic tie-breaker instead; check which version "
       "the treaty follows."],
      ["oecd_mtc.residence_tiebreaker_entity"]),
    P("5(1)", "Art. 5(1)", "Fixed place of business permanent establishment",
      "A fixed place of business through which the business of an enterprise is wholly or partly carried on.",
      C.B, "Elements (place, fixed, at the disposal of the enterprise, business carried on through it) are evaluative.",
      ["'Fixed' implies a degree of permanence; the Commentary's six-month practice is guidance, not a rule.",
       "Home offices: under the 2025 Commentary, generally no PE where the individual works from that place less than "
       "50% of working time over any 12-month period; at or above 50%, a PE turns on a commercial reason for the "
       "activity being carried on in that State."],
      ["oecd_mtc.fixed_place_pe", "oecd_mtc.home_office_pe"], NOTE_2025),
    P("5(3)", "Art. 5(3)", "Building site or construction or installation project",
      "Constitutes a PE only if it lasts more than twelve months.",
      C.A, "Duration is a determinate fact; the consequence follows mechanically.",
      ["When a site 'starts' and 'ends' (preparatory work, interruptions) is a factual question with Commentary guidance.",
       "Splitting contracts among related enterprises to stay under 12 months is addressed by the principal purpose "
       "test (Art. 29(9)) rather than by Art. 5(3) itself; some treaties add an aggregation rule."],
      ["oecd_mtc.construction_pe"]),
    P("5(4)", "Art. 5(4) and 5(4.1)", "Preparatory or auxiliary activities and anti-fragmentation",
      "Listed activities do not create a PE if preparatory or auxiliary; the exception does not apply where closely "
      "related enterprises' complementary functions form a cohesive business operation.",
      C.B, "'Preparatory or auxiliary' and 'cohesive business operation' require judgment.",
      ["Whether the 2017 'preparatory or auxiliary' condition applies to every listed activity depends on which treaty "
       "option (or MLI choice) applies."],
      ["oecd_mtc.fixed_place_pe"]),
    P("5(5)-(6)", "Art. 5(5)-(6)", "Dependent agent permanent establishment",
      "A person acting on behalf of the enterprise who habitually concludes contracts, or habitually plays the principal "
      "role leading to contracts routinely concluded without material modification, creates a PE unless an independent "
      "agent acting in the ordinary course of business; a person acting exclusively or almost exclusively for closely "
      "related enterprises is not independent.",
      C.B, "'Habitually', 'principal role' and 'material modification' are evaluative.",
      ["Pre-2017 treaties use the narrower 'authority to conclude contracts' test."],
      ["oecd_mtc.dependent_agent_pe"]),
    P("10(2)", "Art. 10(2)", "Dividends: source-State limit",
      "Source tax may not exceed 5% of the gross dividend if the beneficial owner is a company holding directly at least "
      "25% of the capital throughout a 365-day period that includes the day of payment; 15% in all other cases.",
      C.A, "Rates, the 25% threshold and the 365-day period are determinate; beneficial ownership is the only open element.",
      ["'Beneficial owner' is not defined in the treaty; the Commentary gives an autonomous, anti-conduit meaning.",
       "Changes of ownership from corporate reorganisations are disregarded in computing the 365 days, which the code "
       "cannot see unless told."],
      ["oecd_mtc.withholding_rate"]),
    P("11(2)", "Art. 11(2)", "Interest: source-State limit",
      "Source tax may not exceed 10% of the gross interest if the beneficial owner is a resident of the other State.",
      C.A, "A single rate with one open element (beneficial ownership).",
      ["Treaties frequently provide exemptions (government, banks, pension funds) absent from the Model."],
      ["oecd_mtc.withholding_rate"]),
    P("12(1)", "Art. 12(1)", "Royalties: residence-State taxation only",
      "Royalties arising in one State and beneficially owned by a resident of the other State are taxable only in the "
      "other State.",
      C.A, "Exclusive residence taxation; the open element is whether a payment is a 'royalty' (classification).",
      ["The boundary between royalties and business profits (software, know-how vs. services) is a classification "
       "question the code takes as input.",
       "Many treaties, and the UN Model, allow source taxation of royalties."],
      ["oecd_mtc.withholding_rate"]),
    P("13(4)", "Art. 13(4)", "Gains on shares deriving value from immovable property",
      "Gains from alienating shares or comparable interests may be taxed where the immovable property is situated if, "
      "at any time during the 365 days preceding the alienation, they derived more than 50% of their value directly or "
      "indirectly from that immovable property.",
      C.A, "The 50% threshold and the 365-day look-back are determinate once values are known.",
      ["The valuation method and the treatment of liabilities are not specified."],
      ["oecd_mtc.land_rich_gains"]),
    P("15(2)", "Art. 15(1)-(2)", "Employment income: the 183-day rule",
      "Remuneration for employment exercised in the other State is taxable only in the residence State if (a) the "
      "employee is present there for periods not exceeding 183 days in any twelve-month period commencing or ending in "
      "the fiscal year concerned, (b) the remuneration is paid by or on behalf of an employer not resident there, and "
      "(c) it is not borne by a PE the employer has there.",
      C.A, "Day counts and the three cumulative conditions are determinate.",
      ["Days of physical presence include part-days, arrival and departure days (Commentary) - a counting convention the "
       "code must choose explicitly.",
       "Who is the 'employer' in hiring-out and secondment arrangements is a substance question (Commentary)."],
      ["oecd_mtc.employment_income", "oecd_mtc.max_days_any_12_months"]),
    P("29(9)", "Art. 29(9)", "Principal purpose test",
      "A treaty benefit is denied if obtaining it was one of the principal purposes of an arrangement or transaction, "
      "unless granting it would be in accordance with the object and purpose of the relevant provisions.",
      C.C, "Both limbs are purposive judgments without a stable decision structure.",
      ["'One of the principal purposes' sets a low threshold whose evidential standard ('reasonable to conclude') is "
       "applied differently across tax administrations."],
      ["oecd_mtc.principal_purpose_test"]),
)
