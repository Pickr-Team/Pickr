from .db_instance import db

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    chinese_name = db.Column(db.String(20))
    english_name = db.Column(db.String(20))
    email = db.Column(db.String(30))
    password = db.Column(db.String(40))

    def __init__(self, chinese_name, english_name, email, password):
        self.chinese_name = chinese_name
        self.english_name = english_name
        self.email = email
        self.password = password

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, chinese_name, english_name, email, password):
        self.chinese_name = chinese_name
        self.english_name = english_name
        self.email = email
        self.password = password
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def query_all(cls):
        return cls.query.all()

    def __repr__(self):
        return f'<Student {self.id}>'
