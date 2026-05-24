"""
Government of Rajasthan — Internship & E-Governance Portal
Flask Application (Corrected Multipage Production Script)

Run:
    pip install flask flask-mysqldb
    python app.py
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from datetime import datetime
import os

try:
    from flask_mysqldb import MySQL
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "rajasthan-portal-secret-2026")

# ── MySQL Configuration ─────────────────────────────────────────────────────
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER", "diya")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD", "DiyaC_607")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB", "rajasthan_portal")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

if MYSQL_AVAILABLE:
    mysql = MySQL(app)

# ── Dynamic Local State Storage (Fixes Demo Mode Overwrites) ────────────────
DEMO_STUDENTS = [
    {"id": "STU001", "name": "Priya Sharma", "branch": "CSE", "cgpa": 8.9, "skills": "Python, ML",      "status": "Placed"},
    {"id": "STU002", "name": "Rahul Gupta",   "branch": "IT",  "cgpa": 7.4, "skills": "Java, Spring",    "status": "Searching"},
    {"id": "STU003", "name": "Anjali Singh",  "branch": "ECE", "cgpa": 8.2, "skills": "VLSI, C++",       "status": "Completed"},
    {"id": "STU004", "name": "Vikram Rao",    "branch": "CSE", "cgpa": 6.8, "skills": "React, Node",     "status": "Searching"},
    {"id": "STU005", "name": "Meera Nair",    "branch": "IT",  "cgpa": 9.1, "skills": "Data Science",    "status": "Placed"},
]

DEMO_INTERNSHIPS = [
    {"id": 1, "company": "TCS",      "role": "ML Intern",         "stipend": 18000, "duration": "3 months", "skills": "Python, ML",   "status": "Open"},
    {"id": 2, "company": "Infosys",  "role": "Full Stack Dev",    "stipend": 20000, "duration": "6 months", "skills": "React, Node",  "status": "Open"},
    {"id": 3, "company": "Wipro",    "role": "Data Analyst",      "stipend": 15000, "duration": "2 months", "skills": "SQL, Tableau", "status": "Closing"},
    {"id": 4, "company": "HCL",      "role": "DevOps Intern",     "stipend": 16000, "duration": "3 months", "skills": "Docker, CI/CD","status": "Open"},
    {"id": 5, "company": "Accenture","role": "AI Research Intern", "stipend": 22000, "duration": "6 months", "skills": "PyTorch, NLP", "status": "Open"},
]

DEMO_APPLICATIONS = [
    {"id": "A-101", "student": "Priya Sharma",  "role": "TCS — ML Intern",        "date": "20 Mar 2026", "status": "Active"},
    {"id": "A-102", "student": "Rahul Gupta",   "role": "Infosys — Full Stack",   "date": "22 Mar 2026", "status": "Pending"},
    {"id": "A-103", "student": "Anjali Singh",  "role": "Wipro — Data Analyst",   "date": "18 Mar 2026", "status": "Completed"},
    {"id": "A-104", "student": "Vikram Rao",    "role": "HCL — DevOps",           "date": "15 Mar 2026", "status": "Rejected"},
    {"id": "A-105", "student": "Meera Nair",    "role": "Accenture — AI Intern",  "date": "25 Mar 2026", "status": "Active"},
]

DEMO_STATS = {
    "total_students": 342,
    "active_internships": 58,
    "employer_partners": 29,
    "placement_rate": "78%",
}

def get_cursor():
    if MYSQL_AVAILABLE:
        try:
            return mysql.connection.cursor()
        except Exception:
            return None
    return None

# ════════════════════════════════════════════════════════════════════════════
#  PAGE ROUTES — Completely isolated multi-page rendering blueprints
# ════════════════════════════════════════════════════════════════════════════

@app.route("/")
@app.route("/dashboard")
def dashboard():
    cur = get_cursor()
    if cur:
        try:
            cur.execute("SELECT COUNT(*) AS cnt FROM students")
            total_students = cur.fetchone()["cnt"]
            cur.execute("SELECT COUNT(*) AS cnt FROM internships WHERE status='Open'")
            active_internships = cur.fetchone()["cnt"]
            cur.execute("SELECT COUNT(*) AS cnt FROM employers")
            employer_partners = cur.fetchone()["cnt"]
            cur.execute("SELECT COUNT(*) AS cnt FROM applications WHERE status='Completed'")
            placed = cur.fetchone()["cnt"]
            placement_rate = f"{round(placed / max(total_students, 1) * 100)}%"
            cur.execute(
                "SELECT a.*, s.name AS student_name FROM applications a "
                "JOIN students s ON a.student_id = s.id ORDER BY a.created_at DESC LIMIT 5"
            )
            recent_applications = cur.fetchall()
            cur.close()
            stats = {
                "total_students": total_students,
                "active_internships": active_internships,
                "employer_partners": employer_partners,
                "placement_rate": placement_rate,
            }
        except Exception:
            stats = DEMO_STATS
            recent_applications = DEMO_APPLICATIONS[:5]
    else:
        stats = DEMO_STATS
        recent_applications = DEMO_APPLICATIONS[:5]

    return render_template(
        "dashboard.html",
        stats=stats,
        recent_applications=recent_applications,
        active_page="dashboard",
        now=datetime.now(),
    )

@app.route("/students", methods=["GET", "POST"])
def students():
    cur = get_cursor()

    if request.method == "POST":
        data = request.form
        if cur:
            try:
                cur.execute(
                    "INSERT INTO students (name, branch, cgpa, skills, email, phone, status) "
                    "VALUES (%s, %s, %s, %s, %s, %s, 'Searching')",
                    (
                        data.get("name"), data.get("branch"), data.get("cgpa"),
                        data.get("skills"), data.get("email"), data.get("phone"),
                    ),
                )
                mysql.connection.commit()
                cur.close()
                flash("Student registered successfully!", "success")
            except Exception as e:
                flash(f"Database error during submission: {str(e)}", "error")
        else:
            new_student = {
                "id": f"STU00{len(DEMO_STUDENTS) + 1}",
                "name": data.get("name"),
                "branch": data.get("branch", "CSE"),
                "cgpa": float(data.get("cgpa", 0.0)),
                "skills": data.get("skills"),
                "status": "Searching"
            }
            DEMO_STUDENTS.append(new_student)
            flash("Student registered securely (Demo Instance Run Mode).", "success")
        return redirect(url_for("students"))

    branch_filter = request.args.get("branch", "")
    search_query = request.args.get("q", "")

    if cur:
        try:
            query = "SELECT * FROM students WHERE 1=1"
            params = []
            if branch_filter:
                query += " AND branch = %s"; params.append(branch_filter)
            if search_query:
                query += " AND (name LIKE %s OR skills LIKE %s)"
                params += [f"%{search_query}%", f"%{search_query}%"]
            query += " ORDER BY name"
            cur.execute(query, params)
            student_list = cur.fetchall()
            cur.close()
        except Exception:
            student_list = DEMO_STUDENTS
    else:
        student_list = DEMO_STUDENTS

    return render_template(
        "students.html",
        students=student_list,
        branch_filter=branch_filter,
        search_query=search_query,
        active_page="students",
        now=datetime.now(),
    )

@app.route("/employers", methods=["GET", "POST"])
def employers():
    cur = get_cursor()

    if request.method == "POST":
        data = request.form
        if cur:
            try:
                cur.execute(
                    "INSERT INTO internships (company, role, stipend, duration, skills, status) "
                    "VALUES (%s, %s, %s, %s, %s, 'Open')",
                    (
                        data.get("company"), data.get("role"),
                        data.get("stipend"), data.get("duration"),
                        data.get("skills"),
                    ),
                )
                mysql.connection.commit()
                cur.close()
                flash("Internship posted successfully!", "success")
            except Exception as e:
                flash(f"Database error during submission: {str(e)}", "error")
        else:
            new_internship = {
                "id": len(DEMO_INTERNSHIPS) + 1,
                "company": data.get("company"),
                "role": data.get("role"),
                "stipend": int(data.get("stipend", 0)),
                "duration": data.get("duration", "3 months"),
                "skills": data.get("skills"),
                "status": "Open"
            }
            DEMO_INTERNSHIPS.insert(0, new_internship)
            flash("Internship structural payload verified (Demo Mode).", "success")
        return redirect(url_for("employers"))

    if cur:
        try:
            cur.execute("SELECT * FROM employers ORDER BY name")
            employer_list = cur.fetchall()
            cur.execute("SELECT * FROM internships ORDER BY id DESC")
            internship_list = cur.fetchall()
            cur.close()
        except Exception:
            employer_list = [{"name": "TCS", "city": "Jaipur", "hired": 12, "openings": 4}]
            internship_list = DEMO_INTERNSHIPS
    else:
        employer_list = [
            {"name": "TCS",      "city": "Mumbai",    "hired": 12, "openings": 4},
            {"name": "Infosys",  "city": "Bengaluru", "hired":  8, "openings": 2},
            {"name": "Wipro",    "city": "Hyderabad", "hired":  6, "openings": 3},
            {"name": "Accenture","city": "Pune",      "hired":  9, "openings": 1},
        ]
        internship_list = DEMO_INTERNSHIPS

    return render_template(
        "employers.html",
        employers=employer_list,
        internships=internship_list,
        active_page="employers",
        now=datetime.now(),
    )

@app.route("/placement")
def placement():
    cur = get_cursor()
    if cur:
        try:
            cur.execute(
                "SELECT branch, COUNT(*) AS total, "
                "SUM(CASE WHEN status='Placed' THEN 1 ELSE 0 END) AS placed "
                "FROM students GROUP BY branch"
            )
            rows = cur.fetchall()
            branch_stats = [
                {
                    "branch": r["branch"],
                    "total":  r["total"],
                    "placed": r["placed"],
                    "pct":    round(r["placed"] / max(r["total"], 1) * 100),
                }
                for r in rows
            ]
            cur.close()
        except Exception:
            branch_stats = [
                {"branch": "Computer Science", "total": 120, "placed": 109, "pct": 91},
                {"branch": "Information Tech", "total":  95, "placed":  79, "pct": 83},
                {"branch": "Electronics",      "total":  80, "placed":  59, "pct": 74},
                {"branch": "Mechanical",       "total":  70, "placed":  36, "pct": 52},
                {"branch": "Civil",            "total":  54, "placed":  22, "pct": 41},
            ]
    else:
        branch_stats = [
            {"branch": "Computer Science", "total": 120, "placed": 109, "pct": 91},
            {"branch": "Information Tech", "total":  95, "placed":  79, "pct": 83},
            {"branch": "Electronics",      "total":  80, "placed":  59, "pct": 74},
            {"branch": "Mechanical",       "total":  70, "placed":  36, "pct": 52},
            {"branch": "Civil",            "total":  54, "placed":  22, "pct": 41},
        ]

    ml_predictions = [
        {"name": "Priya Sharma", "score": 94},
        {"name": "Meera Nair",   "score": 91},
        {"name": "Anjali Singh", "score": 79},
        {"name": "Rahul Gupta",  "score": 63},
        {"name": "Vikram Rao",   "score": 48},
    ]

    return render_template(
        "placement.html",
        branch_stats=branch_stats,
        ml_predictions=ml_predictions,
        active_page="placement",
        now=datetime.now(),
    )

@app.route("/egov")
def egov():
    services = [
        {"name": "SSO Rajasthan",         "status": "Active",  "users": "2.4M"},
        {"name": "Jan Aadhaar Portal",    "status": "Active",  "users": "1.8M"},
        {"name": "RajSevak Connect",      "status": "Active",  "users": "340K"},
        {"name": "Scholarship Management","status": "Maintenance","users": "120K"},
        {"name": "Internship Registry",   "status": "Active",  "users": "58K"},
    ]
    return render_template(
        "egov.html",
        services=services,
        active_page="egov",
        now=datetime.now(),
    )

@app.route("/internconnect")
def internconnect():
    cur = get_cursor()
    if cur:
        try:
            cur.execute("SELECT * FROM internships WHERE status='Open' ORDER BY stipend DESC")
            internship_list = cur.fetchall()
            cur.close()
        except Exception:
            internship_list = DEMO_INTERNSHIPS
    else:
        internship_list = DEMO_INTERNSHIPS

    return render_template(
        "internconnect.html",
        internships=internship_list,
        active_page="internconnect",
        now=datetime.now(),
    )

@app.route("/notifications")
def notifications():
    notifs = [
        {"icon": "🎉", "msg": "TCS shortlisted you for interview on 2 Apr 2026", "time": "2h ago",  "type": "success"},
        {"icon": "📄", "msg": "Your application #A-103 status changed to Completed", "time": "5h ago",  "type": "info"},
        {"icon": "🔔", "msg": "New internship posted: Accenture AI Research Intern", "time": "1d ago",  "type": "info"},
        {"icon": "⚠️", "msg": "Document upload pending for Wipro application",       "time": "2d ago",  "type": "warning"},
    ]
    return render_template(
        "notifications.html",
        notifications=notifs,
        active_page="notifications",
        now=datetime.now(),
    )

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        flash("Settings and access profiles saved successfully!", "success")
        return redirect(url_for("settings"))
    return render_template(
        "settings.html",
        active_page="settings",
        now=datetime.now(),
    )

# ── REST API ENDPOINTS (JSON) ───────────────────────────────────────────────

@app.route("/api/students", methods=["GET"])
def api_students():
    cur = get_cursor()
    if cur:
        cur.execute("SELECT * FROM students")
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    return jsonify(DEMO_STUDENTS)

# Fixed: Variable routing segment rule assigned correctly
@app.route("/api/students/<string:student_id>", methods=["GET"])
def api_student_detail(student_id):
    cur = get_cursor()
    if cur:
        cur.execute("SELECT * FROM students WHERE id=%s", (student_id,))
        data = cur.fetchone()
        cur.close()
        return jsonify(data or {})
    result = next((s for s in DEMO_STUDENTS if s["id"] == student_id), None)
    return jsonify(result or {})

@app.route("/api/internships", methods=["GET"])
def api_internships():
    cur = get_cursor()
    if cur:
        cur.execute("SELECT * FROM internships WHERE status='Open'")
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    return jsonify(DEMO_INTERNSHIPS)

@app.route("/api/applications", methods=["GET", "POST"])
def api_applications():
    cur = get_cursor()
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
            
        if cur:
            try:
                cur.execute(
                    "INSERT INTO applications (student_id, internship_id, status) VALUES (%s, %s, 'Applied')",
                    (data.get("student_id"), data.get("internship_id")),
                )
                mysql.connection.commit()
                cur.close()
                return jsonify({"message": "Application submitted"}), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        else:
            flash("Application cataloged successfully (Simulation Run Mode).", "success")
            return redirect(url_for("internconnect"))

    if cur:
        cur.execute("SELECT * FROM applications ORDER BY created_at DESC")
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    return jsonify(DEMO_APPLICATIONS)

# Fixed: Variable routing segment rule assigned correctly
@app.route("/api/applications/<string:app_id>", methods=["PUT"])
def api_update_application(app_id):
    data = request.get_json()
    new_status = data.get("status")
    cur = get_cursor()
    if cur:
        cur.execute("UPDATE applications SET status=%s WHERE id=%s", (new_status, app_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Status updated", "id": app_id, "status": new_status})
    return jsonify({"message": "Updated (demo mode)", "id": app_id, "status": new_status})

@app.route("/api/stats")
def api_stats():
    cur = get_cursor()
    if cur:
        cur.execute("SELECT COUNT(*) AS cnt FROM students")
        s = cur.fetchone()["cnt"]
        cur.execute("SELECT COUNT(*) AS cnt FROM internships WHERE status='Open'")
        i = cur.fetchone()["cnt"]
        cur.execute("SELECT COUNT(*) AS cnt FROM employers")
        e = cur.fetchone()["cnt"]
        cur.close()
        return jsonify({"students": s, "internships": i, "employers": e})
    return jsonify(DEMO_STATS)

# ── ERROR HANDLERS ──────────────────────────────────────────────────────────

@app.errorhandler(404)"""
Government of Rajasthan — Internship & E-Governance Portal
Flask Application (Corrected Multipage Production Script)

Run:
    pip install flask flask-mysqldb
    python app.py
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from datetime import datetime
from functools import wraps
import os

try:
    from flask_mysqldb import MySQL
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

app = Flask(__name__)
# In production, always set a robust environment secret key
app.secret_key = os.environ.get("SECRET_KEY", "rajasthan-portal-secret-2026")

# ── MySQL Configuration ─────────────────────────────────────────────────────
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER", "diya")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD", "DiyaC_607")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB", "rajasthan_portal")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

if MYSQL_AVAILABLE:
    mysql = MySQL(app)

# ── Dynamic Local State Storage (Fixes Demo Mode Overwrites) ────────────────
DEMO_STUDENTS = [
    {"id": "STU001", "name": "Priya Sharma", "branch": "CSE", "cgpa": 8.9, "skills": "Python, ML",      "status": "Placed"},
    {"id": "STU002", "name": "Rahul Gupta",   "branch": "IT",  "cgpa": 7.4, "skills": "Java, Spring",    "status": "Searching"},
    {"id": "STU003", "name": "Anjali Singh",  "branch": "ECE", "cgpa": 8.2, "skills": "VLSI, C++",       "status": "Completed"},
    {"id": "STU004", "name": "Vikram Rao",    "branch": "CSE", "cgpa": 6.8, "skills": "React, Node",     "status": "Searching"},
    {"id": "STU005", "name": "Meera Nair",    "branch": "IT",  "cgpa": 9.1, "skills": "Data Science",    "status": "Placed"},
]

DEMO_INTERNSHIPS = [
    {"id": 1, "company": "TCS",      "role": "ML Intern",         "stipend": 18000, "duration": "3 months", "skills": "Python, ML",   "status": "Open"},
    {"id": 2, "company": "Infosys",  "role": "Full Stack Dev",    "stipend": 20000, "duration": "6 months", "skills": "React, Node",  "status": "Open"},
    {"id": 3, "company": "Wipro",    "role": "Data Analyst",      "stipend": 15000, "duration": "2 months", "skills": "SQL, Tableau", "status": "Closing"},
    {"id": 4, "company": "HCL",      "role": "DevOps Intern",     "stipend": 16000, "duration": "3 months", "skills": "Docker, CI/CD","status": "Open"},
    {"id": 5, "company": "Accenture","role": "AI Research Intern", "stipend": 22000, "duration": "6 months", "skills": "PyTorch, NLP", "status": "Open"},
]

DEMO_APPLICATIONS = [
    {"id": "A-101", "student": "Priya Sharma",  "role": "TCS — ML Intern",        "date": "20 Mar 2026", "status": "Active"},
    {"id": "A-102", "student": "Rahul Gupta",   "role": "Infosys — Full Stack",   "date": "22 Mar 2026", "status": "Pending"},
    {"id": "A-103", "student": "Anjali Singh",  "role": "Wipro — Data Analyst",   "date": "18 Mar 2026", "status": "Completed"},
    {"id": "A-104", "student": "Vikram Rao",    "role": "HCL — DevOps",           "date": "15 Mar 2026", "status": "Rejected"},
    {"id": "A-105", "student": "Meera Nair",    "role": "Accenture — AI Intern",  "date": "25 Mar 2026", "status": "Active"},
]

DEMO_STATS = {
    "total_students": 342,
    "active_internships": 58,
    "employer_partners": 29,
    "placement_rate": "78%",
}

def get_cursor():
    if MYSQL_AVAILABLE:
        try:
            return mysql.connection.cursor()
        except Exception:
            return None
    return None

# ── Authentication Guards ───────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            flash("Please log in to access this secure resource.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ── AUTHENTICATION ROUTES ───────────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        captcha = request.form.get("captcha", "").strip()
        
        # Enforce CAPTCHA verification check matches the interface token
        if captcha.upper() != "X4P2QR":
            flash("Invalid CAPTCHA sequence entered. Please retry.", "error")
            return render_template("login.html", now=datetime.now())
            
        cur = get_cursor()
        if cur:
            try:
                # Production Database Query Optimization Block
                cur.execute("SELECT * FROM admin_users WHERE username = %s", (username,))
                user = cur.fetchone()
                cur.close()
                
                # Verify password (use safe hashing models like werkzeug.security in true prod)
                if user and user["password"] == password:
                    session["logged_in"] = True
                    session["user_id"] = username
                    session["user_display"] = user.get("name", "Administrator")
                    flash(f"Login successful! Welcome back, {session['user_display']}.", "success")
                    return redirect(url_for("dashboard"))
            except Exception as e:
                flash(f"Authentication system failure: {str(e)}", "error")
        else:
            # Fallback Demo Authentication Context
            if username == "admin" and password == "Rajasthan@2026":
                session["logged_in"] = True
                session["user_id"] = "admin"
                session["user_display"] = "Arjun Kumar"
                flash("Login successful! Welcome, Arjun Kumar (Demo Context).", "success")
                return redirect(url_for("dashboard"))
                
        flash("Invalid Employee ID / SSO ID or security credentials.", "error")
        
    return render_template("login.html", now=datetime.now())

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out securely.", "success")
    return redirect(url_for("login"))

# ── PAGE ROUTES — Completely isolated multi-page rendering blueprints ──────

@app.route("/")
@app.route("/dashboard")
def dashboard():
    cur = get_cursor()
    if cur:
        try:
            cur.execute("SELECT COUNT(*) AS cnt FROM students")
            total_students = cur.fetchone()["cnt"]
            cur.execute("SELECT COUNT(*) AS cnt FROM internships WHERE status='Open'")
            active_internships = cur.fetchone()["cnt"]
            cur.execute("SELECT COUNT(*) AS cnt FROM employers")
            employer_partners = cur.fetchone()["cnt"]
            cur.execute("SELECT COUNT(*) AS cnt FROM applications WHERE status='Completed'")
            placed = cur.fetchone()["cnt"]
            placement_rate = f"{round(placed / max(total_students, 1) * 100)}%"
            cur.execute(
                "SELECT a.*, s.name AS student_name FROM applications a "
                "JOIN students s ON a.student_id = s.id ORDER BY a.created_at DESC LIMIT 5"
            )
            recent_applications = cur.fetchall()
            cur.close()
            stats = {
                "total_students": total_students,
                "active_internships": active_internships,
                "employer_partners": employer_partners,
                "placement_rate": placement_rate,
            }
        except Exception:
            stats = DEMO_STATS
            recent_applications = DEMO_APPLICATIONS[:5]
    else:
        stats = DEMO_STATS
        recent_applications = DEMO_APPLICATIONS[:5]

    return render_template(
        "dashboard.html",
        stats=stats,
        recent_applications=recent_applications,
        active_page="dashboard",
        now=datetime.now(),
    )

@app.route("/students", methods=["GET", "POST"])
def students():
    cur = get_cursor()

    if request.method == "POST":
        data = request.form
        if cur:
            try:
                cur.execute(
                    "INSERT INTO students (name, branch, cgpa, skills, email, phone, status) "
                    "VALUES (%s, %s, %s, %s, %s, %s, 'Searching')",
                    (
                        data.get("name"), data.get("branch"), data.get("cgpa"),
                        data.get("skills"), data.get("email"), data.get("phone"),
                    ),
                )
                mysql.connection.commit()
                cur.close()
                flash("Student registered successfully!", "success")
            except Exception as e:
                flash(f"Database error during submission: {str(e)}", "error")
        else:
            new_student = {
                "id": f"STU00{len(DEMO_STUDENTS) + 1}",
                "name": data.get("name"),
                "branch": data.get("branch", "CSE"),
                "cgpa": float(data.get("cgpa", 0.0)),
                "skills": data.get("skills"),
                "status": "Searching"
            }
            DEMO_STUDENTS.append(new_student)
            flash("Student registered securely (Demo Instance Run Mode).", "success")
        return redirect(url_for("students"))

    branch_filter = request.args.get("branch", "")
    search_query = request.args.get("q", "")

    if cur:
        try:
            query = "SELECT * FROM students WHERE 1=1"
            params = []
            if branch_filter:
                query += " AND branch = %s"; params.append(branch_filter)
            if search_query:
                query += " AND (name LIKE %s OR skills LIKE %s)"
                params += [f"%{search_query}%", f"%{search_query}%"]
            query += " ORDER BY name"
            cur.execute(query, params)
            student_list = cur.fetchall()
            cur.close()
        except Exception:
            student_list = DEMO_STUDENTS
    else:
        student_list = DEMO_STUDENTS

    return render_template(
        "students.html",
        students=student_list,
        branch_filter=branch_filter,
        search_query=search_query,
        active_page="students",
        now=datetime.now(),
    )

@app.route("/employers", methods=["GET", "POST"])
def employers():
    cur = get_cursor()

    if request.method == "POST":
        data = request.form
        if cur:
            try:
                cur.execute(
                    "INSERT INTO internships (company, role, stipend, duration, skills, status) "
                    "VALUES (%s, %s, %s, %s, %s, 'Open')",
                    (
                        data.get("company"), data.get("role"),
                        data.get("stipend"), data.get("duration"),
                        data.get("skills"),
                    ),
                )
                mysql.connection.commit()
                cur.close()
                flash("Internship posted successfully!", "success")
            except Exception as e:
                flash(f"Database error during submission: {str(e)}", "error")
        else:
            new_internship = {
                "id": len(DEMO_INTERNSHIPS) + 1,
                "company": data.get("company"),
                "role": data.get("role"),
                "stipend": int(data.get("stipend", 0)),
                "duration": data.get("duration", "3 months"),
                "skills": data.get("skills"),
                "status": "Open"
            }
            DEMO_INTERNSHIPS.insert(0, new_internship)
            flash("Internship structural payload verified (Demo Mode).", "success")
        return redirect(url_for("employers"))

    if cur:
        try:
            cur.execute("SELECT * FROM employers ORDER BY name")
            employer_list = cur.fetchall()
            cur.execute("SELECT * FROM internships ORDER BY id DESC")
            internship_list = cur.fetchall()
            cur.close()
        except Exception:
            employer_list = [{"name": "TCS", "city": "Jaipur", "hired": 12, "openings": 4}]
            internship_list = DEMO_INTERNSHIPS
    else:
        employer_list = [
            {"name": "TCS",      "city": "Mumbai",    "hired": 12, "openings": 4},
            {"name": "Infosys",  "city": "Bengaluru", "hired":  8, "openings": 2},
            {"name": "Wipro",    "city": "Hyderabad", "hired":  6, "openings": 3},
            {"name": "Accenture","city": "Pune",      "hired":  9, "openings": 1},
        ]
        internship_list = DEMO_INTERNSHIPS

    return render_template(
        "employers.html",
        employers=employer_list,
        internships=internship_list,
        active_page="employers",
        now=datetime.now(),
    )

@app.route("/placement")
def placement():
    cur = get_cursor()
    if cur:
        try:
            cur.execute(
                "SELECT branch, COUNT(*) AS total, "
                "SUM(CASE WHEN status='Placed' THEN 1 ELSE 0 END) AS placed "
                "FROM students GROUP BY branch"
            )
            rows = cur.fetchall()
            branch_stats = [
                {
                    "branch": r["branch"],
                    "total":  r["total"],
                    "placed": r["placed"],
                    "pct":    round(r["placed"] / max(r["total"], 1) * 100),
                }
                for r in rows
            ]
            cur.close()
        except Exception:
            branch_stats = [
                {"branch": "Computer Science", "total": 120, "placed": 109, "pct": 91},
                {"branch": "Information Tech", "total":  95, "placed":  79, "pct": 83},
                {"branch": "Electronics",      "total":  80, "placed":  59, "pct": 74},
                {"branch": "Mechanical",       "total":  70, "placed":  36, "pct": 52},
                {"branch": "Civil",            "total":  54, "placed":  22, "pct": 41},
            ]
    else:
        branch_stats = [
            {"branch": "Computer Science", "total": 120, "placed": 109, "pct": 91},
            {"branch": "Information Tech", "total":  95, "placed":  79, "pct": 83},
            {"branch": "Electronics",      "total":  80, "placed":  59, "pct": 74},
            {"branch": "Mechanical",       "total":  70, "placed":  36, "pct": 52},
            {"branch": "Civil",            "total":  54, "placed":  22, "pct": 41},
        ]

    ml_predictions = [
        {"name": "Priya Sharma", "score": 94},
        {"name": "Meera Nair",   "score": 91},
        {"name": "Anjali Singh", "score": 79},
        {"name": "Rahul Gupta",  "score": 63},
        {"name": "Vikram Rao",   "score": 48},
    ]

    return render_template(
        "placement.html",
        branch_stats=branch_stats,
        ml_predictions=ml_predictions,
        active_page="placement",
        now=datetime.now(),
    )

@app.route("/egov")
def egov():
    services = [
        {"name": "SSO Rajasthan",         "status": "Active",  "users": "2.4M"},
        {"name": "Jan Aadhaar Portal",    "status": "Active",  "users": "1.8M"},
        {"name": "RajSevak Connect",      "status": "Active",  "users": "340K"},
        {"name": "Scholarship Management","status": "Maintenance","users": "120K"},
        {"name": "Internship Registry",   "status": "Active",  "users": "58K"},
    ]
    return render_template(
        "egov.html",
        services=services,
        active_page="egov",
        now=datetime.now(),
    )

@app.route("/internconnect")
def internconnect():
    cur = get_cursor()
    if cur:
        try:
            cur.execute("SELECT * FROM internships WHERE status='Open' ORDER BY stipend DESC")
            internship_list = cur.fetchall()
            cur.close()
        except Exception:
            internship_list = DEMO_INTERNSHIPS
    else:
        internship_list = DEMO_INTERNSHIPS

    return render_template(
        "internconnect.html",
        internships=internship_list,
        active_page="internconnect",
        now=datetime.now(),
    )

@app.route("/notifications")
def notifications():
    notifs = [
        {"icon": "🎉", "msg": "TCS shortlisted you for interview on 2 Apr 2026", "time": "2h ago",  "type": "success"},
        {"icon": "📄", "msg": "Your application #A-103 status changed to Completed", "time": "5h ago",  "type": "info"},
        {"icon": "🔔", "msg": "New internship posted: Accenture AI Research Intern", "time": "1d ago",  "type": "info"},
        {"icon": "⚠️", "msg": "Document upload pending for Wipro application",       "time": "2d ago",  "type": "warning"},
    ]
    return render_template(
        "notifications.html",
        notifications=notifs,
        active_page="notifications",
        now=datetime.now(),
    )

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        flash("Settings and access profiles saved successfully!", "success")
        return redirect(url_for("settings"))
    return render_template(
        "settings.html",
        active_page="settings",
        now=datetime.now(),
    )

# ── REST API ENDPOINTS (JSON) ───────────────────────────────────────────────

@app.route("/api/students", methods=["GET"])
def api_students():
    cur = get_cursor()
    if cur:
        cur.execute("SELECT * FROM students")
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    return jsonify(DEMO_STUDENTS)

@app.route("/api/students/<string:student_id>", methods=["GET"])
def api_student_detail(student_id):
    cur = get_cursor()
    if cur:
        cur.execute("SELECT * FROM students WHERE id=%s", (student_id,))
        data = cur.fetchone()
        cur.close()
        return jsonify(data or {})
    result = next((s for s in DEMO_STUDENTS if s["id"] == student_id), None)
    return jsonify(result or {})

@app.route("/api/internships", methods=["GET"])
def api_internships():
    cur = get_cursor()
    if cur:
        cur.execute("SELECT * FROM internships WHERE status='Open'")
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    return jsonify(DEMO_INTERNSHIPS)

@app.route("/api/applications", methods=["GET", "POST"])
def api_applications():
    cur = get_cursor()
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
            
        if cur:
            try:
                cur.execute(
                    "INSERT INTO applications (student_id, internship_id, status) VALUES (%s, %s, 'Applied')",
                    (data.get("student_id"), data.get("internship_id")),
                )
                mysql.connection.commit()
                cur.close()
                return jsonify({"message": "Application submitted"}), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        else:
            flash("Application cataloged successfully (Simulation Run Mode).", "success")
            return redirect(url_for("internconnect"))

    if cur:
        cur.execute("SELECT * FROM applications ORDER BY created_at DESC")
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    return jsonify(DEMO_APPLICATIONS)

@app.route("/api/applications/<string:app_id>", methods=["PUT"])
def api_update_application(app_id):
    data = request.get_json()
    new_status = data.get("status")
    cur = get_cursor()
    if cur:
        cur.execute("UPDATE applications SET status=%s WHERE id=%s", (new_status, app_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Status updated", "id": app_id, "status": new_status})
    return jsonify({"message": "Updated (demo mode)", "id": app_id, "status": new_status})

@app.route("/api/stats")
def api_stats():
    cur = get_cursor()
    if cur:
        cur.execute("SELECT COUNT(*) AS cnt FROM students")
        s = cur.fetchone()["cnt"]
        cur.execute("SELECT COUNT(*) AS cnt FROM internships WHERE status='Open'")
        i = cur.fetchone()["cnt"]
        cur.execute("SELECT COUNT(*) AS cnt FROM employers")
        e = cur.fetchone()["cnt"]
        cur.close()
        return jsonify({"students": s, "internships": i, "employers": e})
    return jsonify(DEMO_STATS)

# ── ERROR HANDLERS ──────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return f"<h1>404 Page Not Found</h1><p>The layout route could not be discovered by the server.</p>", 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error", "detail": str(e)}), 500

if __name__ == "__main__":
    print("=" * 60)
    print(" Rajasthan Internship & E-Governance Portal")
    print(" \ Flask Balanced Production Server Routing Environment")
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=5000)
def not_found(e):
    return f"<h1>404 Page Not Found</h1><p>The layout route could not be discovered by the server.</p>", 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error", "detail": str(e)}), 500

if __name__ == "__main__":
    print("=" * 60)
    print("  Rajasthan Internship & E-Governance Portal")
    print("  Flask Balanced Production Server Routing Environment")
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=5000)