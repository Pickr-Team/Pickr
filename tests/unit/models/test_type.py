from unittest import TestCase
from flask import Flask

from models.topic import Topic
from models.type import Type
from models.selection import Selection
from models.student import Student
from models.supervisor import Supervisor
from config import *
from exts import db


class TestType(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config.from_object(TestConfig)
        cls.db = db
        cls.db.init_app(cls.app)
        with cls.app.app_context():
            cls.db.create_all()

    @classmethod
    def tearDownClass(cls) -> None:
        with cls.app.app_context():
            cls.db.drop_all()

    def tearDown(self):
        # clear Type after each test
        with self.app.app_context():
            self.db.session.query(Topic).delete()
            self.db.session.query(Type).delete()
            self.db.session.commit()

    def test_add(self):
        with self.app.app_context():
            _type = Type(name='Game')
            _type.add()
            added_type = self.db.session.query(Type).filter_by(name='Game').first()
            self.assertIsNotNone(added_type)
            self.assertEqual(added_type.name, 'Game')

    def test_update(self):
        with self.app.app_context():
            _type = Type(name='Game')
            _type.add()
            added_type = self.db.session.query(Type).filter_by(name='Game').first()
            self.assertIsNotNone(added_type)
            added_type.update(name='VR')
            self.assertEqual(added_type.name, 'VR')

    def test_delete(self):
        with self.app.app_context():
            _type = Type(name='3D')
            _type.add()
            added_type = self.db.session.query(Type).filter_by(name='3D').first()
            self.assertIsNotNone(added_type)
            added_type.delete()
            deleted_type = self.db.session.query(Type).filter_by(name='3D').first()
            self.assertIsNone(deleted_type)

    def test_get_by_id(self):
        with self.app.app_context():
            _type = Type(name='ARR')
            _type.add()
            added_type = Type.get_by_id(_type.id)
            self.assertIsNotNone(added_type)
            assert added_type.name == 'ARR'

    def test_get_by_title(self):
        with self.app.app_context():
            _type = Type(name='Game2')
            _type.add()
            added_type = Type.get_by_title('Game2')
            assert added_type.name == 'Game2'

    def test_get_all(self):
        with self.app.app_context():
            _type = Type(name='Game')
            _type_2 = Type(name='3D')
            _type.add()
            _type_2.add()
            types = Type.get_all()
            assert len(types) == 2
            assert types[0].name == '3D'
            assert types[1].name == 'Game'

    def test_get_num(self):
        with self.app.app_context():
            _type = Type(name='Game')
            _type_2 = Type(name='3D')
            _type.add()
            _type_2.add()
            num = Type.get_num()
            assert num == 2

    def test_has_topic_false(self):
        with self.app.app_context():
            _type = Type(name='Game')
            _type.add()
            assert _type.has_topics is False

    def test_has_topic_true(self):
        with self.app.app_context():
            _type = Type(name='Game')
            _type.add()
            supervisor = Supervisor('Clivia', 'Li', False, 20, 'clivia', '123456', None, None)
            supervisor.add()
            topic = Topic('topic', 1, 10, False, _type.id, None, None, None)
            topic.add()
            assert _type.has_topics is True
