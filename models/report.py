from exts import db
from models.base import BaseModel


class Report(BaseModel):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    student = db.relationship('Student', backref=db.backref('reports', lazy=True))
    submit_time = db.Column(db.String(20), nullable=False)
    update_time = db.Column(db.String(20), nullable=False)
    current_plan = db.Column(db.Text, nullable=True)
    next_plan = db.Column(db.Text, nullable=True)
    issues = db.Column(db.Text, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    semester = db.Column(db.Integer, nullable=False)  # 1, 2
    week = db.Column(db.Integer, nullable=False)  # 1 - 12

    def __init__(self, student_id, submit_time, update_time, semester, week,
                 current_plan=None, next_plan=None, issues=None, feedback=None):
        self.student_id = student_id
        self.submit_time = submit_time
        self.update_time = update_time
        self.semester = semester
        self.week = week
        self.current_plan = current_plan
        self.next_plan = next_plan
        self.issues = issues
        self.feedback = feedback

    @classmethod
    def get_by_student_id(cls, student_id):
        return cls.query.filter_by(student_id=student_id).all()