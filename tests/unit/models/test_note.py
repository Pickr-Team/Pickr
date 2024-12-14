from unittest import TestCase
from flask import Flask
from models.note import Note
from config import *
from exts import db


class TestNote(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config.from_object(TestConfig)
        cls.db = db
        cls.db.init_app(cls.app)
        with cls.app.app_context():
            cls.db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            cls.db.drop_all()

    def tearDown(self):
        # clear data after each test
        with self.app.app_context():
            self.db.session.query(Note).delete()
            self.db.session.commit()

    def test_add(self):
        with self.app.app_context():
            note = Note(title='test-note', content='test-content')
            note.add()
            added_note = self.db.session.query(Note).filter_by(title='test-note').first()
            self.assertIsNotNone(added_note)
            self.assertEqual(added_note.title, 'test-note')
            self.assertEqual(added_note.content, 'test-content')

    def test_update(self):
        with self.app.app_context():
            note = Note(title='test-note', content='test-content')
            note.add()
            self.assertIsNotNone(note)
            note.update(title='new-title', content='new-content')
            self.assertEqual(note.title, 'new-title')
            self.assertEqual(note.content, 'new-content')

    def test_delete(self):
        with self.app.app_context():
            note = Note(title='test-note', content='test-content')
            note.add()
            self.assertIsNotNone(note)
            note.delete()
            deleted_note = self.db.session.query(Note).filter_by(title='test-note').first()
            self.assertIsNone(deleted_note)

    def test_get_by_id(self):
        with self.app.app_context():
            note = Note(title='test-note-123', content='test-content')
            note.add()
            added_obj = Note.get_by_id(note.id)
            self.assertIsNotNone(added_obj)
            assert added_obj.title == 'test-note-123'
            assert added_obj.content == 'test-content'

    def test_get_num(self):
        with self.app.app_context():
            note_1 = Note(title='test-note-1', content='test-content')
            note_2 = Note(title='test-note-2', content='test-content')
            note_1.add()
            note_2.add()
            num = Note.get_num()
            assert num == 2

    def test_get_all(self):
        with self.app.app_context():
            note_1 = Note(title='test-note-1', content='test-content')
            note_2 = Note(title='test-note-2', content='test-content')
            note_1.add()
            note_2.add()
            notes = Note.get_all()
            assert len(notes) == 2
            assert notes[0].title == 'test-note-2'
            assert notes[1].title == 'test-note-1'

