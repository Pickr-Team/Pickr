from .db_instance import db


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    chinese_name = db.Column(db.String(20))
    english_name = db.Column(db.String(20))
    class_number = db.Column(db.String(30))
    email = db.Column(db.String(100))
    password = db.Column(db.String(40))
    user_name = db.Column(db.String(20))

    def __init__(self, chinese_name, english_name, email, password, user_name, class_number):
        self.chinese_name = chinese_name
        self.english_name = english_name
        self.email = email
        self.password = password
        self.user_name = user_name
        self.class_number = class_number

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, chinese_name, english_name, email, password, user_name, class_number):
        self.chinese_name = chinese_name
        self.english_name = english_name
        self.email = email
        self.password = password
        self.user_name = user_name
        self.class_number = class_number
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_query(cls):
        return cls.query

    @classmethod
    def get_num(cls):
        return cls.query.count()

    @classmethod
    def get_id(cls, english_name):
        return cls.query.filter_by(english_name=english_name).first().id

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_name_username_class_number(cls, search_query):
        return cls.query.filter(
            (cls.chinese_name.like(f'%{search_query}%')) |
            (cls.english_name.like(f'%{search_query}%')) |
            (cls.user_name.like(f'%{search_query}%')) |
            (cls.class_number.like(f'%{search_query}%'))
        )

    def __repr__(self):
        return f'<Student {self.id}>'
