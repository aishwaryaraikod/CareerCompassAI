import os
from PyPDF2 import PdfReader


class ResumeAnalyzer:
    """Extracts PDF text, detects skills, scores ATS readiness, and suggests fixes."""

    REQUIRED_SKILLS = {
        "python", "sql", "flask", "html", "css", "javascript", "sqlite", "machine learning",
        "data analysis", "git", "api", "oop", "communication", "leadership", "problem solving"
    }

    SECTIONS = ["education", "skills", "projects", "experience", "certifications", "contact"]

    def extract_text(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError("Uploaded resume file was not found.")
        try:
            reader = PdfReader(filepath)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as error:
            raise ValueError("Could not read PDF. Please upload a valid text-based PDF resume.") from error

    def analyze(self, filepath):
        text = self.extract_text(filepath)
        lowered = text.lower()
        found_skills = sorted(skill.title() for skill in self.REQUIRED_SKILLS if skill in lowered)
        missing_skills = sorted(skill.title() for skill in self.REQUIRED_SKILLS if skill not in lowered)
        sections_present = [section for section in self.SECTIONS if section in lowered]

        score = 30
        score += min(len(found_skills) * 4, 40)
        score += len(sections_present) * 4
        if len(text) > 1200:
            score += 6
        score = min(score, 100)

        if score >= 85:
            category = "Excellent"
        elif score >= 70:
            category = "Good"
        elif score >= 50:
            category = "Average"
        else:
            category = "Needs Improvement"

        suggestions = self._suggestions(found_skills, missing_skills, sections_present, score)
        return {
            "text": text[:1200],
            "score": score,
            "category": category,
            "skills": found_skills,
            "missing_skills": missing_skills[:8],
            "suggestions": suggestions,
        }

    def _suggestions(self, found_skills, missing_skills, sections_present, score):
        suggestions = []
        if missing_skills:
            suggestions.append("Add missing role keywords such as " + ", ".join(missing_skills[:5]) + ".")
        for section in self.SECTIONS:
            if section not in sections_present:
                suggestions.append(f"Add a clear {section.title()} section for ATS scanning.")
        if score < 70:
            suggestions.append("Quantify projects with metrics, tools used, and measurable outcomes.")
        suggestions.append("Keep formatting simple, use action verbs, and tailor the resume to each job description.")
        return suggestions
