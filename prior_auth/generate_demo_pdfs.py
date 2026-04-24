from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


def build_policy():
    doc = SimpleDocTemplate(
        "static/demo_policy.pdf",
        pagesize=letter,
        leftMargin=1*inch, rightMargin=1*inch,
        topMargin=1*inch, bottomMargin=1*inch,
    )
    styles = getSampleStyleSheet()

    def h(text, size=12, bold=True, color=colors.HexColor("#1e3a5f")):
        return Paragraph(text, ParagraphStyle(
            "h", parent=styles["Normal"],
            fontSize=size, leading=size*1.3,
            textColor=color,
            fontName="Helvetica-Bold" if bold else "Helvetica",
            spaceAfter=4,
        ))

    def body(text):
        return Paragraph(text, ParagraphStyle(
            "b", parent=styles["Normal"],
            fontSize=9.5, leading=14,
            textColor=colors.HexColor("#333333"),
            spaceAfter=6,
        ))

    def bullet(text):
        return Paragraph(f"• &nbsp; {text}", ParagraphStyle(
            "bullet", parent=styles["Normal"],
            fontSize=9.5, leading=14,
            leftIndent=18,
            textColor=colors.HexColor("#333333"),
            spaceAfter=4,
        ))

    story = []

    # Header block
    story.append(h("BLUECREST HEALTH INSURANCE", size=16))
    story.append(h("Prior Authorization Policy", size=13, color=colors.HexColor("#2563eb")))
    story.append(body("<b>Drug/Treatment:</b> Adalimumab (Humira) for Rheumatoid Arthritis"))
    story.append(body("<b>Policy Number:</b> BCH-PA-BIO-2024-017 &nbsp;&nbsp; <b>Effective Date:</b> January 1, 2024 &nbsp;&nbsp; <b>Review Date:</b> December 31, 2024"))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=12))

    story.append(h("1. OVERVIEW"))
    story.append(body(
        "BlueCrest Health Insurance requires prior authorization (PA) for all biologic disease-modifying "
        "antirheumatic drugs (bDMARDs), including adalimumab (Humira), for the treatment of rheumatoid "
        "arthritis (RA). Requests that do not meet ALL criteria listed below will be denied. "
        "Partial documentation is insufficient for approval."
    ))
    story.append(Spacer(1, 8))

    story.append(h("2. STEP THERAPY REQUIREMENTS (MANDATORY)"))
    story.append(body(
        "The member must have documented trial AND failure of BOTH of the following conventional "
        "DMARDs prior to biologic approval. Failure is defined as inadequate clinical response or "
        "documented intolerance requiring discontinuation."
    ))
    story.append(bullet("<b>Methotrexate (MTX):</b> Documented trial of at least 3 months (12 weeks) at a minimum dose of 15 mg/week. "
                        "Trials of shorter duration or sub-therapeutic doses do not satisfy this requirement. "
                        "Documentation must include start date, dose titration, and reason for discontinuation if applicable."))
    story.append(bullet("<b>Sulfasalazine (SSZ):</b> Documented trial of at least 3 months (12 weeks) at a minimum dose of 2,000 mg/day (2 g/day). "
                        "Must be documented in the medical record with prescribing dates and clinical response notes."))
    story.append(body(
        "<b>Note:</b> Both agents must be trialed. Failure of one agent alone does not satisfy step therapy. "
        "Contraindications must be documented by the treating specialist with supporting clinical rationale."
    ))
    story.append(Spacer(1, 8))

    story.append(h("3. CLINICAL CRITERIA"))
    story.append(body("ALL of the following must be documented at the time of the PA request:"))
    story.append(bullet("<b>DAS28 Score ≥ 3.2:</b> A Disease Activity Score 28 (DAS28) of 3.2 or greater must be recorded "
                        "in the medical record at the time of the authorization request. Qualitative descriptions such as "
                        "'significant joint involvement' or 'moderate disease activity' are NOT acceptable substitutes. "
                        "The numeric DAS28 value and date of assessment are required."))
    story.append(bullet("<b>Rheumatologist Evaluation Note:</b> A complete evaluation note from a board-certified or board-eligible "
                        "rheumatologist is required. A referral order, referral letter, or pending appointment does NOT satisfy "
                        "this requirement. The note must document history, physical examination, and treatment recommendations."))
    story.append(Spacer(1, 8))

    story.append(h("4. LABORATORY REQUIREMENTS"))
    story.append(body("The following labs must be current at the time of PA submission:"))
    story.append(bullet("<b>TB Screening:</b> QuantiFERON-TB Gold (QFT) or Tuberculin Skin Test (TST) result within the "
                        "preceding 6 months. Active TB must be ruled out before initiating biologic therapy. "
                        "If positive result, documentation of appropriate treatment or prophylaxis is required."))
    story.append(bullet("<b>Complete Blood Count (CBC):</b> CBC with differential within the preceding 3 months. "
                        "Significant cytopenias may require additional evaluation before approval is granted."))
    story.append(Spacer(1, 8))

    story.append(h("5. DIAGNOSIS CODE REQUIREMENTS"))
    story.append(body(
        "The ICD-10-CM diagnosis code submitted with the PA request must exactly match one of the following "
        "approved codes. Claims submitted with non-matching codes will be automatically denied."
    ))
    story.append(bullet("<b>M05.79</b> — Rheumatoid arthritis with rheumatoid factor, multiple sites"))
    story.append(bullet("<b>M06.09</b> — Rheumatoid arthritis without rheumatoid factor, multiple sites"))
    story.append(body(
        "<b>Important:</b> Codes such as M06.9 (Rheumatoid arthritis, unspecified) are NOT accepted. "
        "The specificity of site designation is required per BlueCrest billing policy."
    ))
    story.append(Spacer(1, 8))

    story.append(h("6. QUANTITY AND DURATION LIMITS"))
    story.append(bullet("<b>Initial Authorization:</b> 12 weeks only. Renewal requests require updated clinical documentation "
                        "including DAS28 reassessment and evidence of clinical response."))
    story.append(bullet("<b>Approved Dose:</b> Adalimumab 40 mg subcutaneous every 2 weeks (standard RA dosing per FDA label)."))
    story.append(bullet("<b>Quantity Limit:</b> 6 prefilled syringes or pens per 12-week authorization period."))
    story.append(Spacer(1, 8))

    story.append(h("7. SUBMISSION REQUIREMENTS"))
    story.append(body("Submit the following with the PA request form:"))
    story.append(bullet("Completed BlueCrest Prior Authorization Request Form (BCH-PA-01)"))
    story.append(bullet("Physician office notes documenting step therapy trials with dates and doses"))
    story.append(bullet("Rheumatologist evaluation note (must be signed and dated)"))
    story.append(bullet("Lab results (TB screening + CBC) with collection dates"))
    story.append(bullet("Documented DAS28 score with date of assessment"))
    story.append(Spacer(1, 8))

    story.append(h("8. APPEALS"))
    story.append(body(
        "Denied requests may be appealed within 60 days of denial. Appeals must include all missing "
        "documentation identified in the denial notice. Peer-to-peer review with a BlueCrest Medical "
        "Director is available within 5 business days of denial."
    ))

    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"), spaceAfter=6))
    story.append(Paragraph(
        "BlueCrest Health Insurance &nbsp;|&nbsp; Pharmacy Management &nbsp;|&nbsp; "
        "PA inquiries: 1-800-555-0192 &nbsp;|&nbsp; Fax: 1-800-555-0193",
        ParagraphStyle("footer", parent=styles["Normal"], fontSize=8, textColor=colors.HexColor("#888888"), alignment=TA_CENTER)
    ))

    doc.build(story)
    print("Generated static/demo_policy.pdf")


def build_record():
    doc = SimpleDocTemplate(
        "static/demo_record.pdf",
        pagesize=letter,
        leftMargin=1*inch, rightMargin=1*inch,
        topMargin=1*inch, bottomMargin=1*inch,
    )
    styles = getSampleStyleSheet()

    def h(text, size=11, color=colors.HexColor("#1e3a5f")):
        return Paragraph(text, ParagraphStyle(
            "h", parent=styles["Normal"],
            fontSize=size, leading=size*1.4,
            textColor=color,
            fontName="Helvetica-Bold",
            spaceAfter=4, spaceBefore=10,
        ))

    def label_value(label, value):
        return Paragraph(f"<b>{label}:</b> {value}", ParagraphStyle(
            "lv", parent=styles["Normal"],
            fontSize=9.5, leading=14,
            textColor=colors.HexColor("#222222"),
            spaceAfter=3,
        ))

    def body(text):
        return Paragraph(text, ParagraphStyle(
            "b", parent=styles["Normal"],
            fontSize=9.5, leading=15,
            textColor=colors.HexColor("#333333"),
            spaceAfter=5,
        ))

    story = []

    # Clinic header
    story.append(h("RIVERSIDE FAMILY CLINIC", size=14, color=colors.HexColor("#1e3a5f")))
    story.append(body("<b>4821 Riverside Drive, Suite 200 &nbsp;|&nbsp; Springfield, IL 62704</b>"))
    story.append(body("Tel: (217) 555-0184 &nbsp;|&nbsp; Fax: (217) 555-0185"))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a5f"), spaceAfter=8))

    story.append(h("CLINIC VISIT NOTE — SOAP FORMAT", size=12))

    # Patient demographics table
    demo_data = [
        [Paragraph("<b>Patient Name:</b> James Whitfield", styles["Normal"]),
         Paragraph("<b>DOB:</b> 03/14/1971 (Age: 53)", styles["Normal"])],
        [Paragraph("<b>MRN:</b> JW-4821", styles["Normal"]),
         Paragraph("<b>Insurance:</b> BlueCrest Health (ID: BCH-2291847)", styles["Normal"])],
        [Paragraph("<b>Date of Visit:</b> 11/07/2024", styles["Normal"]),
         Paragraph("<b>Provider:</b> Dr. Sarah Chen, MD", styles["Normal"])],
        [Paragraph("<b>Visit Type:</b> Follow-up — Rheumatology Referral", styles["Normal"]),
         Paragraph("<b>NPI:</b> 1245896357", styles["Normal"])],
    ]
    t = Table(demo_data, colWidths=[3.25*inch, 3.25*inch])
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # SUBJECTIVE
    story.append(h("SUBJECTIVE"))
    story.append(body(
        "Mr. Whitfield is a 53-year-old male presenting for follow-up of rheumatoid arthritis. "
        "He reports ongoing joint pain primarily affecting bilateral wrists, MCPs, and PIPs. "
        "He states pain is approximately 6/10, worsening with activity and morning stiffness lasting "
        "approximately 90 minutes. Patient reports significant difficulty with fine motor tasks at work."
    ))
    story.append(body(
        "Medications reviewed: Patient was trialed on methotrexate starting approximately 10 weeks ago "
        "at 12.5 mg/week. Trial was discontinued at week 10 due to persistent nausea and GI intolerance. "
        "No sulfasalazine has been prescribed or discussed previously."
    ))
    story.append(body(
        "Patient is requesting initiation of biologic therapy to better control disease activity. "
        "He has been referred to rheumatology but has not yet been seen — appointment is pending."
    ))

    # OBJECTIVE
    story.append(h("OBJECTIVE"))
    story.append(label_value("Vital Signs", "BP 128/82, HR 74, Temp 98.6°F, Weight 184 lbs"))
    story.append(label_value("General", "Alert and oriented, no acute distress"))
    story.append(label_value("Musculoskeletal",
        "Bilateral wrist tenderness to palpation. Swelling noted at 2nd and 3rd MCPs bilaterally. "
        "Grip strength reduced bilaterally. Significant joint involvement observed. "
        "No DAS28 assessment performed this visit."))
    story.append(label_value("Skin", "No rash, nodules, or tophi"))
    story.append(label_value("Labs",
        "CMP within normal limits (drawn 08/15/2024). CBC not repeated this visit. "
        "No TB screening documented in chart."))

    # ASSESSMENT
    story.append(h("ASSESSMENT"))
    story.append(label_value("Primary Diagnosis", "Rheumatoid arthritis, unspecified — ICD-10: M06.9"))
    story.append(body(
        "Patient has confirmed rheumatoid arthritis with ongoing moderate-to-severe disease activity "
        "despite trial of conventional DMARD therapy. Methotrexate was not tolerated due to GI side effects. "
        "Patient has not yet completed sulfasalazine trial. Disease course appears progressive."
    ))

    # PLAN
    story.append(h("PLAN"))
    story.append(body(
        "1. <b>Biologic initiation:</b> Will initiate adalimumab (Humira) 40 mg subcutaneous every 2 weeks "
        "given failure of conventional DMARD therapy. Submitting prior authorization to BlueCrest Health."
    ))
    story.append(body(
        "2. <b>Rheumatology referral:</b> Referral placed to Dr. Marcus Okafor, Rheumatology Associates, "
        "Springfield. Appointment expected within 6–8 weeks."
    ))
    story.append(body(
        "3. <b>Monitoring:</b> Patient instructed on self-injection technique. Follow up in 12 weeks "
        "to assess response. Will repeat LFTs at that time."
    ))
    story.append(body(
        "4. <b>Patient education:</b> Discussed risks and benefits of biologic therapy including infection risk. "
        "Patient verbalized understanding and provided written consent."
    ))

    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"), spaceAfter=6))
    story.append(body(
        "<b>Electronically signed by:</b> Sarah Chen, MD &nbsp;|&nbsp; "
        "<b>Date:</b> 11/07/2024 &nbsp;|&nbsp; <b>Time:</b> 2:47 PM"
    ))
    story.append(Paragraph(
        "This document is confidential and intended solely for the named recipient. "
        "Unauthorized disclosure is prohibited under HIPAA.",
        ParagraphStyle("footer", parent=styles["Normal"], fontSize=7.5,
                       textColor=colors.HexColor("#999999"), alignment=TA_CENTER)
    ))

    doc.build(story)
    print("Generated static/demo_record.pdf")


if __name__ == "__main__":
    build_policy()
    build_record()
