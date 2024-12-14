from unittest import TestCase
from flask import Flask
from models.selection import Selection
from models.student import Student
from models.topic import Topic
from models.supervisor import Supervisor
from models.type import Type
from config import *
from exts import db


class TestSelection(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config.from_object(TestConfig)
        cls.db = db
        cls.db.init_app(cls.app)
        with cls.app.app_context():
            db.create_all()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            student = cls.db.session.query(Student).filter_by(user_name='student-test').first()
            supervisor = cls.db.session.query(Supervisor).filter_by(user_name='supervisor-test').first()
            topic_1 = cls.db.session.query(Topic).filter_by(name='test_topic_1').first()
            topic_2 = cls.db.session.query(Topic).filter_by(name='test_topic_2').first()
            topic_3 = cls.db.session.query(Topic).filter_by(name='test_topic_3').first()
            _type = cls.db.session.query(Type).filter_by(name='Game').first()
            selection = cls.db.session.query(Selection).filter_by(student_id=student.id).first()

            if student:
                cls.db.session.delete(student)
            if supervisor:
                cls.db.session.delete(supervisor)
            if topic_1:
                cls.db.session.delete(topic_1)
            if topic_2:
                cls.db.session.delete(topic_2)
            if topic_3:
                cls.db.session.delete(topic_3)
            if selection:
                cls.db.session.delete(selection)
            if _type:
                cls.db.session.delete(_type)

            cls.db.session.commit()

    # add selection: not custom
    def test_1_add(self):
        with self.app.app_context():
            student = Student(
                chinese_name='张三',
                english_name='zhangsan',
                email='zhangsan@example.com',
                password='password123',
                user_name='student-test',
                class_number='CS101'
            )

            supervisor = Supervisor(first_name='test', last_name='test', is_admin=False, position=100,
                                    user_name='supervisor-test',
                                    password='test', email='test', expertise='test')

            topic1 = Topic(quota=1, is_custom=False, required_skills='null', reference='null',
                           name='test_topic_1',
                           supervisor_id=supervisor.id,
                           description='description', type_id=1)
            topic2 = Topic(quota=1, is_custom=False, required_skills='null', reference='null',
                           name='test_topic_2',
                           supervisor_id=supervisor.id,
                           description='description', type_id=1)
            topic3 = Topic(quota=1, is_custom=False, required_skills='null', reference='null',
                           name='test_topic_3',
                           supervisor_id=supervisor.id,
                           description='description', type_id=1)

            _type = Type(name='Game')

            topic1.supervisor_id = supervisor.id
            topic2.supervisor_id = supervisor.id
            topic3.supervisor_id = supervisor.id

            topic1.type_id = _type.id
            topic2.type_id = _type.id
            topic3.type_id = _type.id

            self.db.session.add_all([student, topic1, topic2, topic3, supervisor, _type])
            self.db.session.commit()

            obj = Selection(student_id=student.id)
            obj.first_topic_id = topic1.id
            obj.second_topic_id = topic2.id
            obj.third_topic_id = topic3.id
            obj.status = 1
            self.db.session.add(obj)
            self.db.session.commit()

            _added = self.db.session.query(Selection).filter_by(student_id=student.id).first()
            self.assertIsNotNone(_added)
            self.assertEqual(_added.student_id, student.id)
            self.assertEqual(_added.status, 1)
            self.assertEqual(_added.first_topic_id, topic1.id)
            self.assertEqual(_added.second_topic_id, topic2.id)
            self.assertEqual(_added.third_topic_id, topic3.id)

    def test_2_update(self):
        with self.app.app_context():
            student = self.db.session.query(Student).filter_by(user_name='student-test').first()
            _added = self.db.session.query(Selection).filter_by(student_id=student.id).first()
            topic_1 = self.db.session.query(Topic).filter_by(name='test_topic_1').first()
            topic_2 = self.db.session.query(Topic).filter_by(name='test_topic_2').first()
            topic_3 = self.db.session.query(Topic).filter_by(name='test_topic_3').first()
            self.assertIsNotNone(_added)
            _added.update(student.id, '2025-11-30 23:59', 4, topic_1.id, topic_2.id, topic_3.id, topic_1.id)
            self.assertEqual(_added.status, 4)
            self.assertEqual(_added.final_topic_id, topic_1.id)

    def test_3_getAll(self):
        with self.app.app_context():
            selections = Selection.get_all()
            print('selections>>>', selections)

    def test_4_delete(self):
        with self.app.app_context():
            student = self.db.session.query(Student).filter_by(user_name='student-test').first()
            _added = self.db.session.query(Selection).filter_by(student_id=student.id).first()
            self.assertIsNotNone(_added)
            _added.delete()
            _deleted = self.db.session.query(Selection).filter_by(student_id=student.id).first()
            self.assertIsNone(_deleted)

    # todo: add selection: custom