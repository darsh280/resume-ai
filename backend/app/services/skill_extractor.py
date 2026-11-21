"""
Skill Extractor Service
=======================
Uses a comprehensive, hand-curated skills dictionary combined with
regex-based multi-word matching to identify technical skills in text.

The dictionary covers:
  - Programming languages
  - Frontend frameworks & tools
  - Backend frameworks
  - Databases
  - Cloud & DevOps
  - AI / Machine Learning
  - Data Engineering
  - Mobile development
  - General developer tools
"""

import re
from typing import List, Set, Dict

# ---------------------------------------------------------------------------
# Skills dictionary — organized by category
# ---------------------------------------------------------------------------
SKILLS_DICTIONARY: Dict[str, List[str]] = {
    "programming_languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "c",
        "go", "golang", "rust", "ruby", "php", "swift", "kotlin", "scala",
        "r", "matlab", "perl", "haskell", "elixir", "dart", "objective-c",
        "assembly", "cobol", "fortran", "julia", "lua", "groovy",
        "bash", "shell", "powershell",
    ],
    "web_frontend": [
        "react", "react.js", "reactjs", "vue", "vue.js", "vuejs", "angular",
        "angularjs", "next.js", "nextjs", "nuxt.js", "svelte", "html", "html5",
        "css", "css3", "sass", "scss", "less", "tailwind", "tailwindcss",
        "tailwind css", "bootstrap", "material-ui", "mui", "chakra ui",
        "ant design", "jquery", "redux", "mobx", "zustand", "webpack",
        "vite", "babel", "gatsby", "remix",
    ],
    "web_backend": [
        "node.js", "nodejs", "express", "express.js", "fastapi", "django",
        "flask", "spring", "spring boot", "laravel", "rails", "ruby on rails",
        "asp.net", ".net", "dotnet", "graphql", "rest", "restful", "grpc",
        "websocket", "fastify", "hapi", "koa", "nestjs", "nest.js",
    ],
    "databases": [
        "sql", "mysql", "postgresql", "postgres", "sqlite", "mongodb", "redis",
        "cassandra", "dynamodb", "elasticsearch", "neo4j", "oracle", "mssql",
        "sql server", "mariadb", "couchdb", "firebase", "supabase", "prisma",
        "sqlalchemy", "sequelize", "mongoose", "typeorm",
    ],
    "cloud_devops": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s",
        "terraform", "ansible", "jenkins", "ci/cd", "github actions",
        "gitlab ci", "helm", "prometheus", "grafana", "elk", "logstash",
        "kibana", "nginx", "apache", "linux", "ubuntu", "centos",
        "serverless", "lambda", "s3", "ec2", "rds", "cloudformation",
        "heroku", "vercel", "netlify",
    ],
    "ai_ml": [
        "machine learning", "deep learning", "neural networks", "nlp",
        "natural language processing", "computer vision", "tensorflow",
        "pytorch", "keras", "scikit-learn", "sklearn", "pandas", "numpy",
        "matplotlib", "seaborn", "hugging face", "huggingface", "transformers",
        "bert", "gpt", "llm", "reinforcement learning", "cnn", "rnn", "lstm",
        "gan", "xgboost", "lightgbm", "catboost", "opencv", "nltk", "spacy",
        "fasttext", "sentence transformers", "langchain", "vector database",
        "rag", "mlflow", "kubeflow", "airflow", "data science", "data analysis",
        "feature engineering", "model deployment",
    ],
    "data_engineering": [
        "spark", "apache spark", "hadoop", "kafka", "apache kafka", "airflow",
        "apache airflow", "dbt", "snowflake", "databricks", "redshift",
        "bigquery", "data warehouse", "data lake", "etl", "elt", "pipeline",
        "streaming", "batch processing", "flink", "storm", "hive", "pig",
    ],
    "mobile": [
        "android", "ios", "react native", "flutter", "xamarin", "ionic",
        "mobile development",
    ],
    "tools_other": [
        "git", "github", "gitlab", "bitbucket", "jira", "confluence", "slack",
        "postman", "swagger", "openapi", "figma", "adobe xd", "agile",
        "scrum", "kanban", "tdd", "bdd", "unit testing", "jest", "pytest",
        "selenium", "cypress", "playwright", "microservices", "event-driven",
        "message queue", "rabbitmq", "celery", "oauth", "jwt", "ssl", "tls",
        "websockets", "tableau", "power bi",
    ],
}

# Flatten and deduplicate skill list (longer phrases first so they match before substrings)
_all_skills_raw: List[str] = []
for _skills in SKILLS_DICTIONARY.values():
    _all_skills_raw.extend(_skills)

# Remove duplicates, preserve order
_seen: Set[str] = set()
ALL_SKILLS: List[str] = []
for _s in _all_skills_raw:
    if _s not in _seen:
        _seen.add(_s)
        ALL_SKILLS.append(_s)

# Sort longest first so multi-word skills are matched before single-word substrings
ALL_SKILLS.sort(key=len, reverse=True)

# Alias map for normalisation (alias -> canonical)
_ALIASES: Dict[str, str] = {
    "react.js": "react",
    "reactjs": "react",
    "vue.js": "vue",
    "vuejs": "vue",
    "nodejs": "node.js",
    "next.js": "next.js",
    "nextjs": "next.js",
    "express.js": "express",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "k8s": "kubernetes",
    "huggingface": "hugging face",
    "tailwindcss": "tailwind css",
    "tailwind": "tailwind css",
}


class SkillExtractor:
    """Extract technical skills from text using the skills dictionary."""

    def __init__(self):
        # Pre-compile regex patterns for each skill
        self._patterns = {
            skill: re.compile(r"\b" + re.escape(skill) + r"\b", re.IGNORECASE)
            for skill in ALL_SKILLS
        }

    def extract(self, text: str) -> List[str]:
        """Return a deduplicated, sorted list of skills found in the text."""
        if not text:
            return []

        found: Set[str] = set()
        for skill, pattern in self._patterns.items():
            if pattern.search(text):
                # Normalise via alias map
                canonical = _ALIASES.get(skill.lower(), skill.lower())
                found.add(canonical)

        # Remove redundant aliases that survived normalisation
        # e.g., if both 'react' and 'react.js' somehow remain, keep 'react'
        cleaned = self._deduplicate(found)
        return sorted(list(cleaned))

    def _deduplicate(self, skills: Set[str]) -> Set[str]:
        """Remove known redundant variations when both appear."""
        result = set(skills)
        redundant_pairs = [
            ("react.js", "react"),
            ("vue.js", "vue"),
            ("nodejs", "node.js"),
            ("nextjs", "next.js"),
            ("sklearn", "scikit-learn"),
            ("k8s", "kubernetes"),
        ]
        for alias, canonical in redundant_pairs:
            if alias in result and canonical in result:
                result.discard(alias)
        return result

    def get_skill_categories(self, skills: List[str]) -> Dict[str, List[str]]:
        """Group a list of skills by their category."""
        categorized: Dict[str, List[str]] = {}
        for category, skill_list in SKILLS_DICTIONARY.items():
            matched = [s for s in skills if s in skill_list or s.lower() in [x.lower() for x in skill_list]]
            if matched:
                categorized[category] = matched
        return categorized
