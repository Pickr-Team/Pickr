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
    first_topic = db.relationship('Topic', foreign_keys=[first_topic_id])
    second_topic = db.relationship('Topic', foreign_keys=[second_topic_id])
    third_topic = db.relationship('Topic', foreign_keys=[third_topic_id])

    @property
    def first_topic_name(self):
        return self.first_topic.name

    @property
    def second_topic_name(self):
        return self.second_topic.name

    @property
    def third_topic_name(self):
        return self.third_topic.name

    @classmethod
    def get_by_student_id(cls, student_id):
        return cls.query.filter_by(student_id=student_id).first()

    def __repr__(self):
        return f'<Selection {self.id}>'
