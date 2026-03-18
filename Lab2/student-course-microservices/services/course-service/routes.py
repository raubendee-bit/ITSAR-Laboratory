from flask import Blueprint, request, jsonify
from models import db, Course

bp = Blueprint('courses', __name__)

@bp.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses]), 200

@bp.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    if not data or 'title' not in data or 'credits' not in data:
        return jsonify({
            'error': 'MISSING_FIELDS',
            'message': 'Both title and credits are required'
        }), 400
    if not data['title'].strip():
        return jsonify({
            'error': 'INVALID_INPUT',
            'message': 'Title cannot be empty'
        }), 400
    if not isinstance(data['credits'], int) or data['credits'] < 1:
        return jsonify({
            'error': 'INVALID_INPUT',
            'message': 'Credits must be a positive integer'
        }), 400
    course = Course(title=data['title'], credits=data['credits'])
    db.session.add(course)
    db.session.commit()
    return jsonify({'id': course.id, 'message': 'created'}), 201

@bp.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({
            'error': 'NOT_FOUND',
            'message': f'Course with id {id} does not exist'
        }), 404
    return jsonify(course.to_dict()), 200

@bp.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({
            'error': 'NOT_FOUND',
            'message': f'Course with id {id} does not exist'
        }), 404
    db.session.delete(course)
    db.session.commit()
    return jsonify({'id': id, 'message': 'deleted'}), 200
