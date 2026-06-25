"""
draft_generator.py
==================
Module 5 — Standardised Bail Application Draft Generator
Supports: Sessions Court | High Court | Supreme Court (SLP)
Author  : AI Legal Research & Drafting Assistant
"""

from datetime import datetime
from typing import List, Dict, Optional, Any


# --------------------------------------------------
# INTERNAL HELPERS
# --------------------------------------------------

def _today() -> str:
    return datetime.now().strftime("%d %B %Y")


def _format_loopholes_as_grounds(loopholes: List[Dict]) -> str:
    """Convert loophole objects into numbered legal ground paragraphs."""
    if not loopholes:
        return "    (i)  The applicant has fully cooperated with the investigating agency.\n    (ii) There is no credible evidence linking the applicant to the alleged offence.\n    (iii) The applicant undertakes not to tamper with evidence or influence witnesses."

    lines = []
    roman = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x",
             "xi", "xii", "xiii", "xiv", "xv"]

    for idx, lh in enumerate(loopholes):
        numeral = roman[idx] if idx < len(roman) else str(idx + 1)
        category  = lh.get("category", "Legal Ground")
        finding   = lh.get("finding", "")
        basis     = lh.get("legal_basis", "")
        strategy  = lh.get("defense_strategy", "")

        block = (
            f"    ({numeral}) [{category.upper()}]\n"
            f"            {finding}\n"
        )
        if basis:
            block += f"            Legal Basis  : {basis}\n"
        if strategy:
            block += f"            Submission   : {strategy}\n"

        lines.append(block)

    return "\n".join(lines)


def _format_sections(sections: List[str]) -> str:
    if not sections:
        return "Sections as mentioned in the FIR / Chargesheet"
    return ", ".join(sections)


def _safe(value: Any, default: str = "Not Available") -> str:
    if value is None or (isinstance(value, str) and not value.strip()):
        return default
    return str(value)


# --------------------------------------------------
# COURT-SPECIFIC DRAFT BUILDERS
# --------------------------------------------------

def generate_sessions_court_draft(
    case_id: str,
    accused_name: str,
    offence: str,
    sections_applied: List[str],
    arrest_date: Optional[str],
    magistrate_presentation_time: Optional[str],
    evidentiary_items: List[str],
    witness_statements: List[Dict],
    loopholes: List[Dict],
    fir_number: str = "As per records",
    police_station: str = "Concerned Police Station",
    district: str = "Concerned District",
    advocate_name: str = "Counsel for the Applicant",
    state: str = "State"
) -> str:

    grounds = _format_loopholes_as_grounds(loopholes)
    sections_str = _format_sections(sections_applied)
    arrest_str = _safe(arrest_date, "As per arrest memo")
    magistrate_str = _safe(magistrate_presentation_time, "As per remand records")

    evidence_block = ""
    if evidentiary_items:
        evidence_block = "\n    Evidentiary items on record:\n"
        for item in evidentiary_items:
            evidence_block += f"        • {item}\n"

    witness_block = ""
    if witness_statements:
        witness_block = "\n    Witness statements on record:\n"
        for ws in witness_statements:
            w = ws.get("witness", "Unknown")
            s = ws.get("statement", "")
            witness_block += f"        • {w}: \"{s}\"\n"

    draft = f"""
================================================================================
                    IN THE COURT OF SESSIONS JUDGE
                    AT {district.upper()}
================================================================================

                        BAIL APPLICATION NO. _______ / {datetime.now().year}

IN THE MATTER OF:

        {accused_name.upper()}                                        ... APPLICANT / ACCUSED
                                vs.
        STATE OF {state.upper()}                                      ... RESPONDENT

--------------------------------------------------------------------------------
        FIR No.         : {fir_number}
        Police Station  : {police_station}
        Case Reference  : {case_id}
        Offence         : {offence}
        Sections Applied: {sections_str}
        Date of Arrest  : {arrest_str}
        Produced Before
        Magistrate On   : {magistrate_str}
--------------------------------------------------------------------------------

                        APPLICATION FOR REGULAR BAIL
              UNDER SECTION 483 OF THE BHARATIYA NAGARIK SURAKSHA
                         SANHITA, 2023 (BNSS, 2023)

TO,
THE HON'BLE SESSIONS JUDGE,
{district.upper()}.

MOST RESPECTFULLY SHOWETH:

1.  INTRODUCTION
    ─────────────
    That the present application is being filed on behalf of the Applicant,
    {accused_name}, who has been arrested in connection with FIR No. {fir_number}
    registered at {police_station} Police Station for alleged offences punishable
    under {sections_str} of the Bharatiya Nyaya Sanhita, 2023 (BNS) / Indian
    Penal Code (as applicable).

2.  BRIEF FACTS OF THE CASE
    ─────────────────────────
    (a) The Applicant was arrested on {arrest_str}.
    (b) The Applicant was produced before the learned Magistrate on {magistrate_str}.
    (c) The Applicant has been in judicial custody since the date of remand.
    (d) The Applicant denies all allegations levelled against him/her and reserves
        the right to contest the same at the appropriate stage.
{evidence_block}{witness_block}

3.  GROUNDS FOR BAIL
    ──────────────────
    That the Applicant is entitled to bail on the following grounds, which are
    submitted without prejudice and are based on settled principles of law:

{grounds}

4.  PERSONAL CIRCUMSTANCES OF THE APPLICANT
    ──────────────────────────────────────────
    (a) The Applicant is a law-abiding citizen with deep roots in the community
        and permanent place of residence within the jurisdiction.
    (b) The Applicant has no prior criminal antecedents / history of conviction.
    (c) The Applicant is the sole breadwinner of his/her family and his/her
        continued incarceration is causing irreparable financial and emotional
        hardship to the family members who are dependent upon him/her.
    (d) The Applicant is not a flight risk and undertakes to remain available
        for investigation and trial at all times.
    (e) The Applicant undertakes to fully cooperate with the investigating agency
        and shall not tamper with evidence or influence any witness.

5.  ON THE APPLICABILITY OF JUDICIAL PRECEDENTS
    ───────────────────────────────────────────────
    (a) That in Arnesh Kumar v. State of Bihar, (2014) 8 SCC 273, the Hon'ble
        Supreme Court held that arrest must be the last resort and not the
        first impulse of the police. The present arrest does not satisfy the
        mandate laid down therein.
    (b) That in Satender Kumar Antil v. Central Bureau of Investigation,
        (2022) 10 SCC 51, the Hon'ble Supreme Court reiterated that the
        default rule is bail and not jail, and courts must not mechanically
        refuse bail without application of mind.
    (c) That in Sanjay Chandra v. CBI, (2012) 1 SCC 40, it was held that
        the object of bail is to secure the appearance of the accused at
        trial, and bail is not to be withheld as a punishment.
    (d) That in P. Chidambaram v. Directorate of Enforcement, (2019) 9 SCC 24,
        the Hon'ble Supreme Court laid down that gravity of the offence alone
        cannot be the sole ground to deny bail.

6.  TRIPLE TEST COMPLIANCE
    ──────────────────────────
    The Applicant satisfies all three prongs of the "Triple Test" established
    by the Hon'ble Supreme Court:
    (a) FLIGHT RISK     : The Applicant is not a flight risk. He/She has
                          strong community ties and a permanent residence.
    (b) EVIDENCE TAMPER : The Applicant has no means or motive to tamper
                          with evidence, most of which is already in the
                          custody of the investigating agency.
    (c) REPEAT OFFENCE  : There is no reasonable apprehension that the
                          Applicant will commit any offence while on bail.

7.  PRAYER
    ────────
    In view of the foregoing facts, circumstances, and legal submissions,
    it is most respectfully prayed that this Hon'ble Court may be pleased to:

    (a) GRANT regular bail to the Applicant, {accused_name}, in connection
        with FIR No. {fir_number} registered at {police_station} Police
        Station under {sections_str};

    (b) IMPOSE such conditions as this Hon'ble Court may deem fit and proper
        in the interest of justice; and

    (c) PASS such other and further order(s) as this Hon'ble Court may deem
        fit and proper in the facts and circumstances of the case.

                                        AND FOR THIS ACT OF KINDNESS,
                                        THE APPLICANT SHALL EVER PRAY.

--------------------------------------------------------------------------------
Place : {district}
Date  : {_today()}

                                        ____________________________________
                                        {advocate_name}
                                        COUNSEL FOR THE APPLICANT
                                        Enrolment No.: ___________________
                                        Mobile No.   : ___________________
--------------------------------------------------------------------------------

VERIFICATION:

I, {accused_name}, the Applicant above-named, do hereby verify and declare
that the contents of this application are true and correct to the best of my
knowledge and belief and nothing material has been concealed therefrom.

Verified at {district} on this {_today()}.

                                        ____________________________________
                                        APPLICANT
================================================================================
                        [CASE REFERENCE: {case_id}]
                   [GENERATED BY AI LEGAL DRAFTING ASSISTANT]
================================================================================
"""
    return draft.strip()


# --------------------------------------------------

def generate_high_court_draft(
    case_id: str,
    accused_name: str,
    offence: str,
    sections_applied: List[str],
    arrest_date: Optional[str],
    magistrate_presentation_time: Optional[str],
    evidentiary_items: List[str],
    witness_statements: List[Dict],
    loopholes: List[Dict],
    fir_number: str = "As per records",
    police_station: str = "Concerned Police Station",
    district: str = "Concerned District",
    sessions_court_order_date: str = "As per records",
    advocate_name: str = "Counsel for the Applicant",
    high_court_bench: str = "Concerned Bench",
    state: str = "State"
) -> str:

    grounds = _format_loopholes_as_grounds(loopholes)
    sections_str = _format_sections(sections_applied)
    arrest_str = _safe(arrest_date, "As per arrest memo")
    magistrate_str = _safe(magistrate_presentation_time, "As per remand records")

    draft = f"""
================================================================================
                    IN THE HIGH COURT OF JUDICATURE
                    AT {high_court_bench.upper()}

                    CRIMINAL MISCELLANEOUS BAIL APPLICATION
                              NO. _______ / {datetime.now().year}
================================================================================

IN THE MATTER OF:

        {accused_name.upper()}                                        ... APPLICANT
                                vs.
        STATE OF {state.upper()}                                      ... RESPONDENT

--------------------------------------------------------------------------------
        FIR No.                    : {fir_number}
        Police Station             : {police_station}, {district}
        Case Reference             : {case_id}
        Offence                    : {offence}
        Sections                   : {sections_str}
        Date of Arrest             : {arrest_str}
        Produced Before Magistrate : {magistrate_str}
        Sessions Court Order Date  : {sessions_court_order_date}
--------------------------------------------------------------------------------

              APPLICATION FOR BAIL UNDER SECTION 483 BNSS, 2023
         (Arising out of rejection of bail by the learned Sessions Court)

TO,
THE HON'BLE CHIEF JUSTICE AND HIS/HER COMPANION JUSTICES
OF THE HIGH COURT OF JUDICATURE AT {high_court_bench.upper()}.

MOST RESPECTFULLY SHOWETH:

1.  INTRODUCTION & JURISDICTION
    ──────────────────────────────
    That the present application is preferred under Section 483 of the
    Bharatiya Nagarik Suraksha Sanhita, 2023, read with Article 226/227
    of the Constitution of India, challenging the order dated
    {sessions_court_order_date} passed by the learned Sessions Court,
    {district}, whereby the prayer for regular bail of the Applicant,
    {accused_name}, was rejected.

2.  BRIEF FACTS
    ─────────────
    (a) That the Applicant, {accused_name}, was arrested on {arrest_str} in
        connection with FIR No. {fir_number} registered at {police_station}
        Police Station for alleged offences under {sections_str}.
    (b) That the Applicant was produced before the learned Magistrate on
        {magistrate_str}.
    (c) That the Applicant preferred a bail application before the learned
        Sessions Court which was dismissed vide order dated
        {sessions_court_order_date} without proper application of judicial mind.
    (d) That the Applicant is innocent and has been falsely implicated in
        the present case due to personal vendetta / ulterior motives of the
        complainant.

3.  IMPUGNED ORDER IS LEGALLY UNSUSTAINABLE
    ────────────────────────────────────────
    That the order dated {sessions_court_order_date} passed by the learned
    Sessions Court is liable to be set aside on the following grounds:

{grounds}

4.  SETTLED PROPOSITIONS OF LAW
    ────────────────────────────
    (a) In Arnesh Kumar v. State of Bihar, (2014) 8 SCC 273, the Hon'ble
        Supreme Court categorically held that personal liberty guaranteed
        under Article 21 of the Constitution cannot be curtailed without
        strict compliance of procedural safeguards.
    (b) In Satender Kumar Antil v. CBI, (2022) 10 SCC 51, the Hon'ble
        Supreme Court deprecated the practice of mechanically refusing bail
        and directed courts to consider bail applications on merits.
    (c) In Manish Sisodia v. Directorate of Enforcement, (2024) SCC OnLine
        SC 1876, the Hon'ble Supreme Court held that prolonged incarceration
        without trial violates Article 21 and bail must be granted.
    (d) In Re: Policy Strategy for Grant of Bail, (2023) SCC OnLine SC 532,
        the Hon'ble Supreme Court issued comprehensive guidelines mandating
        expeditious disposal of bail applications.

5.  PERSONAL ANTECEDENTS & TRIPLE TEST
    ─────────────────────────────────────
    (a) FLIGHT RISK     : Nil. The Applicant has permanent residence in
                          {district} and strong family ties.
    (b) EVIDENCE TAMPER : No possibility. Investigation is complete and
                          all material evidence is in custody of the agency.
    (c) REPEAT OFFENCE  : No apprehension. The Applicant has no prior
                          criminal record and is a person of standing
                          in the community.

6.  PRAYER
    ────────
    In view of the foregoing submissions, it is most respectfully prayed
    that this Hon'ble Court may be pleased to:

    (a) ADMIT this application;

    (b) GRANT regular bail to the Applicant, {accused_name}, in connection
        with FIR No. {fir_number}, {police_station} Police Station,
        {district}, under {sections_str}, on such terms and conditions
        as this Hon'ble Court may deem fit;

    (c) STAY the operation of the order dated {sessions_court_order_date}
        passed by the learned Sessions Court, {district}, pending disposal
        of this application; and

    (d) PASS such other and further order(s) as this Hon'ble Court may deem
        fit and proper in the facts and circumstances of the case.

                                        AND FOR THIS ACT OF KINDNESS,
                                        THE APPLICANT SHALL EVER PRAY.

--------------------------------------------------------------------------------
Place : {high_court_bench}
Date  : {_today()}

                                        ____________________________________
                                        {advocate_name}
                                        COUNSEL FOR THE APPLICANT
                                        Enrolment No.: ___________________
                                        Mobile No.   : ___________________
--------------------------------------------------------------------------------

VERIFICATION:

I, {accused_name}, the Applicant above-named, do hereby verify that the
contents of the above application are true and correct to the best of my
knowledge and belief and no material fact has been concealed therefrom.

Verified at {high_court_bench} on this {_today()}.

                                        ____________________________________
                                        APPLICANT
================================================================================
                        [CASE REFERENCE: {case_id}]
                   [GENERATED BY AI LEGAL DRAFTING ASSISTANT]
================================================================================
"""
    return draft.strip()


# --------------------------------------------------

def generate_supreme_court_draft(
    case_id: str,
    accused_name: str,
    offence: str,
    sections_applied: List[str],
    arrest_date: Optional[str],
    magistrate_presentation_time: Optional[str],
    evidentiary_items: List[str],
    witness_statements: List[Dict],
    loopholes: List[Dict],
    fir_number: str = "As per records",
    police_station: str = "Concerned Police Station",
    district: str = "Concerned District",
    high_court_order_date: str = "As per records",
    high_court_bench: str = "Concerned High Court",
    advocate_name: str = "Counsel for the Petitioner",
    state: str = "State"
) -> str:

    grounds = _format_loopholes_as_grounds(loopholes)
    sections_str = _format_sections(sections_applied)
    arrest_str = _safe(arrest_date, "As per arrest memo")

    draft = f"""
================================================================================
                IN THE SUPREME COURT OF INDIA
                CRIMINAL APPELLATE JURISDICTION

          SPECIAL LEAVE PETITION (CRIMINAL) NO. _______ / {datetime.now().year}
                   [ARISING FROM BAIL MATTER]
================================================================================

IN THE MATTER OF:

        {accused_name.upper()}                                        ... PETITIONER
                                vs.
        STATE OF {state.upper()} & ANR.                              ... RESPONDENTS

--------------------------------------------------------------------------------
        FIR No.                  : {fir_number}
        Police Station           : {police_station}, {district}
        Case Reference           : {case_id}
        Offence                  : {offence}
        Sections                 : {sections_str}
        Date of Arrest           : {arrest_str}
        High Court               : {high_court_bench}
        Impugned HC Order Date   : {high_court_order_date}
--------------------------------------------------------------------------------

         SPECIAL LEAVE PETITION UNDER ARTICLE 136 OF THE CONSTITUTION
         OF INDIA AGAINST THE IMPUGNED ORDER DATED {high_court_order_date.upper()}
         PASSED BY THE HON'BLE HIGH COURT OF {high_court_bench.upper()}
         DECLINING BAIL TO THE PETITIONER

TO,
THE HON'BLE CHIEF JUSTICE OF INDIA AND
HIS/HER COMPANION JUSTICES OF THE SUPREME COURT OF INDIA.

THE HUMBLE PETITION OF THE PETITIONER ABOVE-NAMED

MOST RESPECTFULLY SHOWETH:

1.  JURISDICTION
    ─────────────
    That this Special Leave Petition is preferred under Article 136 of the
    Constitution of India against the impugned order dated {high_court_order_date}
    passed by the Hon'ble High Court of {high_court_bench} in Criminal
    Miscellaneous Bail Application No. ___ / {datetime.now().year}, whereby the
    prayer for bail of the Petitioner, {accused_name}, was declined, causing
    grave miscarriage of justice and violation of the Petitioner's fundamental
    right to personal liberty guaranteed under Article 21 of the Constitution
    of India.

2.  DECLARATION AS TO MAINTAINABILITY
    ─────────────────────────────────────
    (a) That the impugned order has been passed by the Hon'ble High Court and
        the same involves substantial questions of law of general public
        importance as well as violation of the Petitioner's fundamental rights.
    (b) That no other petition arising out of this very cause of action has
        been filed before this Hon'ble Court previously.

3.  BRIEF FACTS
    ─────────────
    (a) That the Petitioner, {accused_name}, was arrested on {arrest_str} in
        connection with FIR No. {fir_number} registered at {police_station}
        for alleged offences under {sections_str}.
    (b) That the Petitioner's bail application was rejected by the learned
        Sessions Court and the said rejection was confirmed by the impugned
        order dated {high_court_order_date} of the Hon'ble High Court of
        {high_court_bench}.
    (c) That the Petitioner is totally innocent and has been falsely
        implicated. The impugned order is perverse, arbitrary, and contrary
        to settled principles of law.

4.  QUESTIONS OF LAW
    ──────────────────
    (a) Whether the Hon'ble High Court was justified in declining bail without
        properly applying the "Triple Test" as mandated by this Hon'ble Court?
    (b) Whether prolonged incarceration of the Petitioner without trial
        constitutes a violation of Article 21 of the Constitution of India?
    (c) Whether the impugned order is vitiated by non-application of judicial
        mind and non-consideration of vital material on record?

5.  GROUNDS
    ─────────

{grounds}

6.  BINDING PRECEDENTS OF THIS HON'BLE COURT
    ─────────────────────────────────────────
    (a) Arnesh Kumar v. State of Bihar, (2014) 8 SCC 273 — Arrest must be
        last resort; personal liberty cannot be curtailed mechanically.
    (b) Satender Kumar Antil v. CBI, (2022) 10 SCC 51 — Default rule is
        bail and not jail; courts must decide bail on merits.
    (c) Manish Sisodia v. ED, (2024) SCC OnLine SC 1876 — Bail must be
        granted where trial is not likely to conclude in near future and
        continued incarceration violates Article 21.
    (d) Sanjay Chandra v. CBI, (2012) 1 SCC 40 — Bail is rule, jail is
        exception; object of bail is to secure presence at trial.
    (e) P. Chidambaram v. ED, (2019) 9 SCC 24 — Gravity of offence alone
        cannot be a ground to deny bail; attending circumstances matter.
    (f) Gudikanti Narasimhulu v. Public Prosecutor, (1978) 1 SCC 240 —
        Denial of bail is deprivation of liberty and must be preceded by
        proper judicial application of mind.

7.  INTERLOCUTORY APPLICATION FOR STAY / INTERIM BAIL
    ────────────────────────────────────────────────────
    That pending hearing and final disposal of the present Special Leave
    Petition, it is prayed that this Hon'ble Court may be pleased to:
    (a) Grant interim bail to the Petitioner on appropriate terms; or
    (b) Issue notice to the Respondents; and
    (c) Stay the operation of the impugned order dated {high_court_order_date}.

8.  MAIN PRAYER
    ─────────────
    In view of the foregoing facts and submissions, it is most respectfully
    prayed that this Hon'ble Court may be pleased to:

    (a) GRANT Special Leave to Appeal against the impugned order dated
        {high_court_order_date} passed by the Hon'ble High Court of
        {high_court_bench};

    (b) Upon grant of leave, ALLOW the appeal and SET ASIDE the impugned
        order;

    (c) GRANT bail to the Petitioner, {accused_name}, in connection with
        FIR No. {fir_number}, {police_station}, {district}, under
        {sections_str}, on such terms and conditions as this Hon'ble
        Court may deem fit and proper;

    (d) PASS such other and further order(s) as this Hon'ble Court may
        deem fit and proper in the facts and circumstances of the case.

                                        AND FOR THIS ACT OF KINDNESS,
                                        THE PETITIONER SHALL EVER PRAY.

--------------------------------------------------------------------------------
Drawn by    : {advocate_name}
Filed by    : Advocate-on-Record, Supreme Court of India
              AOR Enrolment No. : ___________________
Date        : {_today()}
--------------------------------------------------------------------------------

VERIFICATION:

I, {accused_name}, the Petitioner above-named, do hereby solemnly verify
and declare that the contents of the above Special Leave Petition are true
and correct to the best of my knowledge and belief. No material fact has
been concealed or misstated therefrom.

Verified at New Delhi on this {_today()}.

                                        ____________________________________
                                        PETITIONER
================================================================================
                        [CASE REFERENCE: {case_id}]
                   [GENERATED BY AI LEGAL DRAFTING ASSISTANT]
================================================================================
"""
    return draft.strip()


# --------------------------------------------------
# MASTER ENTRY POINT — called by main.py endpoint
# --------------------------------------------------

def generate_bail_draft(
    court_level: str,
    case_id: str,
    facts: Dict,
    loopholes: List[Dict],
    additional_params: Optional[Dict] = None
) -> str:
    """
    Master function called by /api/v1/generate-draft endpoint.

    Parameters
    ----------
    court_level : "sessions" | "high_court" | "supreme_court"
    case_id     : Unique case reference ID
    facts       : extracted_facts dict from Module 2
    loopholes   : detected_loopholes list from Module 4
    additional_params : Optional dict for court-specific fields
    """
    p = additional_params or {}

    accused_name   = facts.get("accused_name", "The Accused")
    offence        = facts.get("offence", facts.get("raw_extracted_text", "As per FIR")[:120])
    sections       = facts.get("sections_applied", facts.get("offence_sections", []))
    arrest_date    = facts.get("arrest_date_time")
    mag_time       = facts.get("magistrate_presentation_time")
    evidence       = facts.get("evidentiary_items", [])
    witnesses      = facts.get("witness_statements", [])

    if court_level == "sessions":
        return generate_sessions_court_draft(
            case_id=case_id,
            accused_name=accused_name,
            offence=offence,
            sections_applied=sections,
            arrest_date=arrest_date,
            magistrate_presentation_time=mag_time,
            evidentiary_items=evidence,
            witness_statements=witnesses,
            loopholes=loopholes,
            fir_number=p.get("fir_number", "As per records"),
            police_station=p.get("police_station", "Concerned Police Station"),
            district=p.get("district", "Concerned District"),
            advocate_name=p.get("advocate_name", "Counsel for the Applicant"),
            state=p.get("state", "State")
        )

    elif court_level == "high_court":
        return generate_high_court_draft(
            case_id=case_id,
            accused_name=accused_name,
            offence=offence,
            sections_applied=sections,
            arrest_date=arrest_date,
            magistrate_presentation_time=mag_time,
            evidentiary_items=evidence,
            witness_statements=witnesses,
            loopholes=loopholes,
            fir_number=p.get("fir_number", "As per records"),
            police_station=p.get("police_station", "Concerned Police Station"),
            district=p.get("district", "Concerned District"),
            sessions_court_order_date=p.get("sessions_court_order_date", "As per records"),
            advocate_name=p.get("advocate_name", "Counsel for the Applicant"),
            high_court_bench=p.get("high_court_bench", "Concerned Bench"),
            state=p.get("state", "State")
        )

    elif court_level == "supreme_court":
        return generate_supreme_court_draft(
            case_id=case_id,
            accused_name=accused_name,
            offence=offence,
            sections_applied=sections,
            arrest_date=arrest_date,
            magistrate_presentation_time=mag_time,
            evidentiary_items=evidence,
            witness_statements=witnesses,
            loopholes=loopholes,
            fir_number=p.get("fir_number", "As per records"),
            police_station=p.get("police_station", "Concerned Police Station"),
            district=p.get("district", "Concerned District"),
            high_court_order_date=p.get("high_court_order_date", "As per records"),
            high_court_bench=p.get("high_court_bench", "Concerned High Court"),
            advocate_name=p.get("advocate_name", "Counsel for the Petitioner"),
            state=p.get("state", "State")
        )

    else:
        raise ValueError(f"Invalid court_level '{court_level}'. Choose: sessions | high_court | supreme_court")