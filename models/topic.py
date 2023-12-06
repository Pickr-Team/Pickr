from sqlalchemy import case, func

from .db_instance import db
from .selection import Selection
from .supervisor import Supervisor
from .type import Type


class Topic(db.Model):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisors.id'))
    supervisor = db.relationship('Supervisor', backref=db.backref('topics', lazy=True))
    quota = db.Column(db.Integer)
    is_custom = db.Column(db.Boolean, default=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    type = db.relationship('Type', backref=db.backref('topics', lazy=True))
    description = db.Column(db.Text)
    required_skills = db.Column(db.Text)
    reference = db.Column(db.Text)

    def __init__(self, name, teacher, quota, is_custom, type_id, description, required_skills, reference):
        self.name = name
        self.teacher = teacher
        self.quota = quota
        self.is_custom = is_custom
        self.type_id = type_id
        self.description = description
        self.required_skills = required_skills
        self.reference = reference

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name, teacher, quota, is_custom, type_id, description, required_skills, reference):
        self.name = name
        self.teacher = teacher
        self.quota = quota
        self.is_custom = is_custom
        self.type_id = type_id
        self.description = description
        self.required_skills = required_skills
        self.reference = reference
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        subquery1 = db.session.query(
            Selection.first_topic_id,
            func.count(Selection.first_topic_id).label('count1')
        ).group_by(Selection.first_topic_id).subquery()

        subquery2 = db.session.query(
            Selection.second_topic_id,
            func.count(Selection.second_topic_id).label('count2')
        ).group_by(Selection.second_topic_id).subquery()

        subquery3 = db.session.query(
            Selection.third_topic_id,
            func.count(Selection.third_topic_id).label('count3')
        ).group_by(Selection.third_topic_id).subquery()

        topic = db.session.query(
            cls,
            Supervisor.first_name,
            Supervisor.last_name,
            Type.name.label('type_name'),
            func.coalesce(subquery1.c.count1, 0) +
            func.coalesce(subquery2.c.count2, 0) +
            func.coalesce(subquery3.c.count3, 0).label('selected_num')
        ).join(Supervisor, cls.supervisor_id == Supervisor.id) \
            .join(Type, cls.type_id == Type.id) \
            .outerjoin(subquery1, cls.id == subquery1.c.first_topic_id) \
            .outerjoin(subquery2, cls.id == subquery2.c.second_topic_id) \
            .outerjoin(subquery3, cls.id == subquery3.c.third_topic_id) \
            .filter(cls.id == id) \
            .first()

        if topic:
            topic_instance, first_name, last_name, type_name, selected_num = topic
            topic_instance.supervisor_name = f"{first_name} {last_name}"
            topic_instance.type_name = type_name
            topic_instance.selected_num = selected_num
            return topic_instance

        return None

    @classmethod
    def get_all(cls):
        subquery1 = db.session.query(
            Selection.first_topic_id, func.count(Selection.first_topic_id)
        ).group_by(Selection.first_topic_id).subquery()
        subquery2 = db.session.query(
            Selection.second_topic_id, func.count(Selection.second_topic_id)
        ).group_by(Selection.second_topic_id).subquery()
        subquery3 = db.session.query(
            Selection.third_topic_id, func.count(Selection.third_topic_id)
        ).group_by(Selection.third_topic_id).subquery()

        query = db.session.query(cls, Supervisor.first_name, Supervisor.last_name, Type.name,
                                 func.coalesce(subquery1.c.count, 0) + func.coalesce(subquery2.c.count,
                                                                                     0) + func.coalesce(
                                     subquery3.c.count, 0)).outerjoin(subquery1,
                                                                      cls.id == subquery1.c.first_topic_id).outerjoin(
            subquery2, cls.id == subquery2.c.second_topic_id).outerjoin(subquery3, cls.id == subquery3.c.third_topic_id)

        query = query.join(Supervisor, cls.supervisor_id == Supervisor.id)

        query = query.join(Type, cls.type_id == Type.id)

        topics = query.all()

        results = []
        for topic, first_name, last_name, type_name, selected_num in topics:
            topic.supervisor_name = f"{first_name} {last_name}"
            topic.type_name = type_name
            topic.selected_num = selected_num
            results.append(topic)

        return results

    @classmethod
    def get_num(cls):
        return cls.query.count()

    def __repr__(self):
        return f'<Topic {self.id}>'
