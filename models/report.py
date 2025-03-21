from exts import db
from models.base import BaseModel
from models.supervisor import Supervisor


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
    is_read = db.Column(db.Integer, nullable=False)  # 0-not read, 1-read
    comments = db.Column(db.Text, nullable=True)

    def __init__(self, student_id, submit_time, update_time, semester, week,
                 current_plan=None, next_plan=None, issues=None, feedback=None, is_read=0, comments=None):
        self.student_id = student_id
        self.submit_time = submit_time
        self.update_time = update_time
        self.semester = semester
        self.week = week
        self.current_plan = current_plan
        self.next_plan = next_plan
        self.issues = issues
        self.feedback = feedback
        self.is_read = is_read
        self.comments = comments

    @classmethod
    def get_by_student_id(cls, student_id):
        return cls.query.filter_by(student_id=student_id).all()

    @classmethod
    def get_all_reports_by_supervisor_id(cls, supervisor_id):
        """Get all reports from students supervised by the specified supervisor"""
        supervisor = Supervisor.get_by_id(supervisor_id)
        selections = supervisor.get_total_selected_selections()

        all_reports = []
        for selection in selections:
            reports = Report.query.filter_by(student_id=selection.student_id) \
                .order_by(Report.update_time.desc()).all()
            all_reports.extend(reports)

        all_reports.sort(key=lambda x: x.update_time, reverse=True)

        return all_reports

    def mark_as_read(self):
        self.is_read = 1
        db.session.add(self)
        db.session.commit()
