"""
Report Generator Service
========================
Generates downloadable reports in two formats:
  1. CSV  — ranking table for all candidates
  2. PDF  — single-candidate detailed analysis report (using ReportLab)
"""

import csv
import io
from typing import List, Dict, Any

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle,
        Paragraph, Spacer, HRFlowable,
    )
    _REPORTLAB_AVAILABLE = True
except ImportError:
    _REPORTLAB_AVAILABLE = False


class ReportGenerator:

    # -------------------------------------------------------------------------
    # CSV Export
    # -------------------------------------------------------------------------

    def generate_csv(self, candidates: List[Dict[str, Any]]) -> str:
        """
        Generate a CSV string for the candidate ranking table.

        Args:
            candidates: List of candidate dicts (with flat fields).

        Returns:
            CSV content as a string.
        """
        output = io.StringIO()
        fieldnames = [
            "rank", "candidate_name", "email", "phone",
            "years_experience", "final_score", "semantic_score",
            "skill_score", "experience_score", "education_score",
            "recommendation", "matched_skills", "missing_skills",
        ]

        writer = csv.DictWriter(
            output, fieldnames=fieldnames, extrasaction="ignore"
        )
        writer.writeheader()

        for c in candidates:
            row = {k: c.get(k, "") for k in fieldnames}
            # Serialise list fields to comma-separated strings
            for list_field in ("matched_skills", "missing_skills"):
                val = row.get(list_field, [])
                if isinstance(val, list):
                    row[list_field] = ", ".join(val)
            writer.writerow(row)

        return output.getvalue()

    # -------------------------------------------------------------------------
    # PDF Export
    # -------------------------------------------------------------------------

    def generate_pdf(self, candidate: Dict[str, Any]) -> bytes:
        """
        Generate a PDF analysis report for a single candidate.

        Args:
            candidate: Dict with all candidate fields.

        Returns:
            Raw PDF bytes.
        """
        if not _REPORTLAB_AVAILABLE:
            raise ImportError(
                "reportlab is not installed. Run: pip install reportlab"
            )

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
            leftMargin=1 * inch,
            rightMargin=1 * inch,
        )
        styles = getSampleStyleSheet()
        story = []

        NAVY = colors.HexColor("#1e3a5f")
        LIGHT_BLUE = colors.HexColor("#e8f4fd")

        # --- Title ---
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Title"],
            fontSize=22,
            textColor=NAVY,
            spaceAfter=4,
        )
        story.append(Paragraph("ResumeAI – Candidate Analysis Report", title_style))
        story.append(HRFlowable(width="100%", thickness=2, color=NAVY))
        story.append(Spacer(1, 0.2 * inch))

        # --- Candidate header ---
        story.append(
            Paragraph(
                f"<b>Candidate:</b> {candidate.get('candidate_name', 'N/A')}",
                styles["Heading1"],
            )
        )
        for label, key in [("Email", "email"), ("Phone", "phone")]:
            val = candidate.get(key) or "N/A"
            story.append(Paragraph(f"<b>{label}:</b> {val}", styles["Normal"]))
        story.append(
            Paragraph(
                f"<b>Experience:</b> {candidate.get('years_experience', 0):.1f} years",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 0.2 * inch))

        # --- Score summary table ---
        story.append(Paragraph("Score Breakdown", styles["Heading2"]))
        s = candidate
        score_data = [
            ["Component", "Score", "Weight", "Weighted Score"],
            ["Semantic Similarity",
             f"{s.get('semantic_score', 0):.1f}%", "40%",
             f"{s.get('semantic_score', 0) * 0.40:.1f}%"],
            ["Technical Skill Match",
             f"{s.get('skill_score', 0):.1f}%", "35%",
             f"{s.get('skill_score', 0) * 0.35:.1f}%"],
            ["Experience Match",
             f"{s.get('experience_score', 0):.1f}%", "15%",
             f"{s.get('experience_score', 0) * 0.15:.1f}%"],
            ["Education Match",
             f"{s.get('education_score', 0):.1f}%", "10%",
             f"{s.get('education_score', 0) * 0.10:.1f}%"],
            ["FINAL SCORE",
             f"{s.get('final_score', 0):.1f}%", "100%",
             f"{s.get('final_score', 0):.1f}%"],
        ]
        tbl = Table(
            score_data,
            colWidths=[2.5 * inch, 1.3 * inch, 0.9 * inch, 1.5 * inch],
        )
        tbl.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BACKGROUND", (0, -1), (-1, -1), LIGHT_BLUE),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -2),
                    [colors.white, colors.HexColor("#f8f9fa")],
                ),
            ])
        )
        story.append(tbl)
        story.append(Spacer(1, 0.2 * inch))

        # --- Recommendation ---
        rec = candidate.get("recommendation", "N/A")
        rec_style = ParagraphStyle(
            "Rec", parent=styles["Normal"], fontSize=13, textColor=NAVY
        )
        story.append(Paragraph(f"<b>Overall Recommendation:</b> {rec}", rec_style))
        story.append(Spacer(1, 0.15 * inch))

        # --- Skills ---
        story.append(Paragraph("Skill Analysis", styles["Heading2"]))
        for label, key in [
            ("Matched Skills", "matched_skills"),
            ("Missing Required Skills", "missing_skills"),
            ("Additional Skills", "additional_skills"),
        ]:
            skills = candidate.get(key, [])
            skills_str = ", ".join(skills) if skills else "None"
            story.append(
                Paragraph(f"<b>{label}:</b> {skills_str}", styles["Normal"])
            )
        story.append(Spacer(1, 0.2 * inch))

        # --- Disclaimer ---
        disclaimer_style = ParagraphStyle(
            "Disclaimer",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.grey,
        )
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
        story.append(Spacer(1, 0.1 * inch))
        story.append(
            Paragraph(
                "⚠ This report is a prototype AI screening indicator generated by ResumeAI. "
                "All scores are computed algorithmically from resume content. "
                "Human review is always required before making hiring decisions.",
                disclaimer_style,
            )
        )

        doc.build(story)
        buffer.seek(0)
        return buffer.read()
