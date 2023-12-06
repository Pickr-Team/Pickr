from app import db


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    content = db.Column(db.Text)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, title, content):
        self.title = title
        self.content = content
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def query_all(cls):
        return cls.query.all()

    def __repr__(self):
        return f'<Note {self.id}>'
