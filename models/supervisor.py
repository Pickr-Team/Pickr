from sqlalchemy import func
from exts import db
from .topic import Topic


class Supervisor(db.Model):
    __tablename__ = 'supervisors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean)
    position = db.Column(db.Integer)
    user_name = db.Column(db.String(20))
    password = db.Column(db.String(100))
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

    def update(self, first_name, last_name, position, user_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.user_name = user_name
        self.email = email
        db.session.commit()

    def update_pwd(self, pwd):
        self.password = pwd
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def has_topics(self):
        return db.session.query(Topic.id).filter_by(supervisor_id=self.id).first() is not None

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_num(cls):
        return cls.query.count()

    def if_admin(self):
        return self.is_admin

    @classmethod
    def get_id(cls, user_name):
        return cls.query.filter_by(user_name=user_name).first().id

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    # Get the number of topic's position supervised by this supervisor
    def get_topic_num(self):
        total_quota = db.session.query(func.sum(Topic.quota)) \
            .filter(Topic.supervisor_id == self.id) \
            .scalar()
        return total_quota if total_quota is not None else 0

    def get_not_custom_topic_num(self):
        total_quota = db.session.query(func.sum(Topic.quota)) \
            .filter(Topic.supervisor_id == self.id, Topic.is_custom == False) \
            .scalar()
        return total_quota if total_quota is not None else 0

    def get_total_final_selections(self):
        topics = Topic.query.filter_by(supervisor_id=self.id).all()
        total_selections = 0
        for topic in topics:
            final_selections = topic.get_selected_num_final()
            if final_selections is not None:
                total_selections += final_selections
        return total_selections

    def __repr__(self):
        return f'<Supervisor {self.id}>'
