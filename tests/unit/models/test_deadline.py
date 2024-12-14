from unittest import TestCase
from flask import Flask
from models.deadline import Deadline
from config import *
from exts import db


class TestDeadline(TestCase):
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
            self.db.session.query(Deadline).delete()
            self.db.session.commit()

    def test_add(self):
        with self.app.app_context():
            deadline = Deadline(submit_time='2024-11-30 23:59', result_time='2024-12-30 23:59', note='note')
            deadline.add()
            _added = self.db.session.query(Deadline).filter_by(submit_time='2024-11-30 23:59').first()
            self.assertIsNotNone(_added)
            self.assertEqual(_added.submit_time, '2024-11-30 23:59')
            self.assertEqual(_added.result_time, '2024-12-30 23:59')
            self.assertEqual(_added.note, 'note')

    def test_update(self):
        with self.app.app_context():
            deadline = Deadline(submit_time='2024-11-30 23:59', result_time='2024-12-30 23:59', note='note')
            deadline.add()
            self.assertIsNotNone(deadline)
            deadline.update(submit_time='2025-11-30 23:59', result_time='2025-12-30 23:59', note='new')
            self.assertEqual(deadline.submit_time, '2025-11-30 23:59')
            self.assertEqual(deadline.result_time, '2025-12-30 23:59')
            self.assertEqual(deadline.note, 'new')

    def test_delete(self):
        with self.app.app_context():
            deadline = Deadline(submit_time='2024-11-30 23:59', result_time='2024-12-30 23:59', note='note')
            deadline.add()
            self.assertIsNotNone(deadline)
            deadline.delete()
            _deleted = self.db.session.query(Deadline).filter_by(submit_time='2025-11-30 23:59').first()
            self.assertIsNone(_deleted)

    def test_reset(self):
        with self.app.app_context():
            deadline = Deadline(submit_time='2024-11-30 23:59', result_time='2024-12-30 23:59', note='note')
            deadline.add()
            deadline.reset()
            self.assertIsNone(deadline.submit_time)
            self.assertIsNone(deadline.result_time)
            self.assertIsNone(deadline.note)
            deadline.delete()

    def test_get_by_id(self):
        with self.app.app_context():
            deadline = Deadline(submit_time='2024-11-30 23:59', result_time='2024-12-30 23:59', note='note')
            deadline.add()
            added_obj = Deadline.get_by_id(deadline.id)
            self.assertIsNotNone(added_obj)
            assert added_obj.submit_time == '2024-11-30 23:59'
            assert added_obj.result_time == '2024-12-30 23:59'
            assert added_obj.note == 'note'

    def test_get_num(self):
        with self.app.app_context():
            deadline_1 = Deadline(submit_time='2024-11-30 23:59', result_time='2024-12-30 23:59', note='note')
            deadline_2 = Deadline(submit_time='2024-11-30 23:59', result_time='2024-12-30 23:59', note='note')
            deadline_1.add()
            deadline_2.add()
            num = Deadline.get_num()
            assert num == 2

    def test_get_all(self):
        with self.app.app_context():
            deadline_1 = Deadline(submit_time='2024-11-30 23:59', result_time='2024-12-30 23:59', note='note_123')
            deadline_2 = Deadline(submit_time='2024-11-30 23:59', result_time='2024-12-30 23:59', note='note_456')
            deadline_1.add()
            deadline_2.add()
            objs = Deadline.get_all()
            assert len(objs) == 2
            assert objs[0].note == 'note_456'
            assert objs[1].note == 'note_123'
