from __future__ import annotations
import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from app.config import settings


class ReportService:
    """Generates professional, styled PDF analysis reports using ReportLab."""

    def __init__(self, reports_dir: Path | None = None):
        self._reports_dir = reports_dir

    @property
    def reports_dir(self) -> Path:
        p = self._reports_dir or settings.REPORTS_DIR
        try:
            p.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        return p


    def generate_pdf_report(self, analysis_data: dict) -> Path:
        """
        Generate a comprehensive PDF evaluation report for a given analysis record.
        Returns the Path to the generated PDF.
        """
        analysis_id = analysis_data.get("id", "preview")
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"Resume_Analysis_Report_{analysis_id}_{timestamp}.pdf"
        report_path = self.reports_dir / filename

        doc = SimpleDocTemplate(
            str(report_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()

        # Custom typography styles
        primary_color = colors.HexColor("#1e3a8a")  # Deep blue
        accent_color = colors.HexColor("#0284c7")   # Sky blue
        text_dark = colors.HexColor("#1f2937")      # Slate 800
        light_bg = colors.HexColor("#f8fafc")       # Slate 50
        border_color = colors.HexColor("#e2e8f0")   # Slate 200
        success_color = colors.HexColor("#16a34a")  # Green 600
        warning_color = colors.HexColor("#ea580c")  # Orange 600

        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=22,
            leading=26,
            textColor=primary_color,
            fontName="Helvetica-Bold",
        )
        subtitle_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#64748b"),
        )
        section_heading_style = ParagraphStyle(
            "SecHeading",
            parent=styles["Heading2"],
            fontSize=13,
            leading=17,
            textColor=primary_color,
            fontName="Helvetica-Bold",
            spaceBefore=10,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontSize=9,
            leading=13,
            textColor=text_dark,
        )
        body_bold = ParagraphStyle(
            "BodyBold",
            parent=body_style,
            fontName="Helvetica-Bold",
        )

        story = []

        # 1. Header & Title
        story.append(Paragraph("AI RESUME ANALYZER", title_style))
        story.append(Paragraph("Automated ATS Evaluation & Job Matching Report | B.Tech Mini Project", subtitle_style))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=12))

        # 2. Candidate & Job Metadata
        info = analysis_data.get("extracted_info") or {}
        job_title = analysis_data.get("job_title", "Target Job")
        created_at = analysis_data.get("created_at", datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

        meta_data = [
            [
                Paragraph("<b>Candidate Name:</b> " + info.get("name", "Not detected"), body_style),
                Paragraph("<b>Target Role:</b> " + job_title, body_style),
            ],
            [
                Paragraph("<b>Email:</b> " + info.get("email", "Not detected"), body_style),
                Paragraph("<b>Degree:</b> " + info.get("degree", "Not detected"), body_style),
            ],
            [
                Paragraph("<b>Phone:</b> " + info.get("phone", "Not detected"), body_style),
                Paragraph("<b>Date of Analysis:</b> " + str(created_at)[:19], body_style),
            ],
        ]
        meta_table = Table(meta_data, colWidths=[270, 270])
        meta_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), light_bg),
            ("BOX", (0, 0), (-1, -1), 1, border_color),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 12))

        # 3. Overall Compatibility Scores
        story.append(Paragraph("Core Evaluation Scores", section_heading_style))

        ats_score = analysis_data.get("ats_score", 0.0)
        resume_score = analysis_data.get("resume_score", 0.0)
        skill_match = analysis_data.get("skill_match_score", 0.0)
        keyword_score = analysis_data.get("keyword_score", 0.0)
        semantic_score = analysis_data.get("semantic_score", 0.0)

        score_data = [
            [
                Paragraph("<b>ATS Compatibility</b><br/><font size='16' color='#1e3a8a'><b>" + str(ats_score) + "%</b></font>", body_style),
                Paragraph("<b>Resume Quality</b><br/><font size='16' color='#0284c7'><b>" + str(resume_score) + "/100</b></font>", body_style),
                Paragraph("<b>Skill Match</b><br/><font size='16' color='#16a34a'><b>" + str(skill_match) + "%</b></font>", body_style),
                Paragraph("<b>Keyword Match</b><br/><font size='16' color='#ea580c'><b>" + str(keyword_score) + "%</b></font>", body_style),
            ]
        ]
        score_table = Table(score_data, colWidths=[135, 135, 135, 135])
        score_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            "<font size='8' color='#64748b'><b>ATS Calculation Formula:</b> ATS Score = 50% Semantic (TF-IDF Cosine: " +
            str(semantic_score) + "%) + 30% Skill Match (" + str(skill_match) + "%) + 20% Keyword Coverage (" +
            str(keyword_score) + "%)</font>",
            body_style
        ))
        story.append(Spacer(1, 12))

        # 4. Matched and Missing Skills
        skills = analysis_data.get("skills", [])
        matched = [s["skill_name"] if isinstance(s, dict) else s.skill_name for s in skills if (isinstance(s, dict) and s.get("status") == "matched") or (hasattr(s, "status") and s.status == "matched")]
        missing = [s["skill_name"] if isinstance(s, dict) else s.skill_name for s in skills if (isinstance(s, dict) and s.get("status") == "missing") or (hasattr(s, "status") and s.status == "missing")]

        story.append(Paragraph("Skills Comparison (Resume vs. Job Description)", section_heading_style))
        skills_table_data = [
            [
                Paragraph("<b>Matched Skills (" + str(len(matched)) + ")</b>", body_bold),
                Paragraph("<b>Missing Skills in Resume (" + str(len(missing)) + ")</b>", body_bold),
            ],
            [
                Paragraph(", ".join(matched) if matched else "None explicitly matched", body_style),
                Paragraph(", ".join(missing) if missing else "None missing! All required skills detected.", body_style),
            ],
        ]
        skills_table = Table(skills_table_data, colWidths=[270, 270])
        skills_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
            ("BOX", (0, 0), (-1, -1), 1, border_color),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(skills_table)
        story.append(Spacer(1, 12))

        # 5. Resume Sections Checklist
        story.append(Paragraph("Resume Section Verification", section_heading_style))
        sections = analysis_data.get("detected_sections") or {}
        sec_rows = []
        sec_items = list(sections.items())
        # 2 columns of sections
        for i in range(0, len(sec_items), 2):
            sec1, pres1 = sec_items[i]
            col1 = f"<b>{sec1}:</b> <font color='{'#16a34a' if pres1 else '#dc2626'}'>{'[Present]' if pres1 else '[Missing]'}</font>"
            col2 = ""
            if i + 1 < len(sec_items):
                sec2, pres2 = sec_items[i + 1]
                col2 = f"<b>{sec2}:</b> <font color='{'#16a34a' if pres2 else '#dc2626'}'>{'[Present]' if pres2 else '[Missing]'}</font>"
            sec_rows.append([Paragraph(col1, body_style), Paragraph(col2, body_style)])

        if sec_rows:
            sec_table = Table(sec_rows, colWidths=[270, 270])
            sec_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), light_bg),
                ("BOX", (0, 0), (-1, -1), 1, border_color),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]))
            story.append(sec_table)
            story.append(Spacer(1, 12))

        # 6. Job Role Recommendations
        story.append(Paragraph("Recommended Job Profiles", section_heading_style))
        recs = analysis_data.get("recommendations", [])
        rec_rows = [[
            Paragraph("<b>Recommended Role</b>", body_bold),
            Paragraph("<b>Fit Score</b>", body_bold),
            Paragraph("<b>Matched Skills</b>", body_bold),
        ]]
        for r in recs[:4]:
            r_role = r.get("job_role", "") if isinstance(r, dict) else r.job_role
            r_score = r.get("score", 0.0) if isinstance(r, dict) else r.score
            r_matched = r.get("matched_skills", []) if isinstance(r, dict) else r.matched_skills
            rec_rows.append([
                Paragraph(f"<b>{r_role}</b>", body_style),
                Paragraph(f"{r_score}%", body_style),
                Paragraph(", ".join(r_matched[:6]) if r_matched else "-", body_style),
            ])
        rec_table = Table(rec_rows, colWidths=[150, 70, 320])
        rec_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
            ("BOX", (0, 0), (-1, -1), 1, border_color),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(rec_table)
        story.append(Spacer(1, 12))

        # 7. Actionable Improvement Suggestions
        story.append(Paragraph("Resume Improvement Suggestions", section_heading_style))
        suggs = analysis_data.get("suggestions", [])
        for s in suggs:
            cat = s.get("category", "General") if isinstance(s, dict) else s.category
            text = s.get("suggestion", "") if isinstance(s, dict) else s.suggestion
            story.append(Paragraph(f"• <b>[{cat}]:</b> {text}", body_style))
            story.append(Spacer(1, 3))

        # Footer Notice
        story.append(Spacer(1, 15))
        story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#94a3b8"), spaceAfter=6))
        story.append(Paragraph(
            "<font size='7' color='#64748b'>Confidential Evaluation Report generated by AI Resume Analyzer (7th Semester B.Tech Project). "
            "This report is for educational and career improvement purposes and does not replace human hiring judgment.</font>",
            body_style
        ))

        doc.build(story)
        return report_path


report_service = ReportService()
