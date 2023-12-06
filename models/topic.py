from .db_instance import db


class Topic(db.Model):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    teacher = db.Column(db.Integer, db.ForeignKey('supervisors.id'))
    quota = db.Column(db.Integer)
    is_custom = db.Column(db.Boolean, default=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    description = db.Column(db.Text)
    required_skills = db.Column(db.Text)
    reference = db.Column(db.Text)

    def __init__(self, name, teacher, quota, is_custom, type_id, description, required_skills, reference):
        self.name = name
        self.teacher = teacher
        self.quota = quota
        self.is_custom = is_custom
        self.type_id = type_id
        self.description = description
        self.required_skills = required_skills
        self.reference = reference

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name, teacher, quota, is_custom, type_id, description, required_skills, reference):
        self.name = name
        self.teacher = teacher
        self.quota = quota
        self.is_custom = is_custom
        self.type_id = type_id
        self.description = description
        self.required_skills = required_skills
        self.reference = reference
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_num(cls):
        return cls.query.count()

    def __repr__(self):
        return f'<Topic {self.id}>'
