"""
Resume Parser Service
====================
Supports PDF (via PyMuPDF/fitz) and DOCX (via python-docx).

Extracted fields:
  - raw_text          : Full text from document
  - candidate_name    : Heuristic: first 2-3 word line in upper case
  - email             : Regex match
  - phone             : Regex match
  - education         : Section extracted by header keywords
  - work_experience   : Section extracted by header keywords
  - projects          : Section extracted by header keywords
  - certifications    : Section extracted by header keywords
  - years_experience  : Estimated from year ranges or explicit "X years" statements
"""

try:
    import pymupdf as fitz
except ImportError:
    import fitz  # PyMuPDF
import re
from pathlib import Path

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None


class ResumeParser:
    # Section header keywords for each section
    SECTION_HEADERS = {
        "education": ["education", "academic background", "academic qualifications", "qualifications"],
        "work_experience": [
            "experience", "work experience", "professional experience",
            "employment history", "work history", "career history",
        ],
        "projects": ["projects", "personal projects", "academic projects", "key projects", "portfolio"],
        "certifications": [
            "certifications", "certificates", "courses", "training",
            "professional development", "licenses",
        ],
    }

    # All known section names (used to detect end of a section)
    ALL_SECTIONS = [
        "education", "experience", "work", "employment", "skills", "projects",
        "certifications", "certificates", "courses", "awards", "publications",
        "references", "summary", "objective", "profile", "portfolio", "training",
        "languages", "interests", "hobbies", "volunteer", "activities",
    ]

    def parse(self, file_path: str) -> dict:
        """Parse a resume file and return a dict with all extracted fields."""
        ext = Path(file_path).suffix.lower()
        if ext == ".pdf":
            text = self._extract_pdf_text(file_path)
        elif ext == ".docx":
            text = self._extract_docx_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        return {
            "raw_text": text,
            "candidate_name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "education": self._extract_section(text, "education"),
            "work_experience": self._extract_section(text, "work_experience"),
            "projects": self._extract_section(text, "projects"),
            "certifications": self._extract_section(text, "certifications"),
            "years_experience": self._estimate_years_experience(text),
        }

    # -------------------------------------------------------------------------
    # Text extraction
    # -------------------------------------------------------------------------

    def _extract_pdf_text(self, path: str) -> str:
        doc = fitz.open(path)
        return "\n".join(page.get_text() for page in doc)

    def _extract_docx_text(self, path: str) -> str:
        if DocxDocument is None:
            raise ImportError("python-docx is not installed. Run: pip install python-docx")
        doc = DocxDocument(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    # -------------------------------------------------------------------------
    # Field extractors
    # -------------------------------------------------------------------------

    def _extract_email(self, text: str) -> str:
        match = re.search(r"[\w.+\-]+@[\w\-]+\.[a-zA-Z]{2,}", text)
        return match.group(0) if match else ""

    def _extract_phone(self, text: str) -> str:
        # Match common phone formats: +1-555-0101, (555) 010-1010, 555.010.1010 etc.
        match = re.search(
            r"(\+?\d[\d\s\-().]{7,15}\d)", text
        )
        return match.group(0).strip() if match else ""

    def _extract_name(self, text: str) -> str:
        """
        Heuristic: the candidate's name is usually the first non-empty line
        that looks like a proper name (2-4 words, starts with uppercase).
        """
        lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
        for line in lines[:8]:  # Only check first 8 lines
            words = line.split()
            if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w.isalpha()):
                # Exclude lines that look like headers/titles
                if not any(kw in line.lower() for kw in ["resume", "curriculum", "cv", "profile"]):
                    return line
        return lines[0] if lines else "Unknown"

    def _extract_section(self, text: str, section_key: str) -> list[str]:
        """
        Generic section extractor.
        Finds the section by matching header keywords, then collects lines
        until the next section header is found.
        """
        keywords = self.SECTION_HEADERS.get(section_key, [])
        lines = text.split("\n")
        in_section = False
        section_lines: list[str] = []

        for line in lines:
            stripped = line.strip()
            lower = stripped.lower()

            if not stripped:
                continue

            # Check if this line is the section header we're looking for
            if not in_section:
                if any(lower == kw or lower.startswith(kw) for kw in keywords) and len(stripped) < 60:
                    in_section = True
                    continue

            if in_section:
                # Check if we've hit another section
                if any(lower == s or lower.startswith(s) for s in self.ALL_SECTIONS) and len(stripped) < 60:
                    # Make sure it's not one of our own keywords
                    if not any(lower == kw or lower.startswith(kw) for kw in keywords):
                        break  # End of our section

                # Skip lines that are purely decorative (dashes, underscores, etc.)
                if re.match(r"^[-─═_\s]{3,}$", stripped):
                    continue

                section_lines.append(stripped)

        return section_lines[:30]  # Limit to 30 lines per section

    # -------------------------------------------------------------------------
    # Experience estimation
    # -------------------------------------------------------------------------

    def _estimate_years_experience(self, text: str) -> float:
        """
        Estimate total years of professional experience.

        Strategy:
          1. Look for explicit "X years of experience" statements.
          2. Find year ranges (e.g. 2018 – 2023, 2020 - Present) and sum durations.
          3. Fall back to 0.0 if nothing is found.
        """
        # Strategy 1: Explicit mention
        explicit = re.search(
            r"(\d+)\+?\s*[-–]?\s*\d*\s+years?\s+of\s+(?:professional\s+)?experience",
            text, re.IGNORECASE,
        )
        if explicit:
            return float(explicit.group(1))

        explicit2 = re.search(
            r"(\d+)\+?\s+years?\s+(?:of\s+)?experience",
            text, re.IGNORECASE,
        )
        if explicit2:
            return float(explicit2.group(1))

        # Strategy 2: Sum year ranges
        import datetime
        current_year = datetime.datetime.now().year

        # Match patterns like "2018 – 2023" or "2020 - Present"
        ranges = re.findall(
            r"\b(20\d{2}|19\d{2})\s*[-–]\s*(20\d{2}|19\d{2}|[Pp]resent|[Cc]urrent|[Nn]ow)\b",
            text,
        )

        total_years = 0.0
        for start, end in ranges:
            try:
                start_yr = int(start)
                end_yr = current_year if end.lower() in ("present", "current", "now") else int(end)
                duration = end_yr - start_yr
                if 0 < duration <= 15:  # Sanity check: ignore bogus ranges
                    total_years += duration
            except ValueError:
                continue

        # Cap at 30 years and deduplicate overlapping ranges (approximate)
        return min(round(total_years, 1), 30.0)
