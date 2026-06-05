import os
import sqlite3
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


class Database:
    """Small SQLite helper that centralizes connection, schema, and CRUD utilities."""

    def __init__(self, path=DB_PATH):
        self.path = path

    def connect(self):
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def execute(self, query, params=(), commit=False):
        try:
            with self.connect() as connection:
                cursor = connection.execute(query, params)
                if commit:
                    connection.commit()
                return cursor
        except sqlite3.Error as error:
            raise RuntimeError(f"Database operation failed: {error}") from error

    def fetch_one(self, query, params=()):
        cursor = self.execute(query, params)
        return cursor.fetchone()

    def fetch_all(self, query, params=()):
        cursor = self.execute(query, params)
        return cursor.fetchall()

    def init_db(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    full_name TEXT DEFAULT '',
                    college TEXT DEFAULT '',
                    career_goal TEXT DEFAULT '',
                    bio TEXT DEFAULT '',
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS roadmap_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    specialization TEXT NOT NULL,
                    completed_steps INTEGER DEFAULT 0,
                    total_steps INTEGER DEFAULT 12,
                    updated_at TEXT NOT NULL,
                    UNIQUE(user_id, specialization),
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS interview_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS resume_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    filename TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    skills TEXT NOT NULL,
                    missing_skills TEXT NOT NULL,
                    suggestions TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS contact_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )
            connection.commit()
        self.seed_sample_data()

    def seed_sample_data(self):
        existing = self.fetch_one("SELECT id FROM users WHERE email = ?", ("demo@careercompass.ai",))
        if existing:
            return
        from werkzeug.security import generate_password_hash

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        password = generate_password_hash("demo123")
        self.execute(
            "INSERT INTO users (username, email, password, created_at) VALUES (?, ?, ?, ?)",
            ("demo_student", "demo@careercompass.ai", password, created_at),
            commit=True,
        )
        user = self.fetch_one("SELECT id FROM users WHERE email = ?", ("demo@careercompass.ai",))
        self.execute(
            "INSERT INTO user_profiles (user_id, full_name, college, career_goal, bio) VALUES (?, ?, ?, ?, ?)",
            (user["id"], "Demo Student", "Career Compass Institute", "Data Science", "Exploring AI career paths."),
            commit=True,
        )
        self.execute(
            "INSERT INTO interview_scores (user_id, category, score, total, date) VALUES (?, ?, ?, ?, ?)",
            (user["id"], "Python", 4, 5, created_at),
            commit=True,
        )
        self.execute(
            "INSERT INTO roadmap_progress (user_id, specialization, completed_steps, total_steps, updated_at) VALUES (?, ?, ?, ?, ?)",
            (user["id"], "Data Science", 5, 12, created_at),
            commit=True,
        )


db = Database()


def init_db():
    db.init_db()
