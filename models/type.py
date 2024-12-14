from exts import db
from .base import BaseModel
from .topic import Topic


class Type(BaseModel):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    @property
    def has_topics(self):
        return db.session.query(Topic.id).filter_by(type_id=self.id, is_custom=False).first() is not None

    @classmethod
    def get_by_title(cls, _name):
        return cls.query.filter_by(name=_name).first()

    def __repr__(self):
        return f'<Type {self.id}>'
