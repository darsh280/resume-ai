"""
seed_demo_data.py
=================
Seeds the database with:
  1. The 12 synthetic resumes from sample_data/resumes/
  2. The sample job 'Senior Full Stack Developer'
  3. Executes the full AI scoring pipeline to rank all 12 candidates.

Usage:
  cd backend
  python seed_demo_data.py
"""

import sys
import os
import json
from pathlib import Path

# Add backend directory to sys.path
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.database import engine, Base, SessionLocal
from app.models.job import JobDescription
from app.models.resume import Resume
from app.models.candidate import CandidateRanking
from app.models.analysis import Analysis
from app.services.resume_parser import ResumeParser
from app.services.skill_extractor import SkillExtractor
from app.services.scoring_engine import ScoringEngine
from app.utils.file_utils import save_upload

def seed():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        resumes_dir = PROJECT_ROOT / "sample_data" / "resumes"
        if not resumes_dir.exists():
            print(f"Error: {resumes_dir} does not exist.")
            return

        parser = ResumeParser()
        skill_extractor = SkillExtractor()
        scoring_engine = ScoringEngine()

        # 1. Seed Resumes
        print("\n1. Parsing & Seeding 12 Resumes...")
        uploaded_resumes = []
        for file_path in resumes_dir.glob("*.docx"):
            existing = db.query(Resume).filter(Resume.filename == file_path.name).first()
            if existing:
                uploaded_resumes.append(existing)
                continue

            content = file_path.read_bytes()
            saved_path = save_upload(content, file_path.name)
            parsed = parser.parse(saved_path)
            skills = skill_extractor.extract(parsed["raw_text"])

            resume = Resume(
                filename=file_path.name,
                file_path=saved_path,
                file_type="docx",
                candidate_name=parsed["candidate_name"],
                email=parsed["email"],
                phone=parsed["phone"],
                raw_text=parsed["raw_text"],
                extracted_skills=json.dumps(skills),
                education=json.dumps(parsed["education"]),
                work_experience=json.dumps(parsed["work_experience"]),
                projects=json.dumps(parsed["projects"]),
                certifications=json.dumps(parsed["certifications"]),
                years_experience=parsed["years_experience"],
            )
            db.add(resume)
            db.commit()
            db.refresh(resume)
            uploaded_resumes.append(resume)
            print(f"   + Added {resume.candidate_name} ({file_path.name})")

        print(f"Total resumes in DB: {db.query(Resume).count()}")

        # 2. Seed Job Description
        print("\n2. Seeding Sample Job Description...")
        jd_file = PROJECT_ROOT / "sample_data" / "job_descriptions" / "senior_full_stack_developer.txt"
        jd_text = jd_file.read_text(encoding="utf-8")
        job = db.query(JobDescription).filter(JobDescription.title == "Senior Full Stack Developer").first()

        if not job:
            jd_skills = skill_extractor.extract(jd_text)
            job = JobDescription(
                title="Senior Full Stack Developer",
                description=jd_text,
                required_experience=5.0,
                extracted_skills=json.dumps(jd_skills),
                required_qualifications=json.dumps([]),
            )
            db.add(job)
            db.commit()
            db.refresh(job)
            print(f"   + Created Job: {job.title} (ID: {job.id})")
        else:
            jd_skills = json.loads(job.extracted_skills or "[]")
            print(f"   Using existing Job: {job.title} (ID: {job.id})")

        # 3. Run Matching Analysis
        print("\n3. Running AI Matching & Candidate Ranking...")
        all_resumes = db.query(Resume).all()
        scored = []
        for r in all_resumes:
            r_skills = json.loads(r.extracted_skills or "[]")
            result = scoring_engine.score_candidate(
                jd_text=job.description,
                jd_skills=jd_skills,
                required_experience=job.required_experience,
                resume_text=r.raw_text,
                resume_skills=r_skills,
                candidate_experience=r.years_experience,
            )
            scored.append((r, result))

        # Sort descending by final score
        scored.sort(key=lambda x: x[1]["final_score"], reverse=True)

        # Create or update analysis record
        avg_score = sum(x[1]["final_score"] for x in scored) / len(scored) if scored else 0
        top_name = scored[0][0].candidate_name if scored else ""

        analysis = Analysis(
            job_id=job.id,
            name=f"Demonstration Analysis — {job.title}",
            total_resumes=len(scored),
            avg_score=round(avg_score, 2),
            top_candidate=top_name,
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        # Save rankings
        for rank, (r, res) in enumerate(scored, start=1):
            db.query(CandidateRanking).filter(
                CandidateRanking.resume_id == r.id,
                CandidateRanking.job_id == job.id,
            ).delete()

            ranking = CandidateRanking(
                resume_id=r.id,
                job_id=job.id,
                analysis_id=analysis.id,
                rank=rank,
                semantic_score=res["semantic_score"],
                skill_score=res["skill_score"],
                experience_score=res["experience_score"],
                education_score=res["education_score"],
                final_score=res["final_score"],
                matched_skills=json.dumps(res["matched_skills"]),
                missing_skills=json.dumps(res["missing_skills"]),
                additional_skills=json.dumps(res["additional_skills"]),
                recommendation=res["recommendation"],
            )
            db.add(ranking)
            db.commit()

        print(f"\nSuccessfully seeded & ranked {len(scored)} candidates!")
        print(f"Top Candidate: {top_name} (Rank #1, Score: {scored[0][1]['final_score']}%)")
        print(f"Average Score across candidates: {round(avg_score, 2)}%")
        print("Ready for live demonstration!")

    finally:
        db.close()

if __name__ == "__main__":
    seed()
