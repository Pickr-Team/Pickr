from sqlalchemy import func
from exts import db
from .base import BaseModel
from .topic import Topic


class Supervisor(BaseModel):
    __tablename__ = 'supervisors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean)
    position = db.Column(db.Integer)
    user_name = db.Column(db.String(20))
    password = db.Column(db.String(100))
    email = db.Column(db.String(30))
    expertise = db.Column(db.String(255))

    def __init__(self, first_name, last_name, is_admin, position, user_name, password, email, expertise):
        self.expertise = expertise
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.position = position
        self.user_name = user_name
        self.password = password
        self.email = email

    def update_pwd(self, pwd):
        self.password = pwd
        db.session.commit()

    @property
    def has_topics(self):
        return db.session.query(Topic.id).filter_by(supervisor_id=self.id).first() is not None

    @classmethod
    def get_all_admins(cls):
        return cls.query.filter_by(is_admin=True).all()

    @classmethod
    def get_all_supervisors(cls):
        return cls.query.filter_by(is_admin=False).all()

    def if_admin(self):
        return self.is_admin

    @classmethod
    def get_id_by_username(cls, user_name):
        return cls.query.filter_by(user_name=user_name).first().id

    @classmethod
    def get_by_name(cls, full_name):
        first_name, last_name = full_name.split(' ')
        return cls.query.filter(
            (cls.first_name == first_name) &
            (cls.last_name == last_name)
        ).first()

    # Get the number of topic's position supervised by this supervisor
    def get_topic_total_quota(self):
        total_quota = db.session.query(func.sum(Topic.quota)) \
            .filter(Topic.supervisor_id == self.id) \
            .scalar()
        return total_quota if total_quota is not None else 0

    def get_not_custom_topic_num(self):
        total_quota = db.session.query(func.sum(Topic.quota)) \
            .filter(Topic.supervisor_id == self.id, Topic.is_custom is False) \
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
