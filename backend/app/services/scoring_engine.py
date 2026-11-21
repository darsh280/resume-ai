"""
Scoring Engine
==============
Implements the explainable, weighted scoring formula:

  Final Score = (Semantic Similarity × 0.40)
              + (Technical Skill Match  × 0.35)
              + (Experience Match       × 0.15)
              + (Education Match        × 0.10)

All component scores are on a 0–100 scale before weighting.

Education scoring:
  Levels: PhD=4, Master's=3, Bachelor's=2, Associate/Diploma=1, Unknown=0
  If the JD does not specify an education level → full marks (1.0).
  If the candidate's education level meets or exceeds the JD level → full marks.
  Otherwise → candidate_level / jd_level (proportional).

Recommendation thresholds:
  85–100 → "Excellent Match"
  70–84  → "Good Match"
  50–69  → "Moderate Match"
  <50    → "Low Match"
"""

from typing import List, Dict, Tuple, Set
from .skill_extractor import SkillExtractor
from .semantic_matcher import SemanticMatcher
from .experience_analyzer import ExperienceAnalyzer

# ---------------------------------------------------------------------------
# Scoring weights
# ---------------------------------------------------------------------------
WEIGHTS: Dict[str, float] = {
    "semantic": 0.40,
    "skills": 0.35,
    "experience": 0.15,
    "education": 0.10,
}

# ---------------------------------------------------------------------------
# Education keyword → numeric level
# ---------------------------------------------------------------------------
EDUCATION_LEVELS: Dict[str, int] = {
    "phd": 4, "ph.d": 4, "doctorate": 4, "doctoral": 4,
    "master": 3, "m.s": 3, "msc": 3, "m.tech": 3, "mba": 3, "m.e": 3,
    "bachelor": 2, "b.s": 2, "bsc": 2, "b.tech": 2, "b.e": 2,
    "undergraduate": 2, "b.sc": 2, "honours": 2,
    "associate": 1, "diploma": 1,
}


class ScoringEngine:
    """Central engine that computes all scoring components and final score."""

    def __init__(self):
        self.skill_extractor = SkillExtractor()
        self.semantic_matcher = SemanticMatcher()
        self.experience_analyzer = ExperienceAnalyzer()

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def score_candidate(
        self,
        jd_text: str,
        jd_skills: List[str],
        required_experience: float,
        resume_text: str,
        resume_skills: List[str],
        candidate_experience: float,
    ) -> Dict:
        """
        Compute every component score and return a detailed results dict.

        Returns:
            {
              semantic_score, skill_score, experience_score, education_score,
              final_score, matched_skills, missing_skills, additional_skills,
              recommendation, weights
            }
        """
        # 1. Semantic similarity (0–100)
        semantic_raw = self.semantic_matcher.compute_similarity(jd_text, resume_text)
        semantic_score = round(semantic_raw * 100, 2)

        # 2. Skill matching (0–100) + detail lists
        skill_raw, matched_skills, missing_skills, additional_skills = (
            self._compute_skill_score(jd_skills, resume_skills)
        )
        skill_score = round(skill_raw * 100, 2)

        # 3. Experience matching (0–100)
        experience_raw = self.experience_analyzer.compute_score(
            candidate_experience, required_experience
        )
        experience_score = round(experience_raw * 100, 2)

        # 4. Education matching (0–100)
        education_raw = self._compute_education_score(resume_text, jd_text)
        education_score = round(education_raw * 100, 2)

        # 5. Weighted final score
        final_score = round(
            semantic_score * WEIGHTS["semantic"]
            + skill_score * WEIGHTS["skills"]
            + experience_score * WEIGHTS["experience"]
            + education_score * WEIGHTS["education"],
            2,
        )

        return {
            "semantic_score": semantic_score,
            "skill_score": skill_score,
            "experience_score": experience_score,
            "education_score": education_score,
            "final_score": final_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "additional_skills": additional_skills,
            "recommendation": self._get_recommendation(final_score),
            "weights": WEIGHTS,
        }

    # -------------------------------------------------------------------------
    # Component scorers
    # -------------------------------------------------------------------------

    def _compute_skill_score(
        self,
        jd_skills: List[str],
        resume_skills: List[str],
    ) -> Tuple[float, List[str], List[str], List[str]]:
        """
        Compare JD skills against resume skills.

        Returns:
            (score 0.0–1.0, matched, missing, additional)
        """
        if not jd_skills:
            # No skills specified in JD → full score, nothing missing
            return 1.0, [], [], list(resume_skills)

        jd_set: Set[str] = {s.lower() for s in jd_skills}
        resume_set: Set[str] = {s.lower() for s in resume_skills}

        matched = sorted(jd_set & resume_set)
        missing = sorted(jd_set - resume_set)
        additional = sorted(resume_set - jd_set)

        score = len(matched) / len(jd_set) if jd_set else 1.0
        return score, matched, missing, additional

    def _get_education_level(self, text: str) -> int:
        """Return the highest education level found in the text (0 = not found)."""
        text_lower = text.lower()
        level = 0
        for keyword, value in EDUCATION_LEVELS.items():
            if keyword in text_lower:
                level = max(level, value)
        return level

    def _compute_education_score(self, resume_text: str, jd_text: str) -> float:
        """
        Score the candidate's education relative to the JD's requirement.

        Returns 0.0–1.0.
        """
        jd_level = self._get_education_level(jd_text)
        resume_level = self._get_education_level(resume_text)

        if jd_level == 0:
            return 1.0  # JD has no education requirement → full marks

        if resume_level >= jd_level:
            return 1.0  # Candidate meets or exceeds requirement

        if resume_level == 0:
            return 0.3  # Has some education but level is not detectable

        return round(resume_level / jd_level, 4)

    # -------------------------------------------------------------------------
    # Recommendation label
    # -------------------------------------------------------------------------

    @staticmethod
    def _get_recommendation(score: float) -> str:
        if score >= 85:
            return "Excellent Match"
        elif score >= 70:
            return "Good Match"
        elif score >= 50:
            return "Moderate Match"
        else:
            return "Low Match"
