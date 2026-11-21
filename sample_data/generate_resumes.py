"""
generate_resumes.py
===================
Creates 12 synthetic DOCX resumes for testing ResumeAI.
All candidate names and details are entirely fictional.

Usage:
    pip install python-docx
    python generate_resumes.py
"""

import os
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUTPUT_DIR = Path(__file__).parent / "resumes"
OUTPUT_DIR.mkdir(exist_ok=True)

NAVY = RGBColor(0x1A, 0x43, 0x8E)
GRAY = RGBColor(0x55, 0x55, 0x55)


def _heading(doc, text, level=1):
    return doc.add_heading(text, level=level)


def _divider(doc):
    p = doc.add_paragraph()
    run = p.add_run("─" * 72)
    run.font.size = Pt(7)
    run.font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)


def _section_heading(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text.upper())
    run.bold = True
    run.font.size = Pt(10)
    run.font.color.rgb = NAVY
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(1)


def _bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.add_run(text)
    p.paragraph_format.space_after = Pt(1)


def _normal(doc, text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(2)
    return p


def create_resume(
    filename, name, email, phone, title, summary,
    education, experience, skills, projects, certifications,
):
    doc = Document()

    # Page margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    # --- Name ---
    h = doc.add_heading(name, level=1)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- Contact ---
    contact = doc.add_paragraph(f"{email}  |  {phone}")
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact.paragraph_format.space_after = Pt(2)

    # --- Title ---
    t = doc.add_paragraph(title)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in t.runs:
        run.bold = True
        run.font.color.rgb = NAVY

    # --- Summary ---
    _section_heading(doc, "Professional Summary")
    _divider(doc)
    _normal(doc, summary)

    # --- Education ---
    _section_heading(doc, "Education")
    _divider(doc)
    for edu in education:
        p = doc.add_paragraph()
        r = p.add_run(edu["degree"])
        r.bold = True
        r.font.size = Pt(11)
        _normal(doc, f"{edu['school']}  |  {edu['year']}")

    # --- Experience ---
    _section_heading(doc, "Work Experience")
    _divider(doc)
    for exp in experience:
        p = doc.add_paragraph()
        r = p.add_run(f"{exp['title']}  —  {exp['company']}")
        r.bold = True
        _normal(doc, f"{exp['dates']}  |  {exp.get('location', 'Remote')}")
        for b in exp["bullets"]:
            _bullet(doc, b)

    # --- Skills ---
    _section_heading(doc, "Technical Skills")
    _divider(doc)
    for category, skill_list in skills.items():
        p = doc.add_paragraph()
        p.add_run(f"{category}: ").bold = True
        p.add_run(", ".join(skill_list))
        p.paragraph_format.space_after = Pt(2)

    # --- Projects ---
    _section_heading(doc, "Projects")
    _divider(doc)
    for proj in projects:
        p = doc.add_paragraph()
        p.add_run(proj["name"]).bold = True
        _normal(doc, proj["description"])
        if proj.get("tech"):
            _normal(doc, "Technologies: " + ", ".join(proj["tech"]))

    # --- Certifications ---
    if certifications:
        _section_heading(doc, "Certifications")
        _divider(doc)
        for cert in certifications:
            _bullet(doc, cert)

    path = OUTPUT_DIR / filename
    doc.save(str(path))
    print(f"  Created: {path.name}")
    return str(path)


# ===========================================================================
# Candidate data
# ===========================================================================

CANDIDATES = [
    {
        "filename": "alex_johnson_resume.docx",
        "name": "Alex Johnson",
        "email": "alex.johnson@email.com",
        "phone": "+1-555-0101",
        "title": "Senior Full Stack Developer",
        "summary": (
            "Senior Full Stack Developer with 7 years of experience building "
            "scalable web applications using Python, React, and AWS. Passionate "
            "about clean architecture, TDD, and cloud-native solutions. Led "
            "multiple cross-functional teams delivering enterprise-grade products."
        ),
        "education": [
            {"degree": "Master of Science in Computer Science",
             "school": "State University of Technology", "year": "2017"},
            {"degree": "Bachelor of Science in Software Engineering",
             "school": "City College of Engineering", "year": "2015"},
        ],
        "experience": [
            {
                "title": "Senior Full Stack Developer",
                "company": "TechCorp Solutions",
                "dates": "2020 – Present",
                "bullets": [
                    "Built RESTful APIs with Python FastAPI handling 50k+ requests/day",
                    "Led migration of monolithic application to microservices (Docker & Kubernetes)",
                    "Developed React.js dashboards with real-time data via WebSockets",
                    "Implemented CI/CD pipelines using GitHub Actions, cutting deploy time by 60%",
                    "Mentored 4 junior developers and conducted weekly code reviews",
                ],
            },
            {
                "title": "Full Stack Developer",
                "company": "WebStart Agency",
                "dates": "2017 – 2020",
                "bullets": [
                    "Built client-facing apps using React, Node.js, and PostgreSQL",
                    "Designed database schemas; optimised SQL queries by 40%",
                    "Deployed and maintained applications on AWS EC2 and S3",
                ],
            },
        ],
        "skills": {
            "Programming Languages": ["Python", "JavaScript", "TypeScript", "SQL"],
            "Frontend": ["React", "Next.js", "Tailwind CSS", "Redux"],
            "Backend": ["FastAPI", "Django", "Node.js", "Express"],
            "Cloud & DevOps": ["AWS", "Docker", "Kubernetes", "GitHub Actions", "CI/CD"],
            "Databases": ["PostgreSQL", "MongoDB", "Redis", "SQLite"],
            "Tools": ["Git", "Jira", "Postman", "Linux"],
        },
        "projects": [
            {
                "name": "E-Commerce Platform",
                "description": "Full-stack e-commerce platform with React and Django REST API handling 10k daily users.",
                "tech": ["React", "Django", "PostgreSQL", "AWS"],
            },
            {
                "name": "Real-Time Analytics Dashboard",
                "description": "Real-time analytics dashboard using WebSockets and D3.js visualisations.",
                "tech": ["React", "Node.js", "WebSockets", "MongoDB"],
            },
        ],
        "certifications": [
            "AWS Certified Solutions Architect – Associate",
            "Google Cloud Professional Developer",
        ],
    },
    {
        "filename": "jordan_smith_resume.docx",
        "name": "Jordan Smith",
        "email": "jordan.smith@email.com",
        "phone": "+1-555-0102",
        "title": "Machine Learning Engineer",
        "summary": (
            "Machine Learning Engineer with 5 years of experience in deep learning, "
            "NLP, and computer vision. PhD in Artificial Intelligence. Expert in "
            "PyTorch, TensorFlow, and production ML systems. Published 3 research papers."
        ),
        "education": [
            {"degree": "PhD in Artificial Intelligence",
             "school": "Institute of Advanced Technology", "year": "2020"},
            {"degree": "Master of Science in Machine Learning",
             "school": "National University", "year": "2017"},
        ],
        "experience": [
            {
                "title": "Machine Learning Engineer",
                "company": "AI Dynamics Inc.",
                "dates": "2020 – Present",
                "bullets": [
                    "Designed and deployed NLP models for text classification (94% accuracy)",
                    "Built production ML pipelines using MLflow and Apache Airflow",
                    "Implemented HuggingFace Transformers models for sentiment analysis",
                    "Reduced model inference latency by 55% using ONNX and TensorRT",
                    "Collaborated with data engineering team on Spark feature pipelines",
                ],
            },
            {
                "title": "AI Research Intern",
                "company": "Research Labs",
                "dates": "2018 – 2020",
                "bullets": [
                    "Published research on few-shot learning for NLP tasks",
                    "Developed computer vision models for object detection using PyTorch",
                ],
            },
        ],
        "skills": {
            "Programming Languages": ["Python", "R", "C++", "Julia"],
            "ML/AI Frameworks": ["PyTorch", "TensorFlow", "Keras", "scikit-learn", "HuggingFace"],
            "NLP": ["BERT", "GPT", "spaCy", "NLTK", "Sentence Transformers", "LangChain"],
            "Data Tools": ["pandas", "NumPy", "matplotlib", "Spark", "Airflow"],
            "MLOps": ["MLflow", "Docker", "Kubernetes", "AWS SageMaker"],
            "Databases": ["PostgreSQL", "MongoDB", "Redis"],
        },
        "projects": [
            {
                "name": "Multilingual Sentiment Analysis System",
                "description": "Multilingual sentiment analysis using BERT variants, deployed on AWS SageMaker.",
                "tech": ["PyTorch", "BERT", "AWS SageMaker", "FastAPI"],
            },
            {
                "name": "Real-Time Object Detection",
                "description": "Real-time object detection using YOLOv8 at 30 FPS on edge devices.",
                "tech": ["PyTorch", "YOLOv8", "OpenCV", "ONNX"],
            },
        ],
        "certifications": [
            "TensorFlow Developer Certificate",
            "AWS Certified Machine Learning Specialty",
            "Deep Learning Specialization (Coursera)",
        ],
    },
    {
        "filename": "morgan_lee_resume.docx",
        "name": "Morgan Lee",
        "email": "morgan.lee@email.com",
        "phone": "+1-555-0103",
        "title": "Backend Developer",
        "summary": (
            "Backend Developer with 3 years of experience building robust APIs "
            "using Node.js, Django, and PostgreSQL. Proficient in RESTful API design, "
            "database optimisation, and cloud deployments."
        ),
        "education": [
            {"degree": "Bachelor of Science in Computer Science",
             "school": "Western State University", "year": "2021"},
        ],
        "experience": [
            {
                "title": "Backend Developer",
                "company": "DataFlow Systems",
                "dates": "2021 – Present",
                "bullets": [
                    "Developed RESTful APIs using Node.js and Express (20k daily requests)",
                    "Designed PostgreSQL schemas; optimised queries reducing load times by 35%",
                    "Implemented authentication using JWT and OAuth 2.0",
                    "Set up automated testing with Jest at 80% code coverage",
                    "Deployed applications to AWS EC2, RDS, and Lambda",
                ],
            },
        ],
        "skills": {
            "Programming Languages": ["JavaScript", "Python", "SQL"],
            "Backend": ["Node.js", "Express", "Django", "FastAPI"],
            "Databases": ["PostgreSQL", "MySQL", "MongoDB", "Redis"],
            "Cloud": ["AWS", "Docker", "GitHub Actions"],
            "Tools": ["Git", "Postman", "Jest", "Linux"],
        },
        "projects": [
            {
                "name": "Task Management API",
                "description": "Comprehensive task management REST API with role-based access control.",
                "tech": ["Node.js", "Express", "PostgreSQL", "JWT"],
            },
            {
                "name": "File Storage Service",
                "description": "Scalable file storage microservice with S3 integration and thumbnail generation.",
                "tech": ["Python", "FastAPI", "AWS S3", "Docker"],
            },
        ],
        "certifications": [
            "AWS Certified Developer – Associate",
            "MongoDB Certified Developer",
        ],
    },
    {
        "filename": "casey_williams_resume.docx",
        "name": "Casey Williams",
        "email": "casey.williams@email.com",
        "phone": "+1-555-0104",
        "title": "Junior Frontend Developer",
        "summary": (
            "Junior Frontend Developer with 1 year of experience creating responsive "
            "web interfaces using React, Vue.js, and modern CSS frameworks. Quick learner "
            "with strong foundation in HTML, CSS, and JavaScript fundamentals."
        ),
        "education": [
            {"degree": "Bachelor of Science in Information Technology",
             "school": "Community Technology College", "year": "2023"},
        ],
        "experience": [
            {
                "title": "Junior Frontend Developer",
                "company": "Creative Web Studio",
                "dates": "2023 – Present",
                "bullets": [
                    "Built responsive UI components using React and Tailwind CSS",
                    "Implemented state management with Redux Toolkit",
                    "Collaborated with backend team to integrate REST APIs",
                    "Participated in daily standups and sprint planning",
                ],
            },
        ],
        "skills": {
            "Programming Languages": ["JavaScript", "HTML", "CSS"],
            "Frontend": ["React", "Vue", "Tailwind CSS", "Bootstrap"],
            "Tools": ["Git", "Figma", "npm", "Webpack"],
            "Others": ["REST APIs", "Responsive Design"],
        },
        "projects": [
            {
                "name": "Portfolio Website",
                "description": "Personal portfolio website built with React and Tailwind CSS with animations.",
                "tech": ["React", "Tailwind CSS", "Framer Motion"],
            },
            {
                "name": "Weather Dashboard",
                "description": "Weather dashboard with OpenWeather API integration and location-based forecasts.",
                "tech": ["React", "Axios", "Chart.js"],
            },
        ],
        "certifications": [
            "Meta Frontend Developer Certificate",
            "freeCodeCamp Responsive Web Design",
        ],
    },
    {
        "filename": "riley_davis_resume.docx",
        "name": "Riley Davis",
        "email": "riley.davis@email.com",
        "phone": "+1-555-0105",
        "title": "DevOps Engineer",
        "summary": (
            "DevOps Engineer with 6 years of experience in infrastructure automation, "
            "CI/CD pipeline design, container orchestration, and cloud management. "
            "AWS Certified Solutions Architect with expertise in Kubernetes and Terraform."
        ),
        "education": [
            {"degree": "Bachelor of Science in Computer Science",
             "school": "Northern Technical University", "year": "2018"},
        ],
        "experience": [
            {
                "title": "Senior DevOps Engineer",
                "company": "CloudInfra Corp",
                "dates": "2021 – Present",
                "bullets": [
                    "Architected and managed Kubernetes clusters for 200+ microservices",
                    "Built CI/CD pipelines with Jenkins and GitHub Actions",
                    "Automated infrastructure provisioning using Terraform and Ansible",
                    "Implemented monitoring with Prometheus, Grafana, and ELK stack",
                    "Reduced infrastructure costs by 40% through optimisation and auto-scaling",
                ],
            },
            {
                "title": "DevOps Engineer",
                "company": "StartupOps",
                "dates": "2018 – 2021",
                "bullets": [
                    "Containerised 15+ applications using Docker",
                    "Managed AWS infrastructure: EC2, S3, RDS, Lambda, CloudFormation",
                    "Implemented security best practices and SSL/TLS certificate management",
                ],
            },
        ],
        "skills": {
            "Cloud Platforms": ["AWS", "Azure", "GCP"],
            "Containers": ["Docker", "Kubernetes", "Helm"],
            "IaC": ["Terraform", "Ansible", "CloudFormation"],
            "CI/CD": ["Jenkins", "GitHub Actions", "GitLab CI"],
            "Monitoring": ["Prometheus", "Grafana", "ELK Stack"],
            "Programming": ["Python", "Bash", "YAML"],
        },
        "projects": [
            {
                "name": "Multi-Cloud Kubernetes Platform",
                "description": "Multi-cloud Kubernetes platform spanning AWS and GCP with unified monitoring.",
                "tech": ["Kubernetes", "Terraform", "Prometheus", "Grafana"],
            },
            {
                "name": "Zero-Downtime Deployment System",
                "description": "Blue-green deployment strategy achieving zero-downtime releases for 50+ services.",
                "tech": ["Kubernetes", "Istio", "GitHub Actions"],
            },
        ],
        "certifications": [
            "AWS Certified Solutions Architect – Professional",
            "Certified Kubernetes Administrator (CKA)",
            "HashiCorp Terraform Associate",
        ],
    },
    {
        "filename": "taylor_brown_resume.docx",
        "name": "Taylor Brown",
        "email": "taylor.brown@email.com",
        "phone": "+1-555-0106",
        "title": "Data Scientist",
        "summary": (
            "Data Scientist with 4 years of experience in machine learning, statistical "
            "modelling, and business intelligence. Master's in Data Science. Proficient in "
            "Python, R, and SQL with expertise in feature engineering and A/B testing."
        ),
        "education": [
            {"degree": "Master of Science in Data Science",
             "school": "Analytics Graduate School", "year": "2020"},
            {"degree": "Bachelor of Science in Mathematics",
             "school": "State University", "year": "2018"},
        ],
        "experience": [
            {
                "title": "Data Scientist",
                "company": "Insight Analytics",
                "dates": "2020 – Present",
                "bullets": [
                    "Built predictive churn model using XGBoost reducing churn by 25%",
                    "Performed A/B testing for product features resulting in 15% conversion uplift",
                    "Created interactive dashboards using Tableau and Plotly",
                    "Developed recommendation engine using collaborative filtering",
                    "Maintained data pipelines with Apache Airflow and dbt",
                ],
            },
        ],
        "skills": {
            "Programming": ["Python", "R", "SQL"],
            "ML Libraries": ["scikit-learn", "XGBoost", "LightGBM", "CatBoost"],
            "Data Tools": ["pandas", "NumPy", "matplotlib", "seaborn"],
            "Big Data": ["Spark", "Airflow", "dbt"],
            "Visualization": ["Tableau", "Plotly", "matplotlib"],
            "Databases": ["PostgreSQL", "BigQuery", "Redshift"],
        },
        "projects": [
            {
                "name": "Customer Churn Prediction",
                "description": "Ensemble ML model predicting churn with 91% accuracy, deployed as Flask API.",
                "tech": ["Python", "XGBoost", "Flask", "PostgreSQL"],
            },
            {
                "name": "Product Recommendation Engine",
                "description": "Collaborative filtering recommendation system increasing AOV by 18%.",
                "tech": ["Python", "scikit-learn", "Redis", "FastAPI"],
            },
        ],
        "certifications": [
            "Google Professional Data Analyst",
            "Databricks Certified Associate Developer",
            "dbt Certified Developer",
        ],
    },
    {
        "filename": "quinn_miller_resume.docx",
        "name": "Quinn Miller",
        "email": "quinn.miller@email.com",
        "phone": "+1-555-0107",
        "title": "Mobile App Developer",
        "summary": (
            "Mobile App Developer with 3 years of experience building cross-platform and "
            "native mobile applications. Proficient in Flutter, React Native, and Swift. "
            "Delivered 8 production apps with 100k+ combined downloads."
        ),
        "education": [
            {"degree": "Bachelor of Science in Computer Science",
             "school": "Mobile Tech University", "year": "2021"},
        ],
        "experience": [
            {
                "title": "Mobile Developer",
                "company": "AppForge Studios",
                "dates": "2021 – Present",
                "bullets": [
                    "Developed 5 cross-platform apps using Flutter with 50k+ combined downloads",
                    "Built React Native apps integrating with RESTful APIs and Firebase",
                    "Implemented push notifications, in-app purchases, and analytics",
                    "Published apps to Apple App Store and Google Play Store",
                    "Used Swift for iOS-native features including Face ID and ARKit",
                ],
            },
        ],
        "skills": {
            "Mobile": ["Flutter", "React Native", "Swift", "Kotlin"],
            "Frontend": ["React", "JavaScript", "TypeScript"],
            "Backend Integration": ["REST APIs", "Firebase", "GraphQL"],
            "Tools": ["Git", "Xcode", "Android Studio", "Figma"],
        },
        "projects": [
            {
                "name": "FitTrack Fitness App",
                "description": "Cross-platform fitness tracking app with workout logging and social features.",
                "tech": ["Flutter", "Firebase", "Dart"],
            },
            {
                "name": "Food Delivery App",
                "description": "Food ordering and delivery app with real-time GPS tracking.",
                "tech": ["React Native", "Node.js", "Google Maps API"],
            },
        ],
        "certifications": [
            "Google Associate Android Developer",
            "Apple iOS Developer Certificate",
        ],
    },
    {
        "filename": "sam_anderson_resume.docx",
        "name": "Sam Anderson",
        "email": "sam.anderson@email.com",
        "phone": "+1-555-0108",
        "title": "Full Stack Developer",
        "summary": (
            "Experienced Full Stack Developer with 8 years building production web "
            "applications. Expert in React, Node.js, Python, and MongoDB. Led development "
            "of multiple SaaS products from concept to launch with 10k+ active users."
        ),
        "education": [
            {"degree": "Bachelor of Science in Computer Science",
             "school": "Pacific University", "year": "2016"},
        ],
        "experience": [
            {
                "title": "Lead Full Stack Developer",
                "company": "SaaS Ventures",
                "dates": "2019 – Present",
                "bullets": [
                    "Led team of 6 developers building a SaaS HR platform with 50k+ users",
                    "Architected microservices backend using Node.js and Python FastAPI",
                    "Implemented real-time collaboration with WebSockets and Redis",
                    "Built PDF and Excel report generation for 10k+ monthly exports",
                    "Established coding standards and code review processes",
                ],
            },
            {
                "title": "Full Stack Developer",
                "company": "Digital Agency X",
                "dates": "2016 – 2019",
                "bullets": [
                    "Built 20+ client web apps using React and Node.js",
                    "Developed REST APIs integrated with Stripe, Twilio, and AWS",
                    "Optimised MongoDB queries and indexes improving performance by 50%",
                ],
            },
        ],
        "skills": {
            "Frontend": ["React", "Next.js", "TypeScript", "Redux", "Tailwind CSS"],
            "Backend": ["Node.js", "Python", "FastAPI", "Express", "GraphQL"],
            "Databases": ["MongoDB", "PostgreSQL", "Redis", "Elasticsearch"],
            "DevOps": ["AWS", "Docker", "GitHub Actions", "Linux"],
            "Tools": ["Git", "Jira", "Postman", "Figma"],
        },
        "projects": [
            {
                "name": "HR Management Platform",
                "description": "Comprehensive HR SaaS platform with employee management, payroll, and analytics.",
                "tech": ["React", "Node.js", "PostgreSQL", "AWS"],
            },
            {
                "name": "Real-Time Chat Application",
                "description": "Scalable chat with file sharing, group rooms, and message search.",
                "tech": ["React", "Node.js", "WebSockets", "MongoDB", "Redis"],
            },
        ],
        "certifications": [
            "AWS Certified Developer",
            "MongoDB Certified Developer",
        ],
    },
    {
        "filename": "jamie_wilson_resume.docx",
        "name": "Jamie Wilson",
        "email": "jamie.wilson@email.com",
        "phone": "+1-555-0109",
        "title": "Frontend Developer",
        "summary": (
            "Frontend Developer with 2 years specialising in React, TypeScript, and "
            "modern CSS frameworks. Passionate about pixel-perfect UI, accessibility, "
            "and performance optimisation."
        ),
        "education": [
            {"degree": "Bachelor of Science in Web Development",
             "school": "Design and Technology Institute", "year": "2022"},
        ],
        "experience": [
            {
                "title": "Frontend Developer",
                "company": "UI Craft Studio",
                "dates": "2022 – Present",
                "bullets": [
                    "Built responsive React apps using TypeScript and Tailwind CSS",
                    "Implemented complex UI: data tables, charts, and form wizards",
                    "Integrated REST APIs using Axios with error handling and loading states",
                    "Improved Lighthouse score from 65 to 95 through optimisation",
                    "Wrote unit and integration tests with Jest and React Testing Library",
                ],
            },
        ],
        "skills": {
            "Frontend": ["React", "TypeScript", "Next.js", "Tailwind CSS", "SCSS"],
            "State Management": ["Redux", "Zustand", "React Query"],
            "Testing": ["Jest", "React Testing Library", "Cypress"],
            "Tools": ["Git", "Figma", "Webpack", "Vite"],
        },
        "projects": [
            {
                "name": "Design System Library",
                "description": "Reusable component library with 40+ components, Storybook docs, and npm publishing.",
                "tech": ["React", "TypeScript", "Storybook", "Tailwind CSS"],
            },
            {
                "name": "Admin Dashboard Template",
                "description": "Fully responsive admin dashboard with dark mode and 15 chart types.",
                "tech": ["React", "TypeScript", "Recharts", "Tailwind CSS"],
            },
        ],
        "certifications": [
            "Meta React Developer Certificate",
            "Certified Scrum Developer",
        ],
    },
    {
        "filename": "drew_martinez_resume.docx",
        "name": "Drew Martinez",
        "email": "drew.martinez@email.com",
        "phone": "+1-555-0110",
        "title": "Cloud Solutions Architect",
        "summary": (
            "Cloud Solutions Architect with 10 years of experience designing enterprise "
            "cloud infrastructure across AWS, Azure, and GCP. Multiple cloud certifications. "
            "Expert in Terraform, Kubernetes, and cloud security."
        ),
        "education": [
            {"degree": "Master of Science in Information Systems",
             "school": "Enterprise Technology School", "year": "2015"},
            {"degree": "Bachelor of Engineering in Computer Engineering",
             "school": "National Engineering College", "year": "2013"},
        ],
        "experience": [
            {
                "title": "Principal Cloud Architect",
                "company": "Enterprise Cloud Solutions",
                "dates": "2019 – Present",
                "bullets": [
                    "Architected multi-region AWS infrastructure serving 2M+ users globally",
                    "Led cloud migration of 50+ on-premise workloads to AWS and Azure",
                    "Designed DR strategy achieving 99.99% uptime SLA",
                    "Implemented cloud cost governance saving $500k annually",
                    "Led team of 8 cloud engineers and 3 DevOps specialists",
                ],
            },
            {
                "title": "Cloud Engineer",
                "company": "TechGrowth Partners",
                "dates": "2015 – 2019",
                "bullets": [
                    "Built and managed AWS infrastructure using CloudFormation and Terraform",
                    "Implemented security controls, IAM policies, and VPC architecture",
                    "Set up monitoring for 100+ microservices using CloudWatch and Datadog",
                ],
            },
        ],
        "skills": {
            "Cloud Platforms": ["AWS", "Azure", "GCP", "Oracle Cloud"],
            "IaC & Automation": ["Terraform", "Ansible", "CloudFormation", "Pulumi"],
            "Containers": ["Docker", "Kubernetes", "Helm", "Istio"],
            "Security": ["AWS IAM", "VPC", "WAF", "SSL/TLS"],
            "Monitoring": ["CloudWatch", "Datadog", "Prometheus", "Grafana"],
            "Programming": ["Python", "Bash", "Go"],
        },
        "projects": [
            {
                "name": "Global Multi-Region Platform",
                "description": "Multi-region active-active AWS architecture handling 100M+ requests/day.",
                "tech": ["AWS", "Terraform", "Kubernetes", "Istio"],
            },
            {
                "name": "Cloud Cost Optimization Tool",
                "description": "Automated cost optimisation tool eliminating unused resources, saving $500k/year.",
                "tech": ["Python", "AWS Boto3", "Lambda", "DynamoDB"],
            },
        ],
        "certifications": [
            "AWS Certified Solutions Architect – Professional",
            "AWS Certified Security Specialist",
            "Google Cloud Professional Architect",
            "Azure Solutions Architect Expert",
            "Certified Kubernetes Administrator (CKA)",
            "HashiCorp Terraform Associate",
        ],
    },
    {
        "filename": "avery_taylor_resume.docx",
        "name": "Avery Taylor",
        "email": "avery.taylor@email.com",
        "phone": "+1-555-0111",
        "title": "Junior Data Analyst",
        "summary": (
            "Junior Data Analyst with 1.5 years of experience in data wrangling, "
            "statistical analysis, and business reporting. Bachelor's in Statistics. "
            "Proficient in Python, SQL, and Excel with growing ML expertise."
        ),
        "education": [
            {"degree": "Bachelor of Science in Statistics",
             "school": "Applied Sciences University", "year": "2022"},
        ],
        "experience": [
            {
                "title": "Junior Data Analyst",
                "company": "Market Insights Co.",
                "dates": "2022 – Present",
                "bullets": [
                    "Analysed sales data using Python pandas and SQL to identify growth trends",
                    "Created automated weekly reports using Excel and Python scripts",
                    "Built Tableau dashboards for executive KPI tracking",
                    "Performed data cleaning and validation for 1M+ record datasets",
                    "Collaborated with marketing on customer segmentation analysis",
                ],
            },
        ],
        "skills": {
            "Programming": ["Python", "SQL", "R"],
            "Data Analysis": ["pandas", "NumPy", "Excel", "SPSS"],
            "Visualization": ["Tableau", "matplotlib", "seaborn", "Power BI"],
            "Databases": ["MySQL", "PostgreSQL"],
        },
        "projects": [
            {
                "name": "Sales Forecasting Model",
                "description": "Time-series forecasting model for monthly sales prediction with 88% accuracy.",
                "tech": ["Python", "scikit-learn", "pandas", "matplotlib"],
            },
            {
                "name": "Customer Segmentation Analysis",
                "description": "K-means clustering on customer purchase data identifying 5 distinct segments.",
                "tech": ["Python", "scikit-learn", "Tableau"],
            },
        ],
        "certifications": [
            "Google Data Analytics Certificate",
            "Tableau Desktop Specialist",
        ],
    },
    {
        "filename": "blake_thomas_resume.docx",
        "name": "Blake Thomas",
        "email": "blake.thomas@email.com",
        "phone": "+1-555-0112",
        "title": "Senior Backend Engineer",
        "summary": (
            "Senior Backend Engineer with 9 years building high-performance backend "
            "systems using Python, FastAPI, and Django. Expert in API design, database "
            "architecture, and system scalability. Master's in Computer Science."
        ),
        "education": [
            {"degree": "Master of Science in Computer Science",
             "school": "Graduate School of Engineering", "year": "2016"},
            {"degree": "Bachelor of Science in Computer Science",
             "school": "State University", "year": "2014"},
        ],
        "experience": [
            {
                "title": "Senior Backend Engineer",
                "company": "Scale Systems",
                "dates": "2020 – Present",
                "bullets": [
                    "Designed Python FastAPI backend handling 500k requests/day",
                    "Architected PostgreSQL layer with read replicas and connection pooling",
                    "Implemented Redis caching strategy reducing DB load by 70%",
                    "Built async task queues using Celery and RabbitMQ",
                    "Led backend team of 5 engineers and established engineering best practices",
                ],
            },
            {
                "title": "Backend Developer",
                "company": "Platform Co.",
                "dates": "2016 – 2020",
                "bullets": [
                    "Built Django REST APIs serving mobile and web clients",
                    "Designed PostgreSQL schemas and ORM models using SQLAlchemy",
                    "Implemented OAuth2.0 authentication and JWT token management",
                    "Set up automated testing with pytest at 90% coverage",
                ],
            },
        ],
        "skills": {
            "Programming Languages": ["Python", "SQL", "Go", "Bash"],
            "Backend Frameworks": ["FastAPI", "Django", "Flask", "Celery"],
            "Databases": ["PostgreSQL", "MySQL", "Redis", "MongoDB", "Elasticsearch"],
            "DevOps": ["Docker", "Kubernetes", "AWS", "GitHub Actions", "Linux"],
            "Tools": ["Git", "SQLAlchemy", "Alembic", "pytest", "Postman"],
        },
        "projects": [
            {
                "name": "High-Performance API Gateway",
                "description": "API gateway handling 500k requests/day with rate limiting, caching, and analytics.",
                "tech": ["Python", "FastAPI", "Redis", "PostgreSQL", "Docker"],
            },
            {
                "name": "Distributed Task Processing System",
                "description": "Distributed task processor using Celery and RabbitMQ processing 1M tasks/day.",
                "tech": ["Python", "Celery", "RabbitMQ", "Redis", "PostgreSQL"],
            },
        ],
        "certifications": [
            "AWS Certified Developer",
            "PostgreSQL Associate Certification",
            "Python Institute Professional Certification",
        ],
    },
]


if __name__ == "__main__":
    print(f"\nGenerating {len(CANDIDATES)} synthetic resumes...")
    print(f"Output directory: {OUTPUT_DIR}\n")
    for c in CANDIDATES:
        create_resume(**c)
    print(f"\nAll {len(CANDIDATES)} resumes created successfully in {OUTPUT_DIR}")
