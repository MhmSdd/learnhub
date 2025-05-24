import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, session, request, g, render_template, redirect, url_for, flash, jsonify
from flask_migrate import Migrate
from models import db, Student, Course, Enrollment
from forms import RegistrationForm, LoginForm
from api import api_bp
from ajax.enroll import ajax_bp
from werkzeug.security import generate_password_hash
from config import Config
from flask_babel import Babel, _

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# تهيئة Babel مع دالة locale_selector
babel = Babel(app)

@babel.locale_selector
def get_locale():
    if 'lang' in session:
        return session['lang']
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'ar'

@app.before_request
def before_request():
    g.lang = session.get('lang', 'en')

@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    if lang_code in app.config['LANGUAGES']:
        session['lang'] = lang_code
    return redirect(url_for('index'))

db.init_app(app)
migrate = Migrate(app, db)

# تعبئة قاعدة البيانات - تأكد أن التنفيذ ضمن سياق التطبيق

#@app.before_request
#def create_tables():
   # db.create_all()  


with app.app_context():
    if Course.query.count() == 0:
        courses = [
            Course(title="Introduction to Python", description="Learn the basics of Python programming."),
            Course(title="Advanced JavaScript", description="Master JavaScript and its modern frameworks."),
            Course(title="Web Development with Flask", description="Build web applications using Flask."),
            Course(title="Data Science with R", description="Learn data analysis and visualization using R.")
        ]
        db.session.bulk_save_objects(courses)
        db.session.commit()

# تسجيل Blueprints
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(ajax_bp, url_prefix='/ajax')

@app.before_request
def session_management():
    session.permanent = True  # Keep session alive until logout

@app.route('/')
def index():
    theme = request.cookies.get('theme', 'light')
    return render_template('index.html', current_theme=theme, languages=app.config['LANGUAGES'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student and student.check_password(form.password.data):
            session['user_id'] = student.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form, languages=app.config['LANGUAGES'])

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('login'))

    student = Student.query.get(session['user_id'])
    enrolled_courses = Course.query.join(Enrollment).filter(Enrollment.student_id == student.id).all()
    return render_template('dashboard.html', student=student, courses=enrolled_courses, languages=app.config['LANGUAGES'])

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))

@app.route('/courses')
def courses():
    if 'user_id' not in session:
        flash("Please login to view courses.", "warning")
        return redirect(url_for('login'))
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses, languages=app.config['LANGUAGES'])

@app.route('/ajax/enroll', methods=['POST'])
def enroll():
    if 'user_id' not in session:
        return jsonify({"message": "You must be logged in to enroll."}), 401

    course_id = request.json.get('course_id')
    
    existing_enrollment = Enrollment.query.filter_by(student_id=session['user_id'], course_id=course_id).first()
    if existing_enrollment:
        return jsonify({"message": "You are already enrolled in this course."}), 400
    
    enrollment = Enrollment(student_id=session['user_id'], course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    
    return jsonify({"message": "Enrolled successfully!"})

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = Student.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email address already registered.', 'danger')
            return redirect(url_for('register'))
        
        new_user = Student(
            email=form.email.data,
            name=form.name.data,
        )
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form, languages=app.config['LANGUAGES'])

if __name__ == '__main__':
    app.run(debug=True)
