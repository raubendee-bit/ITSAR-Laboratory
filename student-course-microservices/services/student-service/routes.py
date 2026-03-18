from flask import Blueprint, request, jsonify
from models import db, Student

bp = Blueprint('students', __name__)

@bp.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200

@bp.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({
            'error': 'MISSING_FIELDS',
            'message': 'Both name and email are required'
        }), 400
    if not data['name'].strip() or not data['email'].strip():
        return jsonify({
            'error': 'INVALID_INPUT',
            'message': 'Name and email cannot be empty'
        }), 400
    if Student.query.filter_by(email=data['email']).first():
        return jsonify({
            'error': 'DUPLICATE_EMAIL',
            'message': f"Email '{data['email']}' already exists"
        }), 409
    student = Student(name=data['name'], email=data['email'])
    db.session.add(student)
    db.session.commit()
    return jsonify({'id': student.id, 'message': 'created'}), 201

@bp.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({
            'error': 'NOT_FOUND',
            'message': f'Student with id {id} does not exist'
        }), 404
    return jsonify(student.to_dict()), 200

@bp.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({
            'error': 'NOT_FOUND',
            'message': f'Student with id {id} does not exist'
        }), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({'id': id, 'message': 'deleted'}), 200
