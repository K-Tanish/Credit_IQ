from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
import io
import os
from .narrative import narrative_engine

class ReportGenerator:
    """
    Pillar 5 Service: Generates the high-fidelity 'Ultimate Credit Report'.
    Synthesizes data from all 5 pillars into a professional memorandum.
    """

    def generate_credit_memo(self, analysis_data: dict, entity_data: dict) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
        styles = getSampleStyleSheet()
        
        # Custom Professional Styles
        styles.add(ParagraphStyle(name='Justify', parent=styles['Normal'], alignment=TA_JUSTIFY, fontSize=10, leading=14))
        styles.add(ParagraphStyle(name='SectionHeader', parent=styles['Heading2'], borderPadding=5, borderRadius=3, fontSize=14, spaceBefore=20, spaceAfter=10, textColor=colors.HexColor("#1e293b")))
        styles.add(ParagraphStyle(name='Verdict', parent=styles['Normal'], fontSize=11, leading=16, fontName='Helvetica-Bold', textColor=colors.HexColor("#0f172a")))
        styles.add(ParagraphStyle(name='Italic', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=9, textColor=colors.HexColor("#64748b")))

        elements = []

        # --- Header ---
        elements.append(Paragraph("CREDIT IQ | CAMS SYSTEM", styles['Code']))
        elements.append(Paragraph(f"ULTIMATE CREDIT INTELLIGENCE REPORT", styles['Title']))
        elements.append(Paragraph(f"Entity: {entity_data.get('company_name', 'Unknown Inc')}", styles['Heading3']))
        elements.append(Spacer(1, 12))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#64748b")))
        elements.append(Spacer(1, 24))

        # --- Section 1: Background ---
        elements.append(Paragraph("1. COMPANY BACKGROUND & PROFILE", styles['SectionHeader']))
        bg_text = narrative_engine.generate_background(entity_data)
        elements.append(Paragraph(bg_text, styles['Justify']))
        
        # Summary Table in background
        data = [
            ["Registration (CIN)", entity_data.get('cin')],
            ["Fiscal ID (PAN)", entity_data.get('pan')],
            ["Sector Benchmarking", entity_data.get('sector', 'General Manufacturing')],
            ["Loan Quantum Requested", f"Rs. {entity_data.get('loan_amount', 'N/A')}"]
        ]
        t = Table(data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#f8fafc")),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor("#64748b")),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
        ]))
        elements.append(Spacer(1, 12))
        elements.append(t)

        # --- Section 2: Quality Research ---
        elements.append(Paragraph("2. DEEP-DIVE TRIANGULATION RESEARCH", styles['SectionHeader']))
        res_text = narrative_engine.generate_research_summary(analysis_data.get('findings', []), analysis_data.get('docs', []))
        elements.append(Paragraph(res_text, styles['Justify']))
        
        # Findings sub-list
        elements.append(Spacer(1, 12))
        for f in analysis_data.get('findings', []):
            color = colors.red if f.get('severity') == 'HIGH' else colors.blue
            icon = "!" if f.get('severity') == 'HIGH' else "i"
            f_text = f"<b>[{icon}] {f.get('type')}:</b> {f.get('message')}"
            elements.append(Paragraph(f_text, styles['Justify']))
            elements.append(Spacer(1, 4))

        # --- Section 3: External Intelligence ---
        elements.append(Paragraph("3. EXTERNAL INTELLIGENCE & MARKET SENTIMENT", styles['SectionHeader']))
        ext_text = narrative_engine.generate_external_intelligence(analysis_data.get('external_intelligence', {}))
        elements.append(Paragraph(ext_text, styles['Justify']))

        # --- Section 4: Final Recommendation ---
        elements.append(Paragraph("4. FINAL VERDICT & PRIMARY CONCERNS", styles['SectionHeader']))
        ver_text = narrative_engine.generate_final_verdict(analysis_data.get('credit_score', 0), analysis_data.get('findings', []))
        
        # Highlight Box for verdict
        v_box_data = [[Paragraph(ver_text, styles['Verdict'])]]
        v_t = Table(v_box_data, colWidths=[450])
        v_color = colors.HexColor("#ecfdf5") if analysis_data.get('credit_score', 0) >= 70 else colors.HexColor("#fef2f2")
        v_t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), v_color),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0,0), (-1,-1), 15),
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            ('LEFTPADDING', (0,0), (-1,-1), 15),
            ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ]))
        elements.append(v_t)
        
        # Final Score Footer
        elements.append(Spacer(1, 24))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
        elements.append(Spacer(1, 12))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"FINAL CAMS RISK SCORE: {analysis_data.get('credit_score')} / 100", styles['Heading2']))
        elements.append(Paragraph("This document is generated by the Credit_IQ AI Engine and intended for secondary credit review purposes.", styles['Italic']))

        doc.build(elements)
        return buffer.getvalue()

report_service = ReportGenerator()
