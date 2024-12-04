from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    candidate = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Vote {self.name}>"

    @staticmethod
    def get_vote_statistics():
        total_votes = Vote.query.count()
        gender_stats = (
            db.session.query(Vote.gender, db.func.count(Vote.id))
            .group_by(Vote.gender)
            .all()
        )
        course_stats = (
            db.session.query(Vote.course, db.func.count(Vote.id))
            .group_by(Vote.course)
            .all()
        )
        candidate_stats = (
            db.session.query(Vote.candidate, db.func.count(Vote.id))
            .group_by(Vote.candidate)
            .all()
        )
        return total_votes, gender_stats, course_stats, candidate_stats
