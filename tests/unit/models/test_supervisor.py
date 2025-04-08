from unittest import TestCase
from flask import Flask
from models.student import Student
from models.supervisor import Supervisor
from models.selection import Selection
from models.topic import Topic
from models.type import Type
from models.supervisor import Supervisor
from config import *
from exts import db
import unittest


class TestSupervisor(TestCase):
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

    # clear data after each test
    def tearDown(self):
        with self.app.app_context():
            self.db.session.query(Topic).delete()
            self.db.session.query(Type).delete()
            self.db.session.query(Supervisor).delete()
            self.db.session.commit()

    def test_add(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            supervisor = Supervisor('Clivia', 'Li', False, 10, 'clivia', '123456', None, None)
            admin.add()
            supervisor.add()
            added_admin = self.db.session.query(Supervisor).filter_by(user_name='joojo').first()
            added_supervisor = self.db.session.query(Supervisor).filter_by(user_name='clivia').first()
            self.assertIsNotNone(added_admin)
            self.assertEqual(added_admin.first_name, 'Joojo')
            self.assertEqual(added_admin.last_name, 'Walker')
            self.assertEqual(added_admin.is_admin, True)
            self.assertEqual(added_admin.position, 100)
            self.assertEqual(added_admin.user_name, 'joojo')
            self.assertEqual(added_admin.password, '123456')
            self.assertIsNotNone(added_supervisor)
            self.assertEqual(added_supervisor.first_name, 'Clivia')
            self.assertEqual(added_supervisor.last_name, 'Li')
            self.assertEqual(added_supervisor.is_admin, False)
            self.assertEqual(added_supervisor.position, 10)
            self.assertEqual(added_supervisor.user_name, 'clivia')
            self.assertEqual(added_supervisor.password, '123456')

    def test_delete(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            admin.add()
            added_admin = self.db.session.query(Supervisor).filter_by(user_name='joojo').first()
            self.assertIsNotNone(added_admin)
            added_admin.delete()
            deleted_admin = self.db.session.query(Supervisor).filter_by(user_name='joojo').first()
            self.assertIsNone(deleted_admin)

    def test_update(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            admin.add()
            added_admin = self.db.session.query(Supervisor).filter_by(user_name='joojo').first()
            self.assertIsNotNone(added_admin)
            added_admin.update(first_name='James', last_name='Jones', is_admin=False, position=1, user_name='james',
                               password='789', email='james@qq.com', expertise='james expertise')
            updated_admin = self.db.session.query(Supervisor).filter_by(user_name='james').first()
            self.assertIsNotNone(updated_admin)
            self.assertEqual(updated_admin.first_name, 'James')
            self.assertEqual(updated_admin.last_name, 'Jones')
            self.assertEqual(updated_admin.is_admin, False)
            self.assertEqual(updated_admin.position, 1)
            self.assertEqual(updated_admin.user_name, 'james')
            self.assertEqual(updated_admin.password, '789')
            self.assertEqual(updated_admin.email, 'james@qq.com')
            self.assertEqual(updated_admin.expertise, 'james expertise')

    def test_get_by_id(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            admin.add()
            added_admin = Supervisor.get_by_id(admin.id)
            self.assertIsNotNone(added_admin)
            self.assertEqual(added_admin.first_name, 'Joojo')
            self.assertEqual(added_admin.last_name, 'Walker')
            self.assertEqual(added_admin.is_admin, True)
            self.assertEqual(added_admin.position, 100)
            self.assertEqual(added_admin.user_name, 'joojo')
            self.assertEqual(added_admin.password, '123456')

    def test_get_num(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            supervisor = Supervisor('Clivia', 'Li', False, 10, 'clivia', '123456', None, None)
            admin.add()
            supervisor.add()
            num = Supervisor.get_num()
            assert num == 2

    def test_get_all(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            supervisor = Supervisor('Clivia', 'Li', False, 10, 'clivia', '123456', None, None)
            admin.add()
            supervisor.add()
            objs = Supervisor.get_all()
            assert len(objs) == 2
            assert objs[0].user_name == 'clivia'
            assert objs[1].user_name == 'joojo'

    def test_update_pwd(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            admin.add()
            added = self.db.session.query(Supervisor).filter_by(user_name='joojo').first()
            self.assertIsNotNone(added)
            added.update_pwd('098765')
            self.assertEqual(added.password, '098765')

    def test_has_topic_false(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            admin.add()
            assert admin.has_topics is False

    # todo
    # def test_has_topic_true(self):
    #     with self.app.app_context():
    #         _type = Type(name='Game')
    #         _type.add()
    #         supervisor = Supervisor('Clivia', 'Li', False, 20, 'clivia', '123456', None, None)
    #         supervisor.add()
    #         topic = Topic('topic', 1, 10, False, _type.id, None, None, None)
    #         topic.add()
    #         assert supervisor.has_topics is True

    def test_get_all_admins(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            supervisor = Supervisor('Clivia', 'Li', False, 10, 'clivia', '123456', None, None)
            admin.add()
            supervisor.add()
            objs = Supervisor.get_all_admins()
            assert len(objs) == 1
            assert objs[0].user_name == 'joojo'

    def test_get_all_supervisor(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            supervisor = Supervisor('Clivia', 'Li', False, 10, 'clivia', '123456', None, None)
            admin.add()
            supervisor.add()
            objs = Supervisor.get_all_supervisors()
            assert len(objs) == 1
            assert objs[0].user_name == 'clivia'

    def test_1_get_id_by_username(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            admin.add()
            id_num = Supervisor.get_id_by_username('joojo')
            assert id_num == 1

    def test_get_id_by_name(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            admin.add()
            obj = Supervisor.get_by_name('joojo walker')
            assert obj.first_name == 'Joojo'
            assert obj.last_name == 'Walker'
            assert obj.user_name == 'joojo'

    def test_get_topic_total_quota(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            admin.add()
            topic_num = admin.get_topic_total_quota()
            assert topic_num == 0
            _type = Type(name='Game')
            _type.add()
            supervisor = Supervisor('Clivia', 'Li', False, 20, 'clivia', '123456', None, None)
            supervisor.add()
            topic = Topic('topic', supervisor.id, 10, False, _type.id, None, None, None)
            topic.add()
            custom_topic = Topic('custom topic', None, 1, True, _type.id, None, None, None)
            custom_topic.add()
            student = Student(
                chinese_name='张三',
                english_name='zhangsan',
                email='zhangsan@example.com',
                password='password123',
                user_name='zhangsan',
                class_number='CS101',
                graduation_year=2025
            )
            student.add()
            selection = Selection(1)
            selection.update(student_id=student.id, status=4, first_topic_id=custom_topic.id,
                             final_topic_id=custom_topic.id, submit_time=None, second_topic_id=None,
                             third_topic_id=None)
            custom_topic.update(supervisor_id=supervisor.id, name='custom topic', quota=1, is_custom=True,
                                type_id=_type.id, description=None, required_skills=None, reference=None)
            topic_num_ = supervisor.get_topic_total_quota()
            assert topic_num_ == 11

    def test_get_not_custom_topic_num(self):
        with self.app.app_context():
            admin = Supervisor('Joojo', 'Walker', True, 100, 'joojo', '123456', None, None)
            admin.add()
            topic_num = admin.get_not_custom_topic_num()
            assert topic_num == 0
            _type = Type(name='Game')
            _type.add()
            supervisor = Supervisor('Clivia', 'Li', False, 20, 'clivia', '123456', None, None)
            supervisor.add()
            topic = Topic('topic', supervisor.id, 10, False, _type.id, None, None, None)
            topic.add()
            topic_num_ = supervisor.get_topic_total_quota()
            assert topic_num_ == 10

    # todo
    # def test_get_total_final_selections(self):
    #     with self.app.app_context():
    #         student_1 = Student(
    #             chinese_name='张三',
    #             english_name='zhangsan',
    #             email='zhangsan@example.com',
    #             password='password123',
    #             user_name='zhangsan',
    #             class_number='CS101'
    #         )
    #         student_1.add()
    #         student_2 = Student(
    #             chinese_name='李四',
    #             english_name='lisi',
    #             email='lisi@example.com',
    #             password='password123',
    #             user_name='lisi',
    #             class_number='CS101'
    #         )
    #         student_2.add()
    #         s_1 = Selection(student_1.id)
    #         s_2 = Selection(student_2.id)
    #         supervisor = Supervisor('Clivia', 'Li', False, 20, 'clivia', '123456', None, None)
    #         supervisor.add()
    #         _type = Type(name='Game')
    #         _type.add()
    #         custom_topic = Topic('custom topic', None, 1, True, _type.id, None, None, None)
    #         custom_topic.add()
    #         custom_topic.update(supervisor_id=supervisor.id, name='custom topic', quota=1, is_custom=True,
    #                             type_id=_type.id,
    #                             description=None, required_skills=None, reference=None)
    #         s_1.update(student_id=student_1.id, status=4, first_topic_id=custom_topic.id,
    #                    final_topic_id=custom_topic.id, submit_time=None, second_topic_id=None,
    #                    third_topic_id=None)
    #         topic_1 = Topic('topic', supervisor.id, 5, False, _type.id, None, None, None)
    #         topic_1.add()
    #         s_2.update_final_topic_id(topic_1.id)
    #         selections_num = supervisor.get_total_final_selections()
    #         print('selections_num???', selections_num)
    #         assert selections_num == 2
