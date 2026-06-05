# Career Compass AI

Career Compass AI is a Python Flask web application for career roadmap generation, interview preparation, resume analysis, progress tracking, and rule-based AI career guidance.

## Python Concepts Demonstrated

- Python functions and modular programming
- Classes and OOP concepts
- Flask routing, templates, sessions, and form handling
- SQLite database integration
- CRUD operations for users, profiles, roadmap progress, scores, resumes, activities, and contacts
- File handling through PDF resume upload and parsing
- Exception handling for authentication, database work, and resume analysis
- Password hashing with Werkzeug

## Folder Structure

```text
CareerCompassAI/
├── app.py
├── database.py
├── models.py
├── chatbot.py
├── roadmap.py
├── resume_analyzer.py
├── requirements.txt
├── README.md
├── database.db
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── roadmap.html
│   ├── interview.html
│   ├── resume.html
│   ├── chatbot.html
│   ├── profile.html
│   ├── about.html
│   └── contact.html
└── static/
    ├── css/style.css
    ├── js/script.js
    ├── images/
    └── uploads/
```

## Installation

```bash
cd CareerCompassAI
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Demo Account

```text
Email: demo@careercompass.ai
Password: demo123
```

## Required Packages

- Flask
- Werkzeug
- PyPDF2
- sqlite3, datetime, and os from the Python standard library

## Main Routes

- `/` home page
- `/register` user registration
- `/login` user login
- `/logout` user logout
- `/dashboard` student dashboard
- `/roadmap` career roadmap generator
- `/interview` interview preparation and quiz scoring
- `/resume` PDF resume analyzer
- `/chatbot` Python rule-based AI career assistant
- `/profile` profile management
- `/about` project overview
- `/contact` contact form

## Database Tables

- `users`
- `user_profiles`
- `roadmap_progress`
- `interview_scores`
- `resume_analysis`
- `activities`
- `contact_messages`

The database is initialized automatically when `python app.py` runs.
