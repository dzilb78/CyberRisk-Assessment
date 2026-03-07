# report_generator.py

# Cybersecurity Risk Assessment Tool
# Copyright (c) 2026 David Zilberman
# Licensed under the MIT License

import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate_report(company, industry, total, categories, ai_advice=""):

    saved_reports_dir = os.path.join(os.path.dirname(__file__), "Saved Reports")
    os.makedirs(saved_reports_dir, exist_ok=True)

    filename = os.path.join(
    saved_reports_dir,
    f"{company}_cyber_report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
)
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    # -------------------------
    # COLORS
    # -------------------------
    PRIMARY     = colors.HexColor("#0d6efd")
    DARK        = colors.HexColor("#1e1e2e")
    LIGHT_GREY  = colors.HexColor("#f0f2f5")
    WHITE       = colors.white
    GREEN       = colors.HexColor("#198754")
    YELLOW      = colors.HexColor("#ffc107")
    RED         = colors.HexColor("#dc3545")

    # -------------------------
    # STYLES
    # -------------------------
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        fontSize=28,
        fontName="Helvetica-Bold",
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        fontSize=13,
        fontName="Helvetica",
        textColor=colors.HexColor("#ccddff"),
        alignment=TA_CENTER,
        spaceAfter=4
    )

    section_style = ParagraphStyle(
        "Section",
        fontSize=14,
        fontName="Helvetica-Bold",
        textColor=PRIMARY,
        spaceBefore=16,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "Body",
        fontSize=11,
        fontName="Helvetica",
        textColor=DARK,
        spaceAfter=4
    )

    # -------------------------
    # RISK COLOR
    # -------------------------
    if total < 50:
        risk_label = "Low"
        risk_color = GREEN
    elif total < 100:
        risk_label = "Moderate"
        risk_color = YELLOW
    else:
        risk_label = "High"
        risk_color = RED

    # -------------------------
    # BUILD PDF
    # -------------------------
    elements = []

    # Header banner
    header_data = [[
        Paragraph("CyberRisk Assessment Report", title_style),
    ]]
    header_table = Table(header_data, colWidths=[7 * inch])
    header_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, -1), DARK),
    ("ROUNDEDCORNERS",[10]),
    ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING",    (0, 0), (-1, -1), 24),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 24),
    ("LEFTPADDING",   (0, 0), (-1, -1), 20),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
]))
    elements.append(header_table)
    elements.append(Spacer(1, 20))

    # Company info table
    info_data = [
        ["Company", company],
        ["Industry", industry],
        ["Report Date", datetime.datetime.now().strftime("%B %d, %Y")],
    ]
    info_table = Table(info_data, colWidths=[2 * inch, 5 * inch])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), PRIMARY),
        ("BACKGROUND", (1, 0), (1, -1), LIGHT_GREY),
        ("TEXTCOLOR", (0, 0), (0, -1), WHITE),
        ("TEXTCOLOR", (1, 0), (1, -1), DARK),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dee2e6")),
        ("ROUNDEDCORNERS", [6]),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # Risk score banner
    risk_data = [[
        Paragraph(f"Overall Risk Score: {round(total, 2)}", ParagraphStyle(
            "Risk", fontSize=18, fontName="Helvetica-Bold",
            textColor=WHITE, alignment=TA_CENTER
        )),
        Paragraph(f"Risk Level: {risk_label}", ParagraphStyle(
            "RiskLabel", fontSize=18, fontName="Helvetica-Bold",
            textColor=WHITE, alignment=TA_CENTER
        ))
    ]]
    risk_table = Table(risk_data, colWidths=[3.5 * inch, 3.5 * inch])
    risk_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), PRIMARY),
        ("BACKGROUND", (1, 0), (1, 0), risk_color),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("ROUNDEDCORNERS", [8]),
    ]))
    elements.append(risk_table)
    elements.append(Spacer(1, 24))

    # Category breakdown section
    elements.append(Paragraph("Category Breakdown", section_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=10))

    cat_header = [["Category", "Score", "Risk Level"]]
    cat_data = []
    for cat, score in categories.items():
        if score < 50:
            level = "Low"
        elif score < 100:
            level = "Moderate"
        else:
            level = "High"
        cat_data.append([cat, str(round(score, 2)), level])

    cat_table = Table(cat_header + cat_data, colWidths=[3 * inch, 2 * inch, 2 * inch])
    cat_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GREY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dee2e6")),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
    ]))
    elements.append(cat_table)
    elements.append(Spacer(1, 24))

    # Risk scale reference
    elements.append(Paragraph("Risk Scale Reference", section_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=10))

    scale_data = [["Low Risk", "Moderate Risk", "High Risk"],
                  ["0 – 49",   "50 – 99",        "100+"]]
    scale_table = Table(scale_data, colWidths=[2.33 * inch, 2.33 * inch, 2.33 * inch])
    scale_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), GREEN),
        ("BACKGROUND", (1, 0), (1, -1), YELLOW),
        ("BACKGROUND", (2, 0), (2, -1), RED),
        ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
        ("TEXTCOLOR", (1, 0), (1, -1), DARK),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("ROUNDEDCORNERS", [6]),
    ]))
    elements.append(scale_table)
    elements.append(Spacer(1, 24))

    # AI Advice section
    if ai_advice:
        elements.append(Paragraph("AI Security Advice", section_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=10))

        # Clean any markdown bold (**text**) from AI response
        import re
        ai_advice_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', ai_advice)
        ai_advice_clean = re.sub(r'\*(.*?)\*', r'\1', ai_advice_clean)

        for paragraph in ai_advice_clean.split("\n"):
            if paragraph.strip():
                elements.append(Paragraph(paragraph.strip(), ParagraphStyle(
                    "AIBody",
                    fontSize=10,
                    fontName="Helvetica",
                    textColor=DARK,
                    spaceAfter=6,
                    leading=14
                )))
        elements.append(Spacer(1, 24))

    # Footer disclaimer
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dee2e6"), spaceAfter=10))
    elements.append(Paragraph(
        "Disclaimer: This report provides educational cybersecurity guidance based on public frameworks "
        "such as NIST and CIS. Results should not replace professional cybersecurity consultation.",
        ParagraphStyle("Footer", fontSize=9, fontName="Helvetica",
                       textColor=colors.HexColor("#6c757d"), alignment=TA_CENTER)
    ))

    doc.build(elements)
    return filename