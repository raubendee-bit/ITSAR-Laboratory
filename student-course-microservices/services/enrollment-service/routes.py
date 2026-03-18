from flask import Blueprint, request, jsonify, current_app
from models import db, Enrollment
import requests
from requests.exceptions import ConnectionError, Timeout

bp = Blueprint('enrollments', __name__)

def student_url():
    return current_app.config['STUDENT_SERVICE_URL']

def course_url():
    return current_app.config['COURSE_SERVICE_URL']

def timeout():
    return current_app.config['TIMEOUT_SECONDS']

@bp.route('/enrollments', methods=['GET'])
def get_enrollments():
    enrollments = Enrollment.query.all()
    try:
        all_students = requests.get(f"{student_url()}/students", timeout=timeout()).json()
        all_courses  = requests.get(f"{course_url()}/courses",   timeout=timeout()).json()
        students_map = {s['id']: s for s in all_students}
        courses_map  = {c['id']: c for c in all_courses}
    except Timeout:
        return jsonify({
            'error': 'GATEWAY_TIMEOUT',
            'message': 'A dependent service took too long to respond'
        }), 504
    except ConnectionError:
        return jsonify({
            'error': 'SERVICE_UNAVAILABLE',
            'message': 'A dependent service is currently unavailable'
        }), 503

    result = []
    for e in enrollments:
        result.append({
            'id': e.id,
            'student': students_map.get(e.student_id, {}),
            'course':  courses_map.get(e.course_id, {})
        })
    return jsonify(result), 200

@bp.route('/enrollments', methods=['POST'])
def create_enrollment():
    data = request.get_json()
    if not data or 'student_id' not in data or 'course_id' not in data:
        return jsonify({
            'error': 'MISSING_FIELDS',
            'message': 'Both student_id and course_id are required'
        }), 400

    student_id = data['student_id']
    course_id  = data['course_id']

    # Validate student exists
    try:
        s_resp = requests.get(f"{student_url()}/students/{student_id}", timeout=timeout())
    except Timeout:
        return jsonify({
            'error': 'GATEWAY_TIMEOUT',
            'message': 'Student Service took too long to respond'
        }), 504
    except ConnectionError:
        return jsonify({
            'error': 'SERVICE_UNAVAILABLE',
            'message': 'Student Service is currently unavailable'
        }), 503

    if s_resp.status_code == 404:
        return jsonify({
            'error': 'NOT_FOUND',
            'message': f'Student with id {student_id} does not exist'
        }), 404

    # Validate course exists
    try:
        c_resp = requests.get(f"{course_url()}/courses/{course_id}", timeout=timeout())
    except Timeout:
        return jsonify({
            'error': 'GATEWAY_TIMEOUT',
            'message': 'Course Service took too long to respond'
        }), 504
    except ConnectionError:
        return jsonify({
            'error': 'SERVICE_UNAVAILABLE',
            'message': 'Course Service is currently unavailable'
        }), 503

    if c_resp.status_code == 404:
        return jsonify({
            'error': 'NOT_FOUND',
            'message': f'Course with id {course_id} does not exist'
        }), 404

    # Check duplicate
    existing = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if existing:
        return jsonify({
            'error': 'DUPLICATE_ENROLLMENT',
            'message': f'Student {student_id} is already enrolled in course {course_id}'
        }), 409

    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'id': enrollment.id, 'message': 'created'}), 201

@bp.route('/enrollments/<int:id>', methods=['GET'])
def get_enrollment(id):
    e = Enrollment.query.get(id)
    if not e:
        return jsonify({
            'error': 'NOT_FOUND',
            'message': f'Enrollment with id {id} does not exist'
        }), 404
    try:
        s = requests.get(f"{student_url()}/students/{e.student_id}", timeout=timeout()).json()
        c = requests.get(f"{course_url()}/courses/{e.course_id}",    timeout=timeout()).json()
    except Timeout:
        return jsonify({
            'error': 'GATEWAY_TIMEOUT',
            'message': 'A dependent service took too long to respond'
        }), 504
    except ConnectionError:
        return jsonify({
            'error': 'SERVICE_UNAVAILABLE',
            'message': 'A dependent service is currently unavailable'
        }), 503
    return jsonify({'id': e.id, 'student': s, 'course': c}), 200
