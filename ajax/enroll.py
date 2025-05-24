from flask import Blueprint, jsonify, session, request
from models import db, Enrollment, Course
from flask_babel import _

ajax_bp = Blueprint('ajax', __name__)

@ajax_bp.route('/enroll', methods=['POST'])
def enroll_course():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': _('Please login first.')}), 401
    
    data = request.get_json()
    course_id = data.get('course_id')
    student_id = session['user_id']
    
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'success': False, 'message': _('Course not found.')}), 404
    
    existing_enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if existing_enrollment:
        return jsonify({'success': False, 'message': _('You are already enrolled in this course.')}), 400
    
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'success': True, 'message': _('Successfully enrolled in the course.')})

@ajax_bp.route('/unenroll', methods=['POST'])
def unenroll_course():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': _('Please login first.')}), 401
    
    data = request.get_json()
    course_id = data.get('course_id')
    student_id = session['user_id']
    
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'success': False, 'message': _('Course not found.')}), 404
    
    enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if not enrollment:
        return jsonify({'success': False, 'message': _('You are not enrolled in this course.')}), 400
    
    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({'success': True, 'message': _('Successfully unenrolled from the course.')})