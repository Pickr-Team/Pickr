from exts import db
from models.base import BaseModel


class Deadline(BaseModel):
    __tablename__ = 'deadlines'
    id = db.Column(db.Integer, primary_key=True)
    submit_time = db.Column(db.String(20))
    result_time = db.Column(db.String(20))
    note = db.Column(db.Text)

    def __init__(self, submit_time, result_time, note):
        self.submit_time = submit_time
        self.result_time = result_time
        self.note = note

    @classmethod
    def get_first(cls):
        return cls.query.first()

    @classmethod
    def get_second(cls):
        return cls.query.filter_by(id=2).first()

    def reset(self):
        self.submit_time = None
        self.result_time = None
        self.note = None
        db.session.commit()

    def __repr__(self):
        return f'<Deadline {self.id}>'
