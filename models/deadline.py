from .db_instance import db


class Deadline(db.Model):
    __tablename__ = 'deadlines'

    id = db.Column(db.Integer, primary_key=True)
    round_num = db.Column(db.Integer)
    submit_time = db.Column(db.String(20))
    result_time = db.Column(db.String(20))
    note = db.Column(db.Text)

    def __init__(self, round_num, submit_time, result_time, note):
        self.round_num = round_num
        self.submit_time = submit_time
        self.result_time = result_time
        self.note = note

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, round_num, submit_time, result_time, note):
        self.round_num = round_num
        self.submit_time = submit_time
        self.result_time = result_time
        self.note = note
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_num(cls):
        return cls.query.count()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def __repr__(self):
        return f'<Deadline {self.id}>'
