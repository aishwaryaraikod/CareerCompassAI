import os
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from chatbot import CareerAssistant
from database import db, init_db
from models import Activity, InterviewScore, Profile, ResumeAnalysis, RoadmapProgress, User
from resume_analyzer import ResumeAnalyzer
from roadmap import SPECIALIZATIONS, generate_roadmap, search_specializations


app = Flask(__name__)
app.config["SECRET_KEY"] = "career-compass-ai-secret-key"
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024

chatbot = CareerAssistant()
resume_analyzer = ResumeAnalyzer()


INTERVIEW_BANK = {
    "Python": [
        {"q": "Which keyword defines a function in Python?", "options": ["def", "func", "function", "lambda"], "answer": "def"},
        {"q": "Which data type stores key-value pairs?", "options": ["list", "tuple", "dict", "set"], "answer": "dict"},
        {"q": "What does OOP stand for?", "options": ["Object Oriented Programming", "Open Online Python", "Ordered Object Process", "Only One Program"], "answer": "Object Oriented Programming"},
        {"q": "Which block handles exceptions?", "options": ["try-except", "if-else", "for-while", "class-def"], "answer": "try-except"},
        {"q": "Which module works with SQLite databases?", "options": ["sqlite3", "sqlpy", "dbLite", "pysql"], "answer": "sqlite3"},
    ],
    "DBMS": [
        {"q": "SQL stands for?", "options": ["Structured Query Language", "Simple Query Logic", "System Query List", "Sequential Question Language"], "answer": "Structured Query Language"},
        {"q": "Which key uniquely identifies a row?", "options": ["Primary Key", "Foreign Key", "Candidate Name", "Index File"], "answer": "Primary Key"},
        {"q": "CRUD means?", "options": ["Create Read Update Delete", "Code Run Upload Download", "Copy Read Use Data", "Class Route User Design"], "answer": "Create Read Update Delete"},
    ],
    "Flask": [
        {"q": "Flask is a Python?", "options": ["Web framework", "Database", "Operating system", "Compiler"], "answer": "Web framework"},
        {"q": "Which decorator maps a URL?", "options": ["@app.route", "@url.map", "@flask.path", "@web.page"], "answer": "@app.route"},
        {"q": "Which function renders HTML templates?", "options": ["render_template", "send_html", "show_page", "template_view"], "answer": "render_template"},
    ],
    "HR Questions": [
        {"q": "Best way to answer 'Tell me about yourself'?", "options": ["Brief structured story", "Only hobbies", "One word", "Salary demand"], "answer": "Brief structured story"},
        {"q": "A good weakness answer should include?", "options": ["Improvement action", "Blame others", "No weakness", "Unrelated jokes"], "answer": "Improvement action"},
    ],
}

for category in [
    "Java", "C Programming", "C++", "Data Structures", "Algorithms", "Operating Systems",
    "Computer Networks", "OOP", "SQL", "HTML", "CSS", "JavaScript", "AI/ML", "Cyber Security"
]:
    INTERVIEW_BANK.setdefault(category, INTERVIEW_BANK["Python"][:3])


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login to continue.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def current_user():
    return User.get(session.get("user_id")) if session.get("user_id") else None


@app.context_processor
def inject_globals():
    return {"current_user": current_user(), "specializations": SPECIALIZATIONS}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            user = User.create(request.form["username"], request.form["email"], request.form["password"])
            session["user_id"] = user.id
            flash("Registration successful. Welcome to Career Compass AI.", "success")
            return redirect(url_for("dashboard"))
        except ValueError as error:
            flash(str(error), "danger")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            user = User.authenticate(request.form["email"], request.form["password"])
            session["user_id"] = user.id
            flash("Login successful.", "success")
            return redirect(url_for("dashboard"))
        except ValueError as error:
            flash(str(error), "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    profile = Profile.get(user_id)
    roadmaps = RoadmapProgress.for_user(user_id)
    scores = InterviewScore.for_user(user_id)
    resume = ResumeAnalysis.latest(user_id)
    activities = Activity.recent(user_id)
    roadmap_percent = round((roadmaps[0]["completed_steps"] / roadmaps[0]["total_steps"]) * 100) if roadmaps else 0
    average_score = round(sum(row["score"] / row["total"] * 100 for row in scores) / len(scores)) if scores else 0
    return render_template(
        "dashboard.html",
        profile=profile,
        roadmaps=roadmaps,
        scores=scores,
        resume=resume,
        activities=activities,
        roadmap_percent=roadmap_percent,
        average_score=average_score,
    )


@app.route("/roadmap", methods=["GET", "POST"])
@login_required
def roadmap():
    selected = request.values.get("specialization", "Artificial Intelligence")
    query = request.args.get("q", "")
    matches = search_specializations(query)
    data = generate_roadmap(selected if selected in SPECIALIZATIONS else matches[0])
    if request.method == "POST":
        completed = int(request.form.get("completed_steps", 0))
        RoadmapProgress.upsert(session["user_id"], data["title"], completed, data["total_steps"])
        flash("Roadmap progress saved.", "success")
        return redirect(url_for("roadmap", specialization=data["title"]))
    return render_template("roadmap.html", roadmap=data, matches=matches, selected=selected, query=query)


@app.route("/interview", methods=["GET", "POST"])
@login_required
def interview():
    category = request.values.get("category", "Python")
    questions = INTERVIEW_BANK.get(category, INTERVIEW_BANK["Python"])
    result = None
    if request.method == "POST":
        score = 0
        for index, question in enumerate(questions):
            if request.form.get(f"q{index}") == question["answer"]:
                score += 1
        InterviewScore.create(session["user_id"], category, score, len(questions))
        percent = round(score / len(questions) * 100)
        result = {"score": score, "total": len(questions), "percent": percent}
        flash(f"Quiz submitted. Score: {score}/{len(questions)}", "success")
    return render_template("interview.html", categories=sorted(INTERVIEW_BANK.keys()), category=category, questions=questions, result=result)


@app.route("/resume", methods=["GET", "POST"])
@login_required
def resume():
    analysis = ResumeAnalysis.latest(session["user_id"])
    if request.method == "POST":
        file = request.files.get("resume")
        if not file or not file.filename.lower().endswith(".pdf"):
            flash("Please upload a PDF resume.", "danger")
            return redirect(url_for("resume"))
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        try:
            result = resume_analyzer.analyze(filepath)
            ResumeAnalysis.create(
                session["user_id"], filename, result["score"], result["category"],
                result["skills"], result["missing_skills"], result["suggestions"]
            )
            flash("Resume analyzed successfully.", "success")
            return redirect(url_for("resume"))
        except ValueError as error:
            flash(str(error), "danger")
    return render_template("resume.html", analysis=analysis)


@app.route("/chatbot", methods=["GET", "POST"])
@login_required
def chatbot_page():
    answer = None
    question = ""
    if request.method == "POST":
        question = request.form.get("message", "")
        answer = chatbot.reply(question)
        Activity.log(session["user_id"], "Asked the AI career assistant")
    return render_template("chatbot.html", answer=answer, question=question)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_row = Profile.get(session["user_id"])
    if request.method == "POST":
        Profile.update(
            session["user_id"],
            request.form.get("full_name", ""),
            request.form.get("college", ""),
            request.form.get("career_goal", ""),
            request.form.get("bio", ""),
        )
        flash("Profile updated.", "success")
        return redirect(url_for("profile"))
    return render_template("profile.html", profile=profile_row)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        db.execute(
            "INSERT INTO contact_messages (name, email, message, created_at) VALUES (?, ?, ?, datetime('now'))",
            (request.form["name"], request.form["email"], request.form["message"]),
            commit=True,
        )
        flash("Thanks. Your message has been saved.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")


@app.errorhandler(404)
def not_found(error):
    return render_template("base.html", error_message="Page not found."), 404


if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    init_db()
    app.run(debug=True)
