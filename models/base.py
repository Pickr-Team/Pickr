from exts import db
from sqlalchemy.orm import Session, object_session


class BaseModel(db.Model):

    __abstract__ = True  # it's an abstract class and will not be used directly as a database table

    def add(self, session: Session = None) -> None:
        if session is None:
            session = db.session
        session.add(self)
        session.commit()

    def update(self, **kwargs: dict) -> None:
        # need to explain the specific attribute's name
        # type.update(name='3D'): correct
        # type.update('3D'): wrong
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        db.session.commit()

    def delete(self, session: Session = None) -> None:
        if session is None:
            session = db.session
        session.delete(self)
        session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.id.desc()).all()

    @classmethod
    def get_num(cls):
        return cls.query.count()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()