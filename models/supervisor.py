from .db_instance import db

class Supervisor(db.Model):
    __tablename__ = 'supervisors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20), default='0')
    is_admin = db.Column(db.Boolean)
    position = db.Column(db.Integer)
    user_name = db.Column(db.String(20))
    password = db.Column(db.String(40))
    email = db.Column(db.String(30))

    def __init__(self, first_name, last_name, is_admin, position, user_name, password, email):
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.position = position
        self.user_name = user_name
        self.password = password
        self.email = email

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, first_name, last_name, is_admin, position, user_name, password, email):
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.position = position
        self.user_name = user_name
        self.password = password
        self.email = email
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def query_all(cls):
        return cls.query.all()

    def __repr__(self):
        return f'<Supervisor {self.id}>'
