# Codifiability index

38 provisions · 12 executable rules · 37 documented ambiguities

## Rubric

- **A — Computable:** Every condition is a determinate fact (date, amount, count, category) and the legal consequence follows mechanically. Code can apply the rule end to end.
- **B — Structurable:** The structure of the test is fixed, but at least one element is an open-textured standard that needs evaluative judgment (e.g. 'centre of vital interests', 'preparatory or auxiliary', 'like'). Code can sequence the test and record the judgment, not make it.
- **C — Not codifiable:** The outcome turns on purposive interpretation or open balancing with no stable decision structure (e.g. 'one of the principal purposes', 'object and purpose'). Code can document, not decide.

## Summary

| Instrument | A | B | C |
|---|---|---|---|
| General Agreement on Trade in Services (1994) | 1 | 6 | 0 |
| OECD GloBE Model Rules (2021) and Administrative Guidance | 3 | 0 | 0 |
| OECD Model Tax Convention (2017) | 6 | 4 | 2 |
| WTO Dispute Settlement Understanding (1994) | 12 | 3 | 1 |
| **All** | **22** | **13** | **3** |

## General Agreement on Trade in Services (1994)

### Art. I:3(b)-(c) — Services supplied in the exercise of governmental authority · class B (Structurable)

Excluded if supplied neither on a commercial basis nor in competition with one or more suppliers.

*Why:* 'Commercial basis' and 'in competition' are evaluative.  
*Implemented by:* [external](https://github.com/AlirezaMahdavishirkharkolaei/wto-gats-reasoning-engine)

### Art. II:1 — Most-favoured-nation treatment · class B (Structurable)

No less favourable treatment of services and suppliers of any Member than like ones of any other country.

*Why:* Likeness and less favourable treatment are evaluative.  
*Implemented by:* [external](https://github.com/AlirezaMahdavishirkharkolaei/wto-gats-reasoning-engine)

*Ambiguities found:*
- De facto discrimination requires an effects analysis.

### Art. XIV(a)-(e) — General exceptions: paragraphs and necessity · class B (Structurable)

Closed list of objectives; necessity as weighing and balancing with a reasonably available alternative.

*Why:* The structure is fixed; necessity is a weighing exercise.  
*Implemented by:* [external](https://github.com/AlirezaMahdavishirkharkolaei/wto-gats-reasoning-engine)

*Ambiguities found:*
- 'Public order' carries a qualifying footnote (fn. 5) absent from GATT Art. XX.

### Art. XIV chapeau — Chapeau · class B (Structurable)

No arbitrary or unjustifiable discrimination where like conditions prevail; no disguised restriction.

*Why:* Two fixed limbs, each requiring an evaluative assessment of how the measure is applied.  
*Implemented by:* [external](https://github.com/AlirezaMahdavishirkharkolaei/wto-gats-reasoning-engine)

### Art. XIV bis — Security exceptions · class B (Structurable)

Measures the Member considers necessary for essential security interests in listed circumstances.

*Why:* Listed circumstances are reviewable; the necessity element is largely self-judging, subject to good faith.  
*Implemented by:* [external](https://github.com/AlirezaMahdavishirkharkolaei/wto-gats-reasoning-engine)

### Art. XVI:2 — Market access: prohibited measure types · class A (Computable)

Six exhaustively listed types of limitation in committed sectors, unless scheduled.

*Why:* A closed list of measure types; classification of a measure is mostly categorical.  
*Implemented by:* [external](https://github.com/AlirezaMahdavishirkharkolaei/wto-gats-reasoning-engine)

*Ambiguities found:*
- Whether a total ban is a 'zero quota' was resolved by interpretation (US - Gambling), not by the text.

### Art. XVII — National treatment · class B (Structurable)

No less favourable treatment than domestic like services and suppliers in committed sectors.

*Why:* Likeness and modification of the conditions of competition are evaluative.  
*Implemented by:* [external](https://github.com/AlirezaMahdavishirkharkolaei/wto-gats-reasoning-engine)


## OECD GloBE Model Rules (2021) and Administrative Guidance

### Art. 5.2 — Top-up tax percentage · class A (Computable)

Minimum rate (15%) minus the jurisdictional effective tax rate.

*Why:* Arithmetic on determinate inputs.  
*Implemented by:* [external](https://github.com/AlirezaMahdavishirkharkolaei/Tax_Risk_AI)

*Ambiguities found:*
- Computing the GloBE ETR itself requires extensive adjustments to accounts.

### Art. 5.3 and 9.2 — Substance-based income exclusion · class A (Computable)

Percentage of eligible payroll costs and tangible assets, with transitional rates.

*Why:* Rates and bases are determinate.  
*Implemented by:* [external](https://github.com/AlirezaMahdavishirkharkolaei/Tax_Risk_AI)

*Ambiguities found:*
- Eligibility of costs and assets requires classification choices.

### Administrative Guidance (Dec. 2022) — Transitional CbCR Safe Harbour · class A (Computable)

De minimis, simplified ETR and routine profits tests on CbCR data.

*Why:* Fixed thresholds applied to reported figures.  
*Implemented by:* [external](https://github.com/AlirezaMahdavishirkharkolaei/Tax_Risk_AI)

*Ambiguities found:*
- Requires 'qualified' CbCR and financial statements.


## OECD Model Tax Convention (2017)

### Art. 10(2) — Dividends: source-State limit · class A (Computable)

Source tax may not exceed 5% of the gross dividend if the beneficial owner is a company holding directly at least 25% of the capital throughout a 365-day period that includes the day of payment; 15% in all other cases.

*Why:* Rates, the 25% threshold and the 365-day period are determinate; beneficial ownership is the only open element.  
*Implemented by:* `oecd_mtc.withholding_rate`

*Ambiguities found:*
- 'Beneficial owner' is not defined in the treaty; the Commentary gives an autonomous, anti-conduit meaning.
- Changes of ownership from corporate reorganisations are disregarded in computing the 365 days, which the code cannot see unless told.

### Art. 11(2) — Interest: source-State limit · class A (Computable)

Source tax may not exceed 10% of the gross interest if the beneficial owner is a resident of the other State.

*Why:* A single rate with one open element (beneficial ownership).  
*Implemented by:* `oecd_mtc.withholding_rate`

*Ambiguities found:*
- Treaties frequently provide exemptions (government, banks, pension funds) absent from the Model.

### Art. 12(1) — Royalties: residence-State taxation only · class A (Computable)

Royalties arising in one State and beneficially owned by a resident of the other State are taxable only in the other State.

*Why:* Exclusive residence taxation; the open element is whether a payment is a 'royalty' (classification).  
*Implemented by:* `oecd_mtc.withholding_rate`

*Ambiguities found:*
- The boundary between royalties and business profits (software, know-how vs. services) is a classification question the code takes as input.
- Many treaties, and the UN Model, allow source taxation of royalties.

### Art. 13(4) — Gains on shares deriving value from immovable property · class A (Computable)

Gains from alienating shares or comparable interests may be taxed where the immovable property is situated if, at any time during the 365 days preceding the alienation, they derived more than 50% of their value directly or indirectly from that immovable property.

*Why:* The 50% threshold and the 365-day look-back are determinate once values are known.  
*Implemented by:* `oecd_mtc.land_rich_gains`

*Ambiguities found:*
- The valuation method and the treatment of liabilities are not specified.

### Art. 15(1)-(2) — Employment income: the 183-day rule · class A (Computable)

Remuneration for employment exercised in the other State is taxable only in the residence State if (a) the employee is present there for periods not exceeding 183 days in any twelve-month period commencing or ending in the fiscal year concerned, (b) the remuneration is paid by or on behalf of an employer not resident there, and (c) it is not borne by a PE the employer has there.

*Why:* Day counts and the three cumulative conditions are determinate.  
*Implemented by:* `oecd_mtc.employment_income`, `oecd_mtc.max_days_any_12_months`

*Ambiguities found:*
- Days of physical presence include part-days, arrival and departure days (Commentary) - a counting convention the code must choose explicitly.
- Who is the 'employer' in hiring-out and secondment arrangements is a substance question (Commentary).

### Art. 29(9) — Principal purpose test · class C (Not codifiable)

A treaty benefit is denied if obtaining it was one of the principal purposes of an arrangement or transaction, unless granting it would be in accordance with the object and purpose of the relevant provisions.

*Why:* Both limbs are purposive judgments without a stable decision structure.  
*Implemented by:* `oecd_mtc.principal_purpose_test`

*Ambiguities found:*
- 'One of the principal purposes' sets a low threshold whose evidential standard ('reasonable to conclude') is applied differently across tax administrations.

### Art. 4(2) — Tie-breaker for dual-resident individuals · class B (Structurable)

Successive tests: permanent home available; centre of vital interests (closer personal and economic relations); habitual abode; nationality; otherwise mutual agreement.

*Why:* The cascade is fixed and the first, third and fourth tests are factual, but 'centre of vital interests' requires weighing personal and economic ties.  
*Implemented by:* `oecd_mtc.residence_tiebreaker_individual`

*Ambiguities found:*
- 'Permanent home available' depends on the quality of the dwelling and its availability, not ownership: a factual but open threshold.
- No weighting is given between personal and economic relations in the vital-interests test.
- 'Habitual abode' has no day-count; the Commentary refers to frequency, duration and regularity of stays over a sufficient period.

### Art. 4(3) — Dual-resident persons other than individuals · class C (Not codifiable)

The competent authorities endeavour to determine residence by mutual agreement, having regard to place of effective management, place of incorporation and other relevant factors; failing agreement, no treaty relief except as agreed.

*Why:* The outcome is left to negotiation between the competent authorities, with no decision rule.  
*Implemented by:* `oecd_mtc.residence_tiebreaker_entity`

*Ambiguities found:*
- Pre-2017 treaties use place of effective management as an automatic tie-breaker instead; check which version the treaty follows.

### Art. 5(1) — Fixed place of business permanent establishment · class B (Structurable)

A fixed place of business through which the business of an enterprise is wholly or partly carried on.

*Why:* Elements (place, fixed, at the disposal of the enterprise, business carried on through it) are evaluative.  
*Implemented by:* `oecd_mtc.fixed_place_pe`, `oecd_mtc.home_office_pe`

*Ambiguities found:*
- 'Fixed' implies a degree of permanence; the Commentary's six-month practice is guidance, not a rule.
- Home offices: under the 2025 Commentary, generally no PE where the individual works from that place less than 50% of working time over any 12-month period; at or above 50%, a PE turns on a commercial reason for the activity being carried on in that State.

*Status:* The 2025 Update (approved 18 Nov 2025) added Commentary on cross-border work from a home or other relevant place (Art. 5), an optional natural-resources provision, and changes to Arts. 9, 25 and 26 Commentary.

### Art. 5(3) — Building site or construction or installation project · class A (Computable)

Constitutes a PE only if it lasts more than twelve months.

*Why:* Duration is a determinate fact; the consequence follows mechanically.  
*Implemented by:* `oecd_mtc.construction_pe`

*Ambiguities found:*
- When a site 'starts' and 'ends' (preparatory work, interruptions) is a factual question with Commentary guidance.
- Splitting contracts among related enterprises to stay under 12 months is addressed by the principal purpose test (Art. 29(9)) rather than by Art. 5(3) itself; some treaties add an aggregation rule.

### Art. 5(4) and 5(4.1) — Preparatory or auxiliary activities and anti-fragmentation · class B (Structurable)

Listed activities do not create a PE if preparatory or auxiliary; the exception does not apply where closely related enterprises' complementary functions form a cohesive business operation.

*Why:* 'Preparatory or auxiliary' and 'cohesive business operation' require judgment.  
*Implemented by:* `oecd_mtc.fixed_place_pe`

*Ambiguities found:*
- Whether the 2017 'preparatory or auxiliary' condition applies to every listed activity depends on which treaty option (or MLI choice) applies.

### Art. 5(5)-(6) — Dependent agent permanent establishment · class B (Structurable)

A person acting on behalf of the enterprise who habitually concludes contracts, or habitually plays the principal role leading to contracts routinely concluded without material modification, creates a PE unless an independent agent acting in the ordinary course of business; a person acting exclusively or almost exclusively for closely related enterprises is not independent.

*Why:* 'Habitually', 'principal role' and 'material modification' are evaluative.  
*Implemented by:* `oecd_mtc.dependent_agent_pe`

*Ambiguities found:*
- Pre-2017 treaties use the narrower 'authority to conclude contracts' test.


## WTO Dispute Settlement Understanding (1994)

### Art. 12.8 — Duration of panel proceedings · class A (Computable)

From composition and terms of reference to the final report to the parties: generally no more than 6 months (3 months in urgent cases).

*Why:* Fixed period; the legal consequence of exceeding it is only an obligation to inform the DSB (Art. 12.9).  
*Implemented by:* `wto_dsu.timeline`

*Ambiguities found:*
- The time limit is phrased as 'shall generally' or 'should', and practice regularly exceeds it.

### Art. 12.9 — Maximum period for panel reports · class A (Computable)

If the panel cannot report within 6 months it informs the DSB; the period from establishment to circulation should in no case exceed 9 months.

*Why:* Fixed period, hortatory in effect.  
*Implemented by:* `wto_dsu.timeline`

*Ambiguities found:*
- The time limit is phrased as 'shall generally' or 'should', and practice regularly exceeds it.

### Art. 16.4 — Adoption of panel reports · class A (Computable)

Within 60 days after circulation the report is adopted at a DSB meeting unless a party notifies an appeal or the DSB decides by consensus not to adopt; it is not considered for adoption until 20 days after circulation (Art. 16.1).

*Why:* Fixed window; adoption by negative consensus.  
*Implemented by:* `wto_dsu.timeline`

*Ambiguities found:*
- Since 11 December 2019 the Appellate Body has had no quorum. An appeal 'into the void' prevents adoption indefinitely, so the code can compute the Art. 16.4 window but not predict adoption.

*Status:* Appellate Body not operational since 11 December 2019; some Members use the Multi-Party Interim Appeal Arbitration Arrangement (MPIA) under Art. 25.

### Art. 17.14 — Adoption of Appellate Body reports · class A (Computable)

Adopted by the DSB and unconditionally accepted by the parties unless the DSB decides by consensus not to, within 30 days following circulation.

*Why:* Fixed period, negative consensus.  
*Implemented by:* `wto_dsu.timeline`

### Art. 17.5 — Duration of appellate proceedings · class A (Computable)

Generally no more than 60 days from notice of appeal to circulation, and in no case more than 90 days.

*Why:* Fixed period.  
*Implemented by:* `wto_dsu.timeline`

*Ambiguities found:*
- The time limit is phrased as 'shall generally' or 'should', and practice regularly exceeds it.
- Inapplicable in practice while the Appellate Body has no quorum.

### Art. 20 — Overall time frame · class A (Computable)

From establishment of the panel to DSB consideration of the report: generally no more than 9 months without appeal, 12 months with appeal.

*Why:* Fixed periods.  
*Implemented by:* `wto_dsu.timeline`

*Ambiguities found:*
- The time limit is phrased as 'shall generally' or 'should', and practice regularly exceeds it.

### Art. 21.3 — Reasonable period of time for implementation · class B (Structurable)

The Member concerned states its intentions within 30 days after adoption. If immediate compliance is impracticable it has a reasonable period of time, which arbitration under Art. 21.3(c) (within 90 days of adoption) determines with a guideline of no more than 15 months.

*Why:* The procedural steps are fixed, but the length of the reasonable period is an evaluative determination.  
*Implemented by:* `wto_dsu.timeline`

*Ambiguities found:*
- The 15-month figure is a 'guideline' that may be shorter or longer 'depending upon the particular circumstances'.

### Art. 21.5 — Compliance proceedings · class A (Computable)

Disagreement on compliance is decided by recourse to the dispute settlement procedures, wherever possible by the original panel, which circulates its report within 90 days of referral.

*Why:* Fixed period.  
*Implemented by:* `wto_dsu.timeline`

*Ambiguities found:*
- The time limit is phrased as 'shall generally' or 'should', and practice regularly exceeds it.
- The sequencing of Arts. 21.5 and 22 is not settled in the text; parties agree sequencing arrangements.

### Art. 22.2 — Compensation and suspension of concessions · class A (Computable)

If the Member fails to comply within the reasonable period, it negotiates compensation on request; if none is agreed within 20 days after the expiry of that period, the complainant may request authorization to suspend concessions.

*Why:* Fixed day count from the end of the reasonable period.  
*Implemented by:* `wto_dsu.timeline`

### Art. 22.6 — Authorization to suspend and Art. 22.6 arbitration · class B (Structurable)

The DSB grants authorization within 30 days of the expiry of the reasonable period unless it decides by consensus to reject; an objection to the level goes to arbitration, completed within 60 days after expiry of the period.

*Why:* The time limits are fixed; the level of suspension (equivalence with nullification) is an economic assessment.  
*Implemented by:* `wto_dsu.timeline`

*Ambiguities found:*
- The 30-day and 60-day limits run from the same date, which practice has had to reconcile.

### Art. 25 — Arbitration as an alternative means · class C (Not codifiable)

Parties may agree to arbitration as an alternative means of dispute settlement; awards are notified to the DSB.

*Why:* Procedure and timing depend entirely on the parties' agreement (e.g. the MPIA).  
*Implemented by:* `wto_dsu.timeline`

*Status:* Basis of the MPIA used by a group of Members while the Appellate Body is not operational.

### Art. 4.3 — Reply to and entry into consultations · class A (Computable)

The responding Member replies within 10 days of receiving a request for consultations and enters into consultations within 30 days; otherwise the complainant may proceed directly to request a panel.

*Why:* Fixed day counts from a dated event.  
*Implemented by:* `wto_dsu.timeline`

### Art. 4.7 — Request for a panel after consultations · class A (Computable)

If consultations fail to settle the dispute within 60 days after receipt of the request, the complainant may request a panel (earlier if both parties consider that consultations have failed).

*Why:* Fixed day count; the early-request exception depends on a joint position recorded as an input.  
*Implemented by:* `wto_dsu.timeline`

### Art. 4.8 — Urgent cases · class B (Structurable)

In cases of urgency, including perishable goods, consultations start within 10 days and a panel may be requested if they fail within 20 days.

*Why:* The time limits are fixed but whether a case is 'urgent' is evaluative.  
*Implemented by:* `wto_dsu.timeline`

*Ambiguities found:*
- 'Cases of urgency' is not defined beyond the perishable-goods example.

### Art. 6.1 — Establishment of a panel · class A (Computable)

A panel is established at the latest at the DSB meeting following the one at which the request first appears as an item, unless the DSB decides by consensus not to.

*Why:* Negative consensus makes establishment automatic at the second meeting.  
*Implemented by:* `wto_dsu.timeline`

*Ambiguities found:*
- The date depends on the DSB meeting calendar, which the code takes as input.

### Art. 8.7 — Composition of the panel by the Director-General · class A (Computable)

If panelists are not agreed within 20 days after establishment, either party may ask the Director-General, who appoints them within 10 days of the request being transmitted to the DSB Chair.

*Why:* Fixed day counts.  
*Implemented by:* `wto_dsu.timeline`

