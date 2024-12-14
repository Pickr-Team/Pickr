from unittest import TestCase
from flask import Flask
from models.topic import Topic
from models.selection import Selection
from models.student import Student
from config import *
from exts import db


# todo
class TestTopic(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config.from_object(TestConfig)
        cls.db = db
        cls.db.init_app(cls.app)
        with cls.app.app_context():
            db.create_all()

    def tearDown(self):
        pass

    def test_add(self):
        with self.app.app_context():
            _new_topic = Topic(quota=1, is_custom=False, required_skills='null', reference='null',
                               name='topic_name',
                               supervisor_id=1,
                               description='description', type_id=1)
            # topic = Topic(
            #     name='abc',
            #     supervisor_id=1,
            #     quota=1,
            #     is_custom=False,
            #     type_id=1,
            #     description='test desc',
            #     required_skills='test skills',
            #     reference='test refer'
            # )
            _new_topic.add()
            # added_topic = self.db.session.query(Topic).filter_by(name='abc').first()
            # self.assertIsNotNone(added_topic)
            # self.assertEqual(added_topic.name, 'test topic')
            # self.assertEqual(added_topic.supervisor_id, '1')
            # self.assertEqual(added_topic.quota, '10')
            # self.assertEqual(added_topic.is_custom, '0')
            # self.assertEqual(added_topic.type_id, '1')
            # self.assertEqual(added_topic.description, 'test desc')
            # self.assertEqual(added_topic.required_skills, 'test skills')
            # self.assertEqual(added_topic.reference, 'test refer')
