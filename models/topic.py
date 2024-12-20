from sqlalchemy import or_, func
from exts import db
from .base import BaseModel
from .selection import Selection
import re


class Topic(BaseModel):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisors.id'))
    supervisor = db.relationship('Supervisor', backref=db.backref('topics', lazy=True))
    quota = db.Column(db.Integer)
    is_custom = db.Column(db.Boolean, default=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    type = db.relationship('Type', backref=db.backref('topics', lazy=True))
    description = db.Column(db.Text)
    required_skills = db.Column(db.Text)
    reference = db.Column(db.Text)

    def __init__(self, name, supervisor_id, quota, is_custom, type_id, description, required_skills, reference):
        self.name = name
        self.supervisor_id = supervisor_id
        self.quota = quota
        self.is_custom = is_custom
        self.type_id = type_id
        self.description = description
        self.required_skills = required_skills
        self.reference = reference

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @classmethod
    def get_by_supervisor_id(cls, supervisor_id):
        return cls.query.filter_by(supervisor_id=supervisor_id).all()

    @classmethod
    def get_by_supervisor_id_not_custom(cls, supervisor_id):
        return cls.query.filter_by(supervisor_id=supervisor_id, is_custom=False).all()

    @classmethod
    def get_by_type_id(cls, type_id):
        return cls.query.filter_by(type_id=type_id).all()

    @classmethod
    def get_by_name_or_id(cls, search_query):
        if search_query.lower().startswith('pk'):
            match = re.search(r'\d+', search_query)
            if match:
                number_part = int(match.group())
                return cls.query.filter(cls.id == number_part).all()
        else:
            return cls.query.filter(
                or_(
                    cls.id == search_query,
                    cls.name.like(f'%{search_query}%')
                )
            ).all()
        return []

    # @classmethod
    # def search_by_id(cls, id):
    #     if id.lower().startswith('pk'):
    #         match = re.search(r'\d+', id)
    #         if match:
    #             number_part = int(match.group())
    #             return cls.query.filter(cls.id == number_part).first()
    #         else:
    #             return None

    # Get the number of students who have selected this topic (selection.status == 0)
    def get_selected_num(self):
        return Selection.query.filter(
            Selection.status == 0,
            (
                    (Selection.first_topic_id == self.id) |
                    (Selection.second_topic_id == self.id) |
                    (Selection.third_topic_id == self.id)
            )
        ).count()

    # Get the number of students who have selected this topic
    def get_selected_num_total(self):
        return Selection.query.filter(
            (Selection.first_topic_id == self.id) |
            (Selection.second_topic_id == self.id) |
            (Selection.third_topic_id == self.id)
        ).count()

    # Get the number of students who have selected this topic (selection.status == 3 or 4)
    def get_selected_num_final(self):
        return Selection.query.filter(
            Selection.status.in_([3, 4]),
            (Selection.final_topic_id == self.id)
        ).count()

    def get_supervisor_name(self):
        if self.supervisor:
            return f'{self.supervisor.first_name} {self.supervisor.last_name}'
        else:
            return None

    def get_type_name(self):
        return self.type.name

    @classmethod
    def get_all_quota(cls):
        # warning, do not change the '==' to 'is'!
        return cls.query.filter(cls.is_custom == False).with_entities(func.sum(cls.quota)).scalar()

    @classmethod
    def get_num_not_custom(cls):
        # warning, do not change the '==' to 'is'!
        return cls.query.filter(cls.is_custom == False).count()

    @classmethod
    def get_num_custom(cls):
        # warning, do not change the '==' to 'is'!
        return cls.query.filter(cls.is_custom == True).count()

    # Get all topics that are custom
    @classmethod
    def get_all_custom(cls):
        # warning, do not change the '==' to 'is'!
        return cls.query.filter(cls.is_custom == True).all()

    def __repr__(self):
        return f'<Topic {self.id}>'
