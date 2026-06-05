from roadmap import SPECIALIZATIONS


class CareerAssistant:
    """Rule-based AI-style career assistant implemented with Python dictionaries."""

    def __init__(self):
        self.responses = {
            "data scientist": "To become a Data Scientist, learn Python, statistics, SQL, data cleaning, visualization, machine learning, and build projects using real datasets.",
            "ai engineer": "To become an AI Engineer, master Python, machine learning, deep learning, APIs, model deployment, and responsible AI concepts.",
            "cyber security": "A Cyber Security roadmap starts with networking, Linux, Python scripting, web security, cryptography, SOC basics, and ethical practice labs.",
            "certifications": "Good student certifications include Google Data Analytics, IBM AI Engineering, AWS Cloud Practitioner, Cisco CCNA, and Security+ depending on your target career.",
            "projects": "Strong student projects include resume analyzers, quiz platforms, AI chatbots, portfolio APIs, dashboards, malware URL detectors, and recommendation systems.",
            "placement": "For placements, revise DSA basics, DBMS, OS, CN, OOP, SQL, Python, projects, HR answers, and practice mock interviews weekly.",
            "resume": "A good resume should be one page, achievement-focused, keyword-rich, project-heavy, and tailored to the role you are applying for.",
            "interview": "Prepare interviews by mixing MCQs, coding practice, project explanation, system basics, HR storytelling, and timed mock rounds.",
        }

    def reply(self, message):
        text = (message or "").lower().strip()
        if not text:
            return "Ask me about careers, roadmaps, certifications, projects, resumes, or interview preparation."
        for key, response in self.responses.items():
            if key in text:
                return response
        for specialization in SPECIALIZATIONS:
            if specialization.lower() in text:
                return f"{specialization} is a strong option. Start with Python fundamentals, learn core domain skills, build 2-3 projects, complete one certification, and practice interviews."
        if "best career" in text or "which career" in text:
            return "Choose based on your strengths: Data Science for analysis, AI/ML for models, Cyber Security for defense, Full Stack for product building, and Cloud/DevOps for infrastructure."
        return "I would suggest starting with Python, SQL, Git, one focused specialization, two portfolio projects, and weekly interview practice. Tell me your interests for a sharper recommendation."
