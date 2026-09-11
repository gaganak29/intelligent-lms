import os
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from database import (
    init_db, get_db_connection, get_or_create_default_student,
    get_student_profile, authenticate_student, create_student, fetch_unique_test_questions,
    record_test_result, record_game_score
)
from summarizer import textrank_summarize
from map_generator import generate_visual_map
from ml_engine import get_student_performance_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'intelligent-lms-secret-key-cse-2026'

# Initialize database tables on startup
with app.app_context():
    init_db()

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'student_id' not in session:
            return redirect(url_for('login', next=request.path))
        return view(*args, **kwargs)
    return wrapped_view

def current_student():
    return get_student_profile(session['student_id'])

# -------------------------------------------------------------
# CORE ROUTES
# -------------------------------------------------------------
@app.route('/')
def home():
    """Shows login first, then the authenticated student's dashboard."""
    if 'student_id' not in session:
        return redirect(url_for('login'))
    student = current_student()
    perf = get_student_performance_data(student['id'], student['category'])
    return render_template(
        'index.html',
        student=student,
        perf=perf,
        hs_data=perf,
        puc_data=perf,
        hs_student=student,
        puc_student=student
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            student_id = int(request.form.get('student_id', '').strip())
        except ValueError:
            student_id = 0
        student = authenticate_student(student_id, request.form.get('password', ''))
        if student:
            session.clear()
            session['student_id'] = student['id']
            destination = request.args.get('next') or url_for('home')
            return redirect(destination)
        error = 'Invalid Student ID or password.'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not name or category not in ('highschool', 'puc_degree') or len(password) < 6:
            error = 'Enter a name, choose a category, and use a password of at least 6 characters.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        else:
            student_id = create_student(name, category, password)
            session.clear()
            session['student_id'] = student_id
            return redirect(url_for('home'))

    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/about')
def about():
    """Project documentation, architecture, genuine IEEE citations, and viva guide."""
    return render_template('about.html')

# -------------------------------------------------------------
# HIGH SCHOOL MODULES
# -------------------------------------------------------------
@app.route('/highschool')
@login_required
def highschool_dashboard():
    """High School Student Hub: 4 Core Modules + Performance Card."""
    student = current_student()
    if student['category'] != 'highschool':
        return redirect(url_for('puc_degree_dashboard'))
    student_id = student['id']
    perf = get_student_performance_data(student_id, 'highschool')
    return render_template('highschool/dashboard.html', perf=perf)

@app.route('/highschool/test')
@login_required
def highschool_test():
    """50-Question Subject-based MCQ Test."""
    student_id = current_student()['id']
    return render_template('highschool/test.html', student_id=student_id)

@app.route('/highschool/games')
@login_required
def highschool_games():
    """Interactive Educational & IQ Games arena."""
    student_id = current_student()['id']
    return render_template('highschool/games.html', student_id=student_id)

@app.route('/highschool/map-method')
@login_required
def highschool_map_method():
    """Theory-to-Visual Map generator."""
    return render_template('highschool/map_method.html')

@app.route('/highschool/newspaper')
@login_required
def highschool_newspaper():
    """TextRank Newspaper Summarizer & Infographic generator."""
    return render_template('highschool/newspaper.html')

@app.route('/highschool/performance')
@login_required
def highschool_performance():
    """Self-assessment student performance analysis & adaptive recommendations."""
    student = current_student()
    if student['category'] != 'highschool':
        return redirect(url_for('puc_degree_performance'))
    student_id = student['id']
    perf = get_student_performance_data(student_id, 'highschool')
    return render_template('highschool/performance.html', perf=perf)

# -------------------------------------------------------------
# PUC & DEGREE MODULES
# -------------------------------------------------------------
@app.route('/puc-degree')
@login_required
def puc_degree_dashboard():
    """PUC & Degree Student Hub."""
    student = current_student()
    if student['category'] != 'puc_degree':
        return redirect(url_for('highschool_dashboard'))
    student_id = student['id']
    perf = get_student_performance_data(student_id, 'puc_degree')
    return render_template('puc_degree/dashboard.html', perf=perf)

@app.route('/puc-degree/test')
@login_required
def puc_degree_test():
    """100-Question Technical & Logical Assessment."""
    student_id = current_student()['id']
    return render_template('puc_degree/test.html', student_id=student_id)

@app.route('/puc-degree/performance')
@login_required
def puc_degree_performance():
    """Technical performance dashboard with Chart.js analytics & recommendations."""
    student = current_student()
    if student['category'] != 'puc_degree':
        return redirect(url_for('highschool_performance'))
    student_id = student['id']
    perf = get_student_performance_data(student_id, 'puc_degree')
    return render_template('puc_degree/performance.html', perf=perf)

# -------------------------------------------------------------
# REST API ENDPOINTS
# -------------------------------------------------------------
@app.route('/api/questions', methods=['GET'])
def api_get_questions():
    """
    Returns unique questions for a test session.
    Strictly guarantees NO duplicates within the active test set.
    """
    category = request.args.get('category', 'highschool')
    requested_count = request.args.get('count')
    if requested_count in (None, '', 'all'):
        count = 300
    else:
        count = max(1, int(requested_count))
    subject = request.args.get('subject', None)

    questions = fetch_unique_test_questions(category, count=count, subject=subject)

    # Re-number with serial numbers 1 to count
    formatted = []
    for idx, q in enumerate(questions, start=1):
        item = dict(q)
        item['serial_number'] = idx
        formatted.append(item)

    return jsonify({
        "status": "success",
        "category": category,
        "count": len(formatted),
        "questions": formatted
    })

@app.route('/api/submit-test', methods=['POST'])
def api_submit_test():
    """
    Evaluates submitted test answers, persists record to SQLite,
    and returns comprehensive evaluation metrics.
    """
    data = request.get_json() or {}
    if 'student_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please log in first'}), 401
    category = data.get('category', 'highschool')
    student_id = session['student_id']
    student = current_student()
    if student['category'] != category or data.get('student_id') not in (None, student_id):
        return jsonify({'status': 'error', 'message': 'Student session does not match this test'}), 403
    test_title = data.get('test_title', 'General Subject Assessment' if category == 'highschool' else 'Logical & Technical Assessment')
    answers_data = data.get('answers', [])

    result = record_test_result(student_id, category, test_title, answers_data)
    return jsonify({
        "status": "success",
        "result": result
    })

@app.route('/api/save-game-score', methods=['POST'])
def api_save_game_score():
    """Stores educational game results in database."""
    data = request.get_json() or {}
    if 'student_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please log in first'}), 401
    category = data.get('category', 'highschool')
    student_id = session['student_id']
    if current_student()['category'] != category:
        return jsonify({'status': 'error', 'message': 'Student session does not match this game'}), 403
    game_type = data.get('game_type', 'IQ Game')
    subject = data.get('subject', 'General')
    score = int(data.get('score', 0))
    max_score = int(data.get('max_score', 100))
    time_taken = int(data.get('time_taken', 0))

    game_id = record_game_score(student_id, game_type, subject, score, max_score, time_taken)
    return jsonify({
        "status": "success",
        "game_id": game_id,
        "message": "Game score recorded successfully!"
    })

@app.route('/api/summarize-news', methods=['POST'])
def api_summarize_news():
    """TextRank extractive summarization API."""
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    if not text:
        return jsonify({"status": "error", "message": "Please enter article text"}), 400

    result = textrank_summarize(text)
    return jsonify({
        "status": "success",
        "data": result
    })

@app.route('/api/generate-map', methods=['POST'])
def api_generate_map():
    """Dynamic theory-to-visual map generation API."""
    data = request.get_json() or {}
    text = data.get('theory_text', '').strip()
    if not text:
        return jsonify({"status": "error", "message": "Please enter theory text"}), 400

    result = generate_visual_map(text)
    return jsonify({
        "status": "success",
        "data": result
    })

@app.route('/api/performance/<category>')
def api_get_performance(category):
    """Returns real-time performance metrics for Chart.js graphing."""
    if 'student_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please log in first'}), 401
    student_id = session['student_id']
    if current_student()['category'] != category:
        return jsonify({'status': 'error', 'message': 'Student session does not match this category'}), 403
    data = get_student_performance_data(student_id, category)
    return jsonify(data)

@app.route('/api/students/<int:student_id>')
def api_get_student(student_id):
    """Returns a student's non-sensitive ID card details."""
    student = get_student_profile(student_id)
    if not student:
        return jsonify({'status': 'error', 'message': 'Student not found'}), 404
    return jsonify({'status': 'success', 'student': student})

if __name__ == '__main__':
    print("Starting AI-Powered Intelligent LMS server on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
