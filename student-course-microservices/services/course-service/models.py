from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    title   = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'credits': self.credits}
