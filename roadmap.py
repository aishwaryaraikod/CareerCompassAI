SPECIALIZATIONS = [
    "Artificial Intelligence", "Machine Learning", "Data Science", "Data Analytics",
    "Cyber Security", "Ethical Hacking", "Cloud Computing", "Full Stack Development",
    "Frontend Development", "Backend Development", "Mobile App Development", "Software Engineering",
    "DevOps Engineering", "UI/UX Design", "Blockchain Development", "Game Development",
    "Internet of Things (IoT)", "Robotics", "Computer Networks", "Database Administration",
    "Embedded Systems", "Computer Vision", "NLP Engineering", "AI Research", "Prompt Engineering"
]


BASE_SKILLS = {
    "ai": ["Python", "Linear Algebra", "Machine Learning", "Deep Learning", "MLOps", "Prompt Design"],
    "data": ["Python", "SQL", "Statistics", "Excel", "Power BI", "Data Cleaning", "Visualization"],
    "security": ["Networking", "Linux", "Python", "Cryptography", "Web Security", "Incident Response"],
    "web": ["HTML", "CSS", "JavaScript", "Python Flask", "SQL", "APIs", "Deployment"],
    "cloud": ["Linux", "Networking", "AWS/Azure", "Docker", "CI/CD", "Monitoring"],
    "design": ["Research", "Wireframing", "Figma", "Prototyping", "Usability Testing", "Design Systems"],
    "systems": ["C/C++", "Microcontrollers", "Networking", "Linux", "Debugging", "Hardware Interfaces"],
}


def category_for(name):
    lowered = name.lower()
    if any(word in lowered for word in ["ai", "machine", "vision", "nlp", "prompt"]):
        return "ai"
    if "data" in lowered:
        return "data"
    if any(word in lowered for word in ["cyber", "ethical"]):
        return "security"
    if any(word in lowered for word in ["stack", "frontend", "backend", "software", "mobile", "game", "blockchain"]):
        return "web"
    if any(word in lowered for word in ["cloud", "devops"]):
        return "cloud"
    if "ui/ux" in lowered:
        return "design"
    return "systems"


def generate_roadmap(specialization):
    """Return a complete roadmap dictionary for any supported specialization."""
    if specialization not in SPECIALIZATIONS:
        raise ValueError("Please select a valid career specialization.")

    category = category_for(specialization)
    skills = BASE_SKILLS[category]
    return {
        "title": specialization,
        "overview": f"{specialization} is a high-growth technology career path that blends problem solving, practical projects, and continuous learning.",
        "industry_demand": "Strong demand across startups, product companies, consulting firms, finance, healthcare, education, and global technology teams.",
        "future_scope": "Excellent long-term scope as organizations continue investing in automation, digital platforms, data systems, cloud infrastructure, and secure products.",
        "skills": skills,
        "learning_path": [
            "Build programming fundamentals and computer science basics.",
            "Learn core tools used by professionals in this domain.",
            "Create portfolio projects and document them on GitHub.",
            "Practice interviews, aptitude, communication, and resume storytelling.",
        ],
        "beginner": [
            "Learn Python fundamentals and Git basics.",
            f"Understand the foundations of {specialization}.",
            "Build two small guided projects.",
            "Write notes and explain concepts in your own words.",
        ],
        "intermediate": [
            "Work with databases, APIs, and real datasets or product requirements.",
            "Study domain-specific tools and common architectures.",
            "Build one complete project with documentation.",
            "Practice technical questions weekly.",
        ],
        "advanced": [
            "Solve open-ended problems and optimize project quality.",
            "Deploy or publish portfolio work.",
            "Contribute to open source, internships, or campus teams.",
            "Prepare for system design, behavioral, and HR interviews.",
        ],
        "certifications": [
            f"Foundations of {specialization}",
            "Python for Everybody or equivalent",
            "Google/Coursera/IBM professional certificate",
            "Cloud or security certification when relevant",
        ],
        "courses": [
            "CS50 or Python foundation course",
            f"Specialized {specialization} course on Coursera, edX, or Udemy",
            "SQL and database fundamentals",
            "Project-based portfolio bootcamp",
        ],
        "internships": [
            "Apply to campus innovation labs and local startups.",
            "Build a domain-specific capstone before applying.",
            "Target internships that mention Python, SQL, analytics, APIs, or cloud tools.",
        ],
        "job_roles": [
            f"Junior {specialization} Associate",
            "Python Developer",
            "Technical Analyst",
            "Project Intern",
            "Software Trainee",
        ],
        "salary_range": "India: INR 3 LPA - 12 LPA entry to early career; Global remote roles vary widely by skill and portfolio.",
        "projects": [
            f"{specialization} learning tracker",
            "Resume analyzer with skill matching",
            "Interview quiz dashboard",
            "Domain-specific recommendation system",
        ],
        "time_required": "6 to 12 months with consistent weekly learning, projects, interview practice, and feedback.",
        "total_steps": 12,
    }


def search_specializations(query):
    query = query.lower().strip()
    if not query:
        return SPECIALIZATIONS
    return [item for item in SPECIALIZATIONS if query in item.lower()]
