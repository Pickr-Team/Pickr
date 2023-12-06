from .db_instance import db

class Selection(db.Model):
    __tablename__ = 'selections'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    submit_time = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    first_topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    second_topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    third_topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    final_topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))

    def __repr__(self):
        return f'<Selection {self.id}>'