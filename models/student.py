from datetime import datetime

from blueprints.utils import get_current_graduation_year
from exts import db
from models.base import BaseModel
from models.selection import Selection


class Student(BaseModel):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    chinese_name = db.Column(db.String(20))
    english_name = db.Column(db.String(20))
    class_number = db.Column(db.String(30))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    user_name = db.Column(db.String(20))
    graduation_year = db.Column(db.Integer)

    def __init__(self, chinese_name, english_name, email, password, user_name, class_number, graduation_year):
        self.chinese_name = chinese_name
        self.english_name = english_name
        self.email = email
        self.password = password
        self.user_name = user_name
        self.class_number = class_number
        self.graduation_year = graduation_year

    def update_pwd(self, pwd):
        self.password = pwd
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'chinese_name': self.chinese_name,
            'english_name': self.english_name,
            'email': self.email,
            'user_name': self.user_name,
            'class_number': self.class_number
        }

    @classmethod
    def get_id_by_english_name(cls, english_name):
        return cls.query.filter_by(english_name=english_name).first().id

    @classmethod
    def get_by_name_username_class_number(cls, search_query):
        # Student.get_by_name_username_class_number('wangwu').first() or
        # Student.get_by_name_username_class_number('wangwu').all()
        return cls.query.filter(
            (cls.chinese_name.like(f'%{search_query}%')) |
            (cls.english_name.like(f'%{search_query}%')) |
            (cls.user_name.like(f'%{search_query}%')) |
            (cls.class_number.like(f'%{search_query}%'))
        )

    def get_final_topic_name(self):
        selection = Selection.get_by_student_id(self.id)
        if selection is None:
            return None
        elif selection.final_topic is None:
            return None
        return selection.final_topic_name

    def get_supervisor_name(self):
        selection = Selection.get_by_student_id(self.id)
        if selection is None:
            return None
        elif selection.final_topic is None:
            return None
        return selection.final_topic_supervisor_name

    @property
    def supervisor(self):
        selection = Selection.get_by_student_id(self.id)
        return selection.final_topic.supervisor

    def __repr__(self):
        return f'<Student {self.id}>'
