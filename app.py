from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import json, os, hashlib, re
from datetime import datetime

app = Flask(__name__)
app.secret_key = "epicalexam-secret-key-2024"

# ── Data store helpers ─────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
CANDIDATES_FILE = os.path.join(BASE_DIR, "candidates.json")
EXAMS_FILE      = os.path.join(BASE_DIR, "exams.json")
RESULTS_FILE    = os.path.join(BASE_DIR, "results.json")


def _load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def _save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_candidates():
    return _load_json(CANDIDATES_FILE)

def save_candidates(candidates):
    _save_json(CANDIDATES_FILE, candidates)

def load_exams():
    return _load_json(EXAMS_FILE)

def load_results():
    return _load_json(RESULTS_FILE)

def save_results(results):
    _save_json(RESULTS_FILE, results)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ── Auth helper ────────────────────────────────────────────────────────────────
def get_current_user():
    """Return the logged-in user dict or None."""
    if "user_id" not in session:
        return None
    candidates = load_candidates()
    return next((c for c in candidates if c["id"] == session["user_id"]), None)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return redirect(url_for("register"))


# ── Register ───────────────────────────────────────────────────────────────────
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        candidates = load_candidates()

        first_name     = request.form.get("first_name", "").strip()
        last_name      = request.form.get("last_name", "").strip()
        email          = request.form.get("email", "").strip().lower()
        phone          = request.form.get("phone", "").strip()
        dob            = request.form.get("dob", "")
        gender         = request.form.get("gender", "")
        roll_no        = request.form.get("roll_no", "").strip().upper()
        department     = request.form.get("department", "")
        year           = request.form.get("year", "")
        institution    = request.form.get("institution", "").strip()
        city           = request.form.get("city", "").strip()
        password       = request.form.get("password", "")
        confirm_pwd    = request.form.get("confirm_password", "")
        terms          = request.form.get("terms")

        errors = []
        if not first_name or len(first_name) < 2:
            errors.append("First name must be at least 2 characters.")
        if not last_name or len(last_name) < 2:
            errors.append("Last name must be at least 2 characters.")
        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            errors.append("Invalid email address.")
        if any(c["email"] == email for c in candidates):
            errors.append("An account with this email already exists.")
        if any(c["roll_no"] == roll_no for c in candidates):
            errors.append("Roll number is already registered.")
        if not re.match(r"^(?=.*[A-Z])(?=.*\d).{8,}$", password):
            errors.append("Password must be at least 8 characters with 1 uppercase and 1 number.")
        if password != confirm_pwd:
            errors.append("Passwords do not match.")
        if not terms:
            errors.append("You must agree to the Terms of Service.")

        if errors:
            for err in errors:
                flash(err, "danger")
            return redirect(url_for("register"))

        new_candidate = {
            "id":          len(candidates) + 1,
            "name":        f"{first_name} {last_name}",
            "first_name":  first_name,
            "last_name":   last_name,
            "email":       email,
            "password":    hash_password(password),
            "phone":       phone,
            "dob":         dob,
            "gender":      gender,
            "roll_no":     roll_no,
            "department":  department,
            "year":        int(year) if year.isdigit() else 1,
            "institution": institution,
            "city":        city,
            "status":      "active",
            "exams_attempted": 0,
            "registered_at": datetime.utcnow().isoformat()
        }

        candidates.append(new_candidate)
        save_candidates(candidates)

        flash(f"🎉 Welcome, {first_name}! Your account has been created successfully.", "success")
        return redirect(url_for("success", name=first_name))

    return render_template("register.html")


# ── Success ────────────────────────────────────────────────────────────────────
@app.route("/success")
def success():
    name = request.args.get("name", "Candidate")
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8"/>
      <title>Registered! | EpicalExam</title>
      <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;800&display=swap" rel="stylesheet"/>
      <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Outfit', sans-serif; background: #0a0a1a; color: #f1f5f9;
                display: flex; align-items: center; justify-content: center; min-height: 100vh;
                background: radial-gradient(ellipse at 20% 30%, rgba(124,58,237,.25), transparent 60%),
                            radial-gradient(ellipse at 80% 80%, rgba(6,182,212,.15), transparent 60%), #0a0a1a; }}
        .card {{ text-align: center; padding: 60px 48px; background: rgba(255,255,255,.05);
                 border: 1px solid rgba(255,255,255,.12); border-radius: 28px;
                 backdrop-filter: blur(20px); max-width: 480px; }}
        .icon {{ font-size: 72px; margin-bottom: 24px; animation: pop .4s ease; }}
        @keyframes pop {{ from {{ transform: scale(0); }} to {{ transform: scale(1); }} }}
        h1 {{ font-size: 32px; font-weight: 800; background: linear-gradient(135deg,#fff,#a78bfa);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px; }}
        p  {{ color: #94a3b8; font-size: 15px; line-height: 1.6; }}
        a  {{ display: inline-block; margin-top: 32px; padding: 14px 36px;
               background: linear-gradient(135deg,#7c3aed,#06b6d4); color: white;
               border-radius: 14px; text-decoration: none; font-weight: 600; font-size: 15px;
               transition: transform .2s, box-shadow .2s; }}
        a:hover {{ transform: translateY(-2px); box-shadow: 0 8px 24px rgba(124,58,237,.4); }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="icon">🎉</div>
        <h1>Welcome, {name}!</h1>
        <p>Your EpicalExam account has been created successfully.<br>
           You can now log in and start taking exams.</p>
        <a href="/login">Go to Login</a>
        <a href="/register" style="background:rgba(255,255,255,0.1);margin-left:12px;">Register Another</a>
      </div>
    </body>
    </html>
    """


# ── Login ──────────────────────────────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        candidates = load_candidates()
        user = next((c for c in candidates if c["email"] == email), None)

        if user and user["password"] == hash_password(password):
            session["user_id"]    = user["id"]
            session["user_name"]  = user["name"]
            session["user_email"] = user["email"]
            flash(f"Welcome back, {user['name']}! 🎉", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password. Please try again.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


# ── Dashboard ──────────────────────────────────────────────────────────────────
@app.route("/dashboard")
def dashboard():
    user = get_current_user()
    if not user:
        flash("Please log in to access the dashboard.", "danger")
        return redirect(url_for("login"))

    exams   = load_exams()
    results = load_results()

    # Results for this user
    user_results = [r for r in results if r["user_id"] == user["id"]]
    completed_exam_ids = [r["exam_id"] for r in user_results]

    # Stats
    total_attempted = len(user_results)
    total_passed    = sum(1 for r in user_results if r["passed"])
    avg_score       = round(sum(r["percentage"] for r in user_results) / total_attempted, 1) if total_attempted else 0

    # Mark exams as completed or available
    for exam in exams:
        exam["completed"] = exam["id"] in completed_exam_ids
        result = next((r for r in user_results if r["exam_id"] == exam["id"]), None)
        exam["user_result"] = result

    return render_template("dashboard.html",
        candidate=user,
        exams=exams,
        user_results=user_results,
        total_attempted=total_attempted,
        total_passed=total_passed,
        avg_score=avg_score
    )


# ── Exam: Start / Take ────────────────────────────────────────────────────────
@app.route("/exam/<int:exam_id>")
def take_exam(exam_id):
    user = get_current_user()
    if not user:
        flash("Please log in to take an exam.", "danger")
        return redirect(url_for("login"))

    exams = load_exams()
    exam  = next((e for e in exams if e["id"] == exam_id), None)
    if not exam:
        flash("Exam not found.", "danger")
        return redirect(url_for("dashboard"))

    # Check if already attempted
    results = load_results()
    already_done = any(r for r in results if r["user_id"] == user["id"] and r["exam_id"] == exam_id)
    if already_done:
        flash("You have already completed this exam.", "info")
        return redirect(url_for("dashboard"))

    # Store exam start time in session
    session["exam_id"]      = exam_id
    session["exam_start"]   = datetime.utcnow().isoformat()

    # Send questions WITHOUT correct answers to the template
    safe_questions = []
    for q in exam["questions"]:
        safe_questions.append({
            "id":      q["id"],
            "text":    q["text"],
            "options": q["options"]
        })

    exam_data = {
        "id":          exam["id"],
        "name":        exam["name"],
        "subject":     exam["subject"],
        "duration":    exam["duration"],
        "total_marks": exam["total_marks"],
        "total_questions": len(exam["questions"]),
        "questions":   safe_questions
    }

    return render_template("exam.html", exam=exam_data, candidate=user)


# ── Exam: Submit ───────────────────────────────────────────────────────────────
@app.route("/exam/<int:exam_id>/submit", methods=["POST"])
def submit_exam(exam_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401

    exams = load_exams()
    exam  = next((e for e in exams if e["id"] == exam_id), None)
    if not exam:
        return jsonify({"error": "Exam not found"}), 404

    # Check if already submitted
    results = load_results()
    already_done = any(r for r in results if r["user_id"] == user["id"] and r["exam_id"] == exam_id)
    if already_done:
        return jsonify({"error": "Exam already submitted"}), 400

    # Get submitted answers
    try:
        submitted = request.get_json()
        answers = submitted.get("answers", {})
        tab_switches = submitted.get("tab_switches", 0)
    except Exception:
        answers = {}
        tab_switches = 0

    # Grade the exam
    score = 0
    total = len(exam["questions"])
    question_results = []

    for q in exam["questions"]:
        q_id = str(q["id"])
        selected = answers.get(q_id)
        is_correct = (selected is not None and int(selected) == q["correct"])
        if is_correct:
            score += 1
        question_results.append({
            "question_id": q["id"],
            "question_text": q["text"],
            "options": q["options"],
            "selected": selected if selected is not None else -1,
            "correct": q["correct"],
            "is_correct": is_correct
        })

    percentage = round((score / total) * 100, 1) if total > 0 else 0
    passed = percentage >= exam["pass_percentage"]

    # Calculate time taken
    start_time = session.get("exam_start")
    if start_time:
        started = datetime.fromisoformat(start_time)
        time_taken = int((datetime.utcnow() - started).total_seconds())
    else:
        time_taken = 0

    # Build result record
    result_record = {
        "id":              len(results) + 1,
        "user_id":         user["id"],
        "user_name":       user["name"],
        "exam_id":         exam["id"],
        "exam_name":       exam["name"],
        "score":           score,
        "total":           total,
        "percentage":      percentage,
        "passed":          passed,
        "answers":         answers,
        "question_results": question_results,
        "tab_switches":    tab_switches,
        "time_taken_seconds": time_taken,
        "submitted_at":    datetime.utcnow().isoformat()
    }

    results.append(result_record)
    save_results(results)

    # Update candidate's exams_attempted count
    candidates = load_candidates()
    for c in candidates:
        if c["id"] == user["id"]:
            c["exams_attempted"] = c.get("exams_attempted", 0) + 1
            break
    save_candidates(candidates)

    # Clear exam session
    session.pop("exam_id", None)
    session.pop("exam_start", None)

    return jsonify({
        "success":    True,
        "result_id":  result_record["id"],
        "score":      score,
        "total":      total,
        "percentage": percentage,
        "passed":     passed,
        "time_taken": time_taken
    })


# ── Result: View Detail ───────────────────────────────────────────────────────
@app.route("/result/<int:result_id>")
def view_result(result_id):
    user = get_current_user()
    if not user:
        flash("Please log in to view results.", "danger")
        return redirect(url_for("login"))

    results = load_results()
    result  = next((r for r in results if r["id"] == result_id and r["user_id"] == user["id"]), None)
    if not result:
        flash("Result not found.", "danger")
        return redirect(url_for("dashboard"))

    return render_template("result.html", result=result, candidate=user)


# ── Logout ─────────────────────────────────────────────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
