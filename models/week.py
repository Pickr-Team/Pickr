from exts import db
from models.base import BaseModel


class Week(BaseModel):
    __tablename__ = 'week'
    id = db.Column(db.Integer, primary_key=True)
    week_num = db.Column(db.Integer, nullable=False)  # 1-13
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    semester_num = db.Column(db.Integer, nullable=False)
    semester = db.relationship('Semester', backref=db.backref('semesters', lazy=True))
    requires_report = db.Column(db.Boolean, default=True)  # should students write weekly report this week?

    def __init__(self, week_num, start_date, semester_num, end_date, semester_id, requires_report=True):
        self.week_num = week_num
        self.start_date = start_date
        self.end_date = end_date
        self.semester_id = semester_id
        self.requires_report = requires_report
        self.semester_num = semester_num
