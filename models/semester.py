from exts import db
from models.base import BaseModel


class Semester(BaseModel):
    __tablename__ = 'semester'
    id = db.Column(db.Integer, primary_key=True)
    graduation_year = db.Column(db.Integer)
    first_semester_start_date = db.Column(db.String(20))
    second_semester_start_date = db.Column(db.String(20))
    # default duration: 13 weeks

    def __init__(self, graduation_year: int, first_semester_start_date: str, second_semester_start_date: str):
        self.graduation_year = graduation_year
        self.first_semester_start_date = first_semester_start_date
        self.second_semester_start_date = second_semester_start_date

    @classmethod
    def get_latest(cls):
        """
        Returns the latest semester record from the database.
        """
        return db.session.query(cls).order_by(cls.id.desc()).first()

    def __repr__(self):
        return f'<Semester {self.id} - Class of {self.graduation_year}>'
