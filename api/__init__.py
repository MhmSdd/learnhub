from flask import Blueprint, jsonify, session
from models import Course, Enrollment
from flask_babel import _

api_bp = Blueprint('api', __name__)

@api_bp.route('/courses', methods=['GET'])
def get_courses():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': _('Please login first.')}), 401
    
    student_id = session['user_id']
    courses = Course.query.all()
    courses_data = []
    
    for course in courses:
        is_enrolled = Enrollment.query.filter_by(student_id=student_id, course_id=course.id).first() is not None
        courses_data.append({
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'is_enrolled': is_enrolled
        })
    
    return jsonify({'success': True, 'courses': courses_data})