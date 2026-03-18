from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Enrollment(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    course_id  = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'student_id': self.student_id, 'course_id': self.course_id}
