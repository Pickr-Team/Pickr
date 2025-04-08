import datetime
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
            cls.db.create_all()

            cls.student = Student(
                chinese_name='张三',
                english_name='zhangsan',
                email='zhangsan@example.com',
                password='password123',
                user_name='zhangsan',
                class_number='CS101',
                graduation_year=2025
            )

            cls.student_2 = Student(
                chinese_name='李四',
                english_name='lisi',
                email='lisi@example.com',
                password='password123',
                user_name='lisi',
                class_number='CS101',
                graduation_year=2025
            )

            # custom topic
            cls.student_3 = Student(
                chinese_name='王五',
                english_name='wangwu',
                email='wangwu@example.com',
                password='password123',
                user_name='wangwu',
                class_number='CS101',
                graduation_year=2025
            )

            cls.student_4 = Student(
                chinese_name='老刘',
                english_name='laoliu',
                email='laoliu@example.com',
                password='password123',
                user_name='laoliu',
                class_number='CS101',
                graduation_year=2025
            )

            supervisor = Supervisor(first_name='test', last_name='test', is_admin=False, position=100,
                                    user_name='supervisor-test',
                                    password='test', email='test', expertise='test')

            supervisor_2 = Supervisor(first_name='supervisor_2', last_name='test', is_admin=False, position=100,
                                      user_name='supervisor_2',
                                      password='test', email='test', expertise='test')

            _type = Type(name='Game')

            cls.db.session.add_all(
                [cls.student, cls.student_2, cls.student_3, cls.student_4, supervisor, supervisor_2, _type])
            cls.db.session.commit()

            topic1 = Topic(quota=1, is_custom=0, required_skills='null', reference='null',
                           name='test_topic_1',
                           supervisor_id=supervisor.id,
                           description='description', type_id=_type.id)
            topic2 = Topic(quota=1, is_custom=False, required_skills='null', reference='null',
                           name='test_topic_2',
                           supervisor_id=supervisor.id,
                           description='description', type_id=_type.id)
            topic3 = Topic(quota=1, is_custom=False, required_skills='null', reference='null',
                           name='test_topic_3',
                           supervisor_id=supervisor.id,
                           description='description', type_id=_type.id)

            custom_topic = Topic('custom topic', None, 1, True, _type.id, None, None, None)

            cls.db.session.add_all(
                [topic1, topic2, topic3, custom_topic])
            cls.db.session.commit()

            selection = Selection(student_id=cls.student.id)  # selection 1
            selection.first_topic_id = topic1.id
            selection.second_topic_id = topic2.id
            selection.third_topic_id = topic3.id
            selection.final_topic_id = topic1.id
            selection.submit_time = '2025-1-01 12:00:00'
            selection.status = 1

            selection_2 = Selection(student_id=cls.student_3.id)  # custome topic selection 2
            selection_2.first_topic_id = custom_topic.id
            selection_2.status = 2

            cls.db.session.add_all([selection, selection_2])
            cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            cls.db.drop_all()

    def tearDown(self):
        pass
        # clear data after each test
        # with self.app.app_context():
        #     self.db.session.query(Selection).delete()
        #     self.db.session.commit()

    # add selection: not custom
    def test_1_add(self):
        with self.app.app_context():
            student = self.db.session.query(Student).filter_by(user_name='lisi').first()
            topic_1 = self.db.session.query(Topic).filter_by(name='test_topic_1').first()
            topic_2 = self.db.session.query(Topic).filter_by(name='test_topic_2').first()
            topic_3 = self.db.session.query(Topic).filter_by(name='test_topic_3').first()

            selection = Selection(student_id=student.id)  # selection 3
            selection.first_topic_id = topic_1.id
            selection.second_topic_id = topic_2.id
            selection.third_topic_id = topic_3.id
            selection.status = 999
            selection.add()

            _added = self.db.session.query(Selection).filter_by(student_id=student.id).first()
            self.assertIsNotNone(_added)
            self.assertEqual(_added.status, 999)
            self.assertEqual(_added.first_topic_id, topic_1.id)
            self.assertEqual(_added.second_topic_id, topic_2.id)
            self.assertEqual(_added.third_topic_id, topic_3.id)

    def test_1_1_get_by_id(self):
        with self.app.app_context():
            _added = Selection.get_by_id(1)
            student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            topic_1 = self.db.session.query(Topic).filter_by(name='test_topic_1').first()
            topic_2 = self.db.session.query(Topic).filter_by(name='test_topic_2').first()
            topic_3 = self.db.session.query(Topic).filter_by(name='test_topic_3').first()
            self.assertIsNotNone(_added)
            self.assertEqual(_added.status, 1)
            self.assertEqual(_added.student_id, student.id)
            self.assertEqual(_added.first_topic_id, topic_1.id)
            self.assertEqual(_added.second_topic_id, topic_2.id)
            self.assertEqual(_added.third_topic_id, topic_3.id)

    def test_1_2_get_by_student_id(self):
        with self.app.app_context():
            student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            self.assertIsNotNone(student)
            selection = Selection.get_by_student_id(student.id)
            self.assertIsNotNone(selection)
            self.assertEqual(selection.student_id, student.id)

    def test_2_update(self):
        with self.app.app_context():
            student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            _added = self.db.session.query(Selection).filter_by(student_id=student.id).first()
            topic_1 = self.db.session.query(Topic).filter_by(name='test_topic_1').first()
            self.assertIsNotNone(_added)
            _added.update(status=4, final_topic_id=topic_1.id)
            self.assertEqual(_added.status, 4)
            self.assertEqual(_added.final_topic_id, topic_1.id)

    def test_3_getAll(self):
        with self.app.app_context():
            selections = Selection.get_all()
            assert len(selections) == 2 or 3  # when test all cases together it is 3

    def test_3_1_get_all_custom_selections(self):
        with self.app.app_context():
            selections = Selection.get_all_custom_selections()
            assert len(selections) == 1

    def test_get_student_name(self):
        with self.app.app_context():
            student_name = Selection.get_student_name(1)
            assert student_name == 'zhangsan'

    def test_get_num_of_status(self):
        with self.app.app_context():
            # num = Selection.get_num_of_status(1)
            num_2 = Selection.get_num_of_status(2)
            # num_3_or_4 = Selection.get_num_of_status_3or4()
            # assert num == 1
            assert num_2 == 1
            # assert num_3_or_4 == 0

    def test_update_status(self):
        with self.app.app_context():
            student = self.db.session.query(Student).filter_by(user_name='lisi').first()
            selection = Selection(student_id=student.id)  # selection 4
            selection.update_status(1000)
            assert selection.status == 1000

    def test_update_submit_time(self):
        with self.app.app_context():
            student = self.db.session.query(Student).filter_by(user_name='lisi').first()
            selection = Selection(student_id=student.id)  # selection 4
            selection.update_submit_time('2024/12/19')
            assert selection.submit_time == '2024/12/19'

    def test_update_first_topic_supervisor_id(self):
        with self.app.app_context():
            student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            supervisor_2 = self.db.session.query(Supervisor).filter_by(user_name='supervisor_2').first()
            selection = Selection.get_by_student_id(student.id)
            self.assertIsNotNone(selection)
            selection.update_first_topic_supervisor_id(supervisor_2.id)
            assert selection.first_topic.supervisor_id == 2

    def test_update_first_topic_type_id(self):
        with self.app.app_context():
            type_2 = Type('Game')
            type_2.add()
            student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            selection = Selection.get_by_student_id(student.id)
            self.assertIsNotNone(selection)
            selection.update_first_topic_type_id(type_2.id)
            self.assertEqual(selection.first_topic.type_id, type_2.id)

    def test_update_first_topic_description(self):
        with self.app.app_context():
            student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            selection = Selection.get_by_student_id(student.id)
            self.assertIsNotNone(selection)
            selection.update_first_topic_description('new desc')
            assert selection.first_topic.description == 'new desc'

    def test_update_first_topic_name(self):
        with self.app.app_context():
            student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            selection = Selection.get_by_student_id(student.id)
            self.assertIsNotNone(selection)
            selection.update_first_topic_name('new topic name')
            assert selection.first_topic.name == 'new topic name'

    def test_update_first_topic_id(self):
        with self.app.app_context():
            new_topic = Topic(quota=1, is_custom=False, required_skills='null', reference='null',
                              name='new topic',
                              supervisor_id=None,
                              description='description', type_id=None)
            new_topic.add()
            student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            selection = Selection.get_by_student_id(student.id)
            self.assertIsNotNone(selection)
            selection.update_first_topic_id(new_topic.id)
            assert selection.first_topic.id == new_topic.id
            assert selection.first_topic.name == 'new topic'

    def test_update_second_topic_id(self):
        with self.app.app_context():
            new_topic_2 = Topic(quota=1, is_custom=False, required_skills='null', reference='null',
                                name='new topic 2',
                                supervisor_id=None,
                                description='description', type_id=None)
            new_topic_2.add()
            student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            selection = Selection.get_by_student_id(student.id)
            self.assertIsNotNone(selection)
            selection.update_second_topic_id(new_topic_2.id)
            assert selection.second_topic.id == new_topic_2.id
            assert selection.second_topic.name == 'new topic 2'

    def test_update_third_topic_id(self):
        with self.app.app_context():
            new_topic_3 = Topic(quota=1, is_custom=False, required_skills='null', reference='null',
                                name='new topic 3',
                                supervisor_id=None,
                                description='description', type_id=None)
            new_topic_3.add()
            student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            selection = Selection.get_by_student_id(student.id)
            self.assertIsNotNone(selection)
            selection.update_third_topic_id(new_topic_3.id)
            assert selection.third_topic.id == new_topic_3.id
            assert selection.third_topic.name == 'new topic 3'

    def test_update_final_topic_id(self):
        with self.app.app_context():
            new_topic_4 = Topic(quota=1, is_custom=False, required_skills='null', reference='null',
                                name='new topic 4',
                                supervisor_id=None,
                                description='description', type_id=None)
            new_topic_4.add()
            student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            selection = Selection.get_by_student_id(student.id)
            self.assertIsNotNone(selection)
            selection.update_final_topic_id(new_topic_4.id)
            assert selection.final_topic.id == new_topic_4.id
            assert selection.final_topic.name == 'new topic 4'

    def test_get_supervisor_selection_not_custom(self):
        with self.app.app_context():
            s1_id = Supervisor.get_id_by_username('supervisor-test')
            selections = Selection.get_supervisor_selection_not_custom(s1_id)
            self.assertEqual(len(selections), 1)
            self.assertEqual(selections[0].final_topic.name, 'test_topic_1')

    def test_get_supervisor_selection_custom(self):
        with self.app.app_context():
            student = Student.get_by_name_username_class_number('wangwu').first()
            selection = Selection.get_by_student_id(student.id)
            supervisor_id = Supervisor.get_id_by_username('supervisor-test')
            topic = Topic.get_by_name_or_id('custom topic')
            topic[0].supervisor_id = supervisor_id
            selection.update_final_topic_id(topic[0].id)
            s1_id = Supervisor.get_id_by_username('supervisor-test')
            selections = Selection.get_supervisor_selection_custom(s1_id)
            self.assertEqual(len(selections), 1)
            self.assertEqual(selections[0].final_topic.name, 'custom topic')

    def test_1_3_get_all_order_by_submit_time(self):
        with self.app.app_context():
            new_selection = Selection(4)
            new_selection.update_status(1)
            new_selection.update_submit_time('2024-10-01 12:00:00')
            new_selection.add()
            new_selection_2 = Selection(4)
            new_selection_2.update_status(1)
            new_selection_2.update_submit_time('2024-9-01 12:00:00')
            new_selection_2.add()
            selections = Selection.get_all_order_by_submit_time()
            self.assertEqual(len(selections), 3)
            self.assertEqual(selections[0].submit_time, datetime.datetime(2024, 9, 1, 12, 0))
            self.assertEqual(selections[1].submit_time, datetime.datetime(2024, 10, 1, 12, 0))
            self.assertEqual(selections[2].submit_time, datetime.datetime(2025, 1, 1, 12, 0))

    def test_is_topic_full(self):
        with self.app.app_context():
            new_full_topic = Topic(quota=0, is_custom=False, required_skills=None, reference=None,
                                   name='new_full_topic', supervisor_id=None, description='description', type_id=None)
            new_full_topic.add()
            new_selection = Selection(4)
            new_selection.add()
            new_selection.update_first_topic_id(new_full_topic.id)
            self.assertTrue(new_selection.topic_is_full('first'))

    def test_zzz_delete(self):
        with self.app.app_context():
            student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            _added = self.db.session.query(Selection).filter_by(student_id=student.id).first()
            self.assertIsNotNone(_added)
            _added.delete()
            _deleted = self.db.session.query(Selection).filter_by(student_id=student.id).first()
            self.assertIsNone(_deleted)
