from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from database import db


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


class User:
    """User model with authentication and profile CRUD behavior."""

    def __init__(self, row):
        self.id = row["id"]
        self.username = row["username"]
        self.email = row["email"]
        self.created_at = row["created_at"]

    @staticmethod
    def create(username, email, password):
        if not username or not email or not password:
            raise ValueError("All registration fields are required.")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")
        existing = db.fetch_one("SELECT id FROM users WHERE email = ?", (email.lower(),))
        if existing:
            raise ValueError("An account with this email already exists.")
        db.execute(
            "INSERT INTO users (username, email, password, created_at) VALUES (?, ?, ?, ?)",
            (username.strip(), email.lower().strip(), generate_password_hash(password), now_text()),
            commit=True,
        )
        row = db.fetch_one("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))
        db.execute("INSERT INTO user_profiles (user_id) VALUES (?)", (row["id"],), commit=True)
        Activity.log(row["id"], "Account created")
        return User(row)

    @staticmethod
    def authenticate(email, password):
        row = db.fetch_one("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))
        if not row or not check_password_hash(row["password"], password):
            raise ValueError("Invalid email or password.")
        Activity.log(row["id"], "Logged in")
        return User(row)

    @staticmethod
    def get(user_id):
        row = db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
        return User(row) if row else None


class Profile:
    @staticmethod
    def get(user_id):
        return db.fetch_one("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))

    @staticmethod
    def update(user_id, full_name, college, career_goal, bio):
        db.execute(
            """
            UPDATE user_profiles
            SET full_name = ?, college = ?, career_goal = ?, bio = ?
            WHERE user_id = ?
            """,
            (full_name.strip(), college.strip(), career_goal.strip(), bio.strip(), user_id),
            commit=True,
        )
        Activity.log(user_id, "Profile updated")


class RoadmapProgress:
    @staticmethod
    def upsert(user_id, specialization, completed_steps, total_steps):
        db.execute(
            """
            INSERT INTO roadmap_progress (user_id, specialization, completed_steps, total_steps, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, specialization)
            DO UPDATE SET completed_steps = excluded.completed_steps,
                          total_steps = excluded.total_steps,
                          updated_at = excluded.updated_at
            """,
            (user_id, specialization, completed_steps, total_steps, now_text()),
            commit=True,
        )
        Activity.log(user_id, f"Updated roadmap progress for {specialization}")

    @staticmethod
    def for_user(user_id):
        return db.fetch_all("SELECT * FROM roadmap_progress WHERE user_id = ? ORDER BY updated_at DESC", (user_id,))


class InterviewScore:
    @staticmethod
    def create(user_id, category, score, total):
        db.execute(
            "INSERT INTO interview_scores (user_id, category, score, total, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, category, score, total, now_text()),
            commit=True,
        )
        Activity.log(user_id, f"Completed {category} quiz with {score}/{total}")

    @staticmethod
    def for_user(user_id):
        return db.fetch_all("SELECT * FROM interview_scores WHERE user_id = ? ORDER BY date DESC", (user_id,))


class ResumeAnalysis:
    @staticmethod
    def create(user_id, filename, score, category, skills, missing_skills, suggestions):
        db.execute(
            """
            INSERT INTO resume_analysis
            (user_id, filename, score, category, skills, missing_skills, suggestions, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, filename, score, category, ", ".join(skills), ", ".join(missing_skills), "\n".join(suggestions), now_text()),
            commit=True,
        )
        Activity.log(user_id, f"Analyzed resume: {filename}")

    @staticmethod
    def latest(user_id):
        return db.fetch_one("SELECT * FROM resume_analysis WHERE user_id = ? ORDER BY created_at DESC LIMIT 1", (user_id,))

    @staticmethod
    def for_user(user_id):
        return db.fetch_all("SELECT * FROM resume_analysis WHERE user_id = ? ORDER BY created_at DESC", (user_id,))


class Activity:
    @staticmethod
    def log(user_id, message):
        db.execute(
            "INSERT INTO activities (user_id, message, created_at) VALUES (?, ?, ?)",
            (user_id, message, now_text()),
            commit=True,
        )

    @staticmethod
    def recent(user_id, limit=6):
        return db.fetch_all(
            "SELECT * FROM activities WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit),
        )
