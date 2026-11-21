"""
Experience Analyzer Service
============================
Compares a candidate's years of experience against the required years
specified in the job description.

Scoring logic:
  - If no experience is required: score = 1.0 (full marks)
  - If candidate meets or exceeds requirement: score = 1.0
  - If candidate is below requirement: score = candidate_years / required_years
    (proportional, never negative)
"""

import re


class ExperienceAnalyzer:

    def compute_score(self, candidate_years: float, required_years: float) -> float:
        """
        Return a normalised experience score between 0.0 and 1.0.

        Args:
            candidate_years: Years of experience the candidate has.
            required_years:  Years required by the job description.
        """
        if required_years <= 0:
            return 1.0  # No requirement → full score
        if candidate_years >= required_years:
            return 1.0  # Meets or exceeds requirement
        if candidate_years <= 0:
            return 0.1  # Has zero experience but slight credit for showing up
        return round(candidate_years / required_years, 4)

    def parse_required_experience(self, jd_text: str) -> float:
        """
        Extract the required years of experience from job description text.

        Handles patterns like:
          - "5+ years of experience"
          - "3 to 5 years of experience"
          - "minimum 3 years"
          - "at least 2 years"
        """
        patterns = [
            # Range: "3–5 years" or "3 to 5 years"
            r"(\d+)\s*[-–to]+\s*(\d+)\s+years?\s+of\s+(?:professional\s+)?experience",
            # Simple: "5+ years of experience"
            r"(\d+)\+?\s+years?\s+of\s+(?:professional\s+)?experience",
            # Simple: "5 years experience"
            r"(\d+)\+?\s+years?\s+experience",
            # "minimum X years"
            r"minimum\s+(\d+)\s+years?",
            # "at least X years"
            r"at\s+least\s+(\d+)\s+years?",
            # "X+ years"
            r"(\d+)\+\s+years?",
        ]

        for pattern in patterns:
            match = re.search(pattern, jd_text, re.IGNORECASE)
            if match:
                # If a range was captured (two groups), return the average
                if match.lastindex and match.lastindex >= 2:
                    try:
                        low = float(match.group(1))
                        high = float(match.group(2))
                        return (low + high) / 2
                    except (IndexError, ValueError):
                        pass
                try:
                    return float(match.group(1))
                except (IndexError, ValueError):
                    continue

        return 0.0  # No requirement found
