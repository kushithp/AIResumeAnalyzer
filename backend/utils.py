import re
from typing import List, Dict, Tuple

# Comprehensive taxonomy of skills grouped by domain
SKILL_TAXONOMY = {
    "Frontend": [
        "react", "vue", "angular", "next.js", "nuxt", "typescript", "javascript",
        "html", "css", "tailwind", "bootstrap", "redux", "sass", "webpack", "vite"
    ],
    "Backend": [
        "python", "fastapi", "django", "flask", "node.js", "express", "java",
        "spring boot", "c#", ".net", "go", "golang", "ruby", "rails", "php", "graphql", "rest api"
    ],
    "Database": [
        "sql", "postgresql", "mysql", "sqlite", "mongodb", "redis", "dynamodb",
        "oracle", "elasticsearch", "prisma", "sqlalchemy"
    ],
    "DevOps & Cloud": [
        "docker", "kubernetes", "aws", "azure", "gcp", "terraform", "ci/cd",
        "git", "github actions", "jenkins", "linux", "nginx", "serverless"
    ],
    "Tools & Frameworks": [
        "git", "jira", "postman", "figma", "jest", "cypress", "pytest", "npm", "yarn"
    ],
    "Soft Skills": [
        "communication", "leadership", "problem solving", "teamwork", "time management",
        "agile", "scrum", "adaptability", "critical thinking", "collaboration"
    ]
}

# Flattened set for quick lookup
ALL_SKILLS = set(skill for sublist in SKILL_TAXONOMY.values() for skill in sublist)


def extract_contact_info(text: str) -> Tuple[str, str, str]:
    """Extract candidate email, phone number, and candidate name heuristic."""
    # Email regex
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_match = re.search(email_pattern, text)
    email = email_match.group(0) if email_match else "Not Found"

    # Phone regex
    phone_pattern = r'(\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}'
    phone_match = re.search(phone_pattern, text)
    phone = phone_match.group(0) if phone_match else "Not Found"

    # Heuristic for Name: First non-empty line usually contains the candidate's name
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    name = "Candidate"
    if lines:
        first_line = lines[0]
        # Ignore if line looks like "Resume" or contains email/phone
        if len(first_line.split()) <= 4 and "@" not in first_line and not re.search(r'\d', first_line):
            name = first_line.title()

    return name, email, phone


def categorize_skills(skills: List[str]) -> List[Dict[str, List[str]]]:
    """Categorize a list of skills based on SKILL_TAXONOMY."""
    categorized = {cat: [] for cat in SKILL_TAXONOMY.keys()}
    
    for skill in skills:
        s_clean = skill.lower().strip()
        matched = False
        for cat, known_skills in SKILL_TAXONOMY.items():
            if any(k == s_clean for k in known_skills):
                categorized[cat].append(skill)
                matched = True
                break
        if not matched:
            categorized["Tools & Frameworks"].append(skill)
            
    # Filter empty categories
    return [{"category": cat, "skills": list(set(skill_list))} for cat, skill_list in categorized.items() if skill_list]
