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


class TestTopic(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config.from_object(TestConfig)
        cls.db = db
        cls.db.init_app(cls.app)
        with cls.app.app_context():
            cls.db.create_all()

            supervisor = Supervisor(first_name='supervisor', last_name='1', is_admin=False, position=100,
                                    user_name='supervisor 1',
                                    password='test', email='test', expertise='test')
            student_1 = Student(
                chinese_name='张三',
                english_name='zhangsan',
                email='zhangsan@example.com',
                password='password123',
                user_name='zhangsan',
                class_number='CS101'
            )
            student_1.add()
            student_2 = Student(
                chinese_name='李四',
                english_name='lisi',
                email='lisi@example.com',
                password='password123',
                user_name='lisi',
                class_number='CS101'
            )
            student_2.add()
            _type = Type('Game')
            cls.db.session.add_all(
                [supervisor, _type, student_1, student_2])
            cls.db.session.commit()
            # class attr
            cls.supervisor_id = supervisor.id
            cls.type_id = _type.id
            cls.student_1_id = student_1.id
            cls.student_2_id = student_2.id

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            cls.db.drop_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.session.query(Selection).delete()
            self.db.session.query(Topic).delete()
            self.db.session.commit()

    def test_add(self):
        with self.app.app_context():
            _new_topic = Topic(quota=999, is_custom=False, required_skills=None, reference=None,
                               name='topic 1', supervisor_id=None, description=None, type_id=None)
            _new_topic.add()
            added_topic = self.db.session.query(Topic).filter_by(name='topic 1').first()
            self.assertIsNotNone(added_topic)
            self.assertEqual(added_topic.name, 'topic 1')
            self.assertEqual(added_topic.quota, 999)

    def test_update(self):
        with self.app.app_context():
            new_topic = Topic(quota=999, is_custom=False, required_skills=None, reference=None,
                              name='topic 2', supervisor_id=None, description=None, type_id=None)
            new_topic.add()
            added_topic = self.db.session.query(Topic).filter_by(name='topic 2').first()
            self.assertIsNotNone(added_topic)
            added_topic.update(name='topic 222', quota=111)
            self.assertEqual(added_topic.name, 'topic 222')
            self.assertEqual(added_topic.quota, 111)

    def test_delete(self):
        with self.app.app_context():
            new_topic = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                              name='topic 3', supervisor_id=None, description=None, type_id=None)
            new_topic.add()
            added_topic = self.db.session.query(Topic).filter_by(name='topic 3').first()
            self.assertIsNotNone(added_topic)
            added_topic.delete()
            del_topic = self.db.session.query(Topic).filter_by(name='topic 3').first()
            self.assertIsNone(del_topic)

    def test_2_get_by_id(self):
        with self.app.app_context():
            new_topic = Topic(quota=555, is_custom=False, required_skills=None, reference=None,
                              name='new topic', supervisor_id=None, description=None, type_id=None)
            new_topic.add()
            topic = Topic.get_by_id(new_topic.id)
            self.assertEqual(topic.name, 'new topic')
            self.assertEqual(topic.quota, 555)

    def test_get_all(self):
        with self.app.app_context():
            new_topic_4 = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                                name='topic 4', supervisor_id=None, description=None, type_id=None)
            new_topic_4.add()
            new_topic_5 = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                                name='topic 5', supervisor_id=None, description=None, type_id=None)
            new_topic_5.add()
            new_topic_6 = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                                name='topic 6', supervisor_id=None, description=None, type_id=None)
            new_topic_6.add()
            topics_num = Topic.get_num()
            self.assertEqual(topics_num, 3)

    def test_get_all(self):
        with self.app.app_context():
            new_topic_4 = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                                name='topic 4', supervisor_id=None, description=None, type_id=None)
            new_topic_4.add()
            new_topic_5 = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                                name='topic 5', supervisor_id=None, description=None, type_id=None)
            new_topic_5.add()
            new_topic_6 = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                                name='topic 6', supervisor_id=None, description=None, type_id=None)
            new_topic_6.add()
            topics = Topic.get_all()
            self.assertEqual(len(topics), 3)
            self.assertEqual(topics[0].name, 'topic 6')
            self.assertEqual(topics[1].name, 'topic 5')
            self.assertEqual(topics[2].name, 'topic 4')

    def test_get_by_supervisor_id(self):
        with self.app.app_context():
            new_topic = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                              name='demo topic', supervisor_id=TestTopic.supervisor_id, description=None, type_id=None)
            new_topic.add()
            topics = Topic.get_by_supervisor_id(TestTopic.supervisor_id)  # custom + not custom
            self.assertEqual(len(topics), 1)
            self.assertEqual(topics[0].name, 'demo topic')

    def test_get_by_supervisor_id_not_custom(self):
        with self.app.app_context():
            custom_topic = Topic(quota=1, is_custom=True, required_skills=None, reference=None,
                                 name='custom topic', supervisor_id=TestTopic.supervisor_id, description=None,
                                 type_id=None)
            custom_topic.add()
            new_topic = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                              name='new topic', supervisor_id=TestTopic.supervisor_id, description=None, type_id=None)
            new_topic.add()
            topics = Topic.get_by_supervisor_id_not_custom(TestTopic.supervisor_id)
            self.assertEqual(len(topics), 1)
            self.assertEqual(topics[0].name, 'new topic')

    def test_get_by_type_id(self):
        with self.app.app_context():
            custom_topic = Topic(quota=1, is_custom=True, required_skills=None, reference=None,
                                 name='custom topic', supervisor_id=TestTopic.supervisor_id, description=None,
                                 type_id=TestTopic.type_id)
            custom_topic.add()
            new_topic = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                              name='new topic', supervisor_id=TestTopic.supervisor_id, description=None,
                              type_id=TestTopic.type_id)
            new_topic.add()
            new_topic_2 = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                                name='new topic 2', supervisor_id=TestTopic.supervisor_id, description=None,
                                type_id=None)
            new_topic_2.add()
            topics = Topic.get_by_type_id(TestTopic.type_id)
            self.assertEqual(len(topics), 2)
            self.assertEqual(topics[0].name, 'custom topic')
            self.assertEqual(topics[1].name, 'new topic')

    def test_1_get_by_name_or_id(self):
        with self.app.app_context():
            new_topic = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                              name='new topic 1', supervisor_id=TestTopic.supervisor_id, description=None,
                              type_id=TestTopic.type_id)
            new_topic.add()
            new_topic_2 = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                                name='new topic 2', supervisor_id=TestTopic.supervisor_id, description=None,
                                type_id=None)
            new_topic_2.add()
            t_1 = Topic.get_by_name_or_id('PK0001')
            t_2 = Topic.get_by_name_or_id('PK9999')
            self.assertEqual(len(t_1), 1)
            self.assertEqual(t_1[0].name, 'new topic 1')
            self.assertEqual(len(t_2), 0)  # [] is not None

    def test_get_selected_num(self):
        with self.app.app_context():
            s1 = Selection(TestTopic.student_1_id)
            s1.update_status(0)
            s1.add()
            s2 = Selection(TestTopic.student_2_id)
            s2.update_status(0)
            s2.add()
            new_topic = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                              name='new topic 1', supervisor_id=TestTopic.supervisor_id, description=None,
                              type_id=TestTopic.type_id)
            new_topic.add()
            new_topic_2 = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                                name='new topic 2', supervisor_id=TestTopic.supervisor_id, description=None,
                                type_id=TestTopic.type_id)
            new_topic_2.add()
            s1.first_topic_id = new_topic.id
            s2.second_topic_id = new_topic.id
            new_topic_selected_num = new_topic.get_selected_num()
            new_topic_2_selected_num = new_topic_2.get_selected_num()
            self.assertEqual(2, new_topic_selected_num)
            self.assertEqual(0, new_topic_2_selected_num)

    def test_get_selected_num_total(self):
        with self.app.app_context():
            s1 = Selection(TestTopic.student_1_id)
            s1.update_status(0)
            s1.add()
            s2 = Selection(TestTopic.student_2_id)
            s2.update_status(999)
            s2.add()
            new_topic = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                              name='new topic 1', supervisor_id=TestTopic.supervisor_id, description=None,
                              type_id=TestTopic.type_id)
            new_topic.add()
            new_topic_2 = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                                name='new topic 2', supervisor_id=TestTopic.supervisor_id, description=None,
                                type_id=TestTopic.type_id)
            new_topic_2.add()

            s1.first_topic_id = new_topic.id
            s1.second_topic_id = new_topic.id

            s2.second_topic_id = new_topic.id
            new_topic_selected_num = new_topic.get_selected_num_total()
            new_topic_2_selected_num = new_topic_2.get_selected_num_total()
            self.assertEqual(2, new_topic_selected_num)
            self.assertEqual(0, new_topic_2_selected_num)

    def test_get_selected_num_final(self):
        with self.app.app_context():
            s1 = Selection(TestTopic.student_1_id)
            s1.update_status(3)
            s1.add()
            new_topic = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                              name='new topic 1', supervisor_id=TestTopic.supervisor_id, description=None,
                              type_id=TestTopic.type_id)
            new_topic.add()
            new_topic_2 = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                                name='new topic 2', supervisor_id=TestTopic.supervisor_id, description=None,
                                type_id=TestTopic.type_id)
            new_topic_2.add()

            s1.final_topic_id = new_topic.id
            s1.second_topic_id = new_topic.id

            s2 = Selection(TestTopic.student_2_id)
            s2.update_status(999)
            s2.add()
            s2.final_topic_id = new_topic_2.id
            s2.second_topic_id = new_topic_2.id
            new_topic_final_num = new_topic.get_selected_num_final()
            new_topic_2_final_num = new_topic_2.get_selected_num_final()
            self.assertEqual(new_topic_final_num, 1)
            self.assertEqual(new_topic_2_final_num, 0)

    def test_get_selected_num_final(self):
        with self.app.app_context():
            new_topic = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                              name='new topic 1', supervisor_id=TestTopic.supervisor_id, description=None,
                              type_id=TestTopic.type_id)
            new_topic.add()
            name = new_topic.get_supervisor_name()
            self.assertEqual('supervisor 1', name)

    def test_get_type_name(self):
        with self.app.app_context():
            new_topic = Topic(quota=1, is_custom=False, required_skills=None, reference=None,
                              name='new topic 1', supervisor_id=TestTopic.supervisor_id, description=None,
                              type_id=TestTopic.type_id)
            new_topic.add()
            name = new_topic.get_type_name()
            self.assertEqual('Game', name)

    def test_get_all_quota(self):
        with self.app.app_context():
            topics = [
                Topic(name='Topic 1', supervisor_id=None, type_id=None, quota=10, is_custom=False, description=None,
                      required_skills=None, reference=None),
                Topic(name='Topic 2', supervisor_id=None, type_id=None, quota=20, is_custom=False, description=None,
                      required_skills=None, reference=None),
                Topic(name='Topic 3', supervisor_id=None, type_id=None, quota=30, is_custom=True, description=None,
                      required_skills=None, reference=None),
            ]
            db.session.add_all(topics)
            db.session.commit()
            expected_quota = 30
            actual_quota = Topic.get_all_quota()  # None
            self.assertEqual(expected_quota, actual_quota)

    def test_get_num_not_custom(self):
        with self.app.app_context():
            topics = [
                Topic(name='Topic 1', supervisor_id=None, type_id=None, quota=10, is_custom=False, description=None,
                      required_skills=None, reference=None),
                Topic(name='Topic 2', supervisor_id=None, type_id=None, quota=20, is_custom=False, description=None,
                      required_skills=None, reference=None),
                Topic(name='Topic 3', supervisor_id=None, type_id=None, quota=30, is_custom=True, description=None,
                      required_skills=None, reference=None),
            ]
            db.session.add_all(topics)
            db.session.commit()
            expected_num = 2
            actual_num = Topic.get_num_not_custom()  # None
            self.assertEqual(expected_num, actual_num)

    def test_get_num_custom(self):
        with self.app.app_context():
            topics = [
                Topic(name='Topic 1', supervisor_id=None, type_id=None, quota=10, is_custom=False, description=None,
                      required_skills=None, reference=None),
                Topic(name='Topic 2', supervisor_id=None, type_id=None, quota=20, is_custom=False, description=None,
                      required_skills=None, reference=None),
                Topic(name='Topic 3', supervisor_id=None, type_id=None, quota=30, is_custom=True, description=None,
                      required_skills=None, reference=None),
            ]
            db.session.add_all(topics)
            db.session.commit()
            expected_num = 1
            actual_num = Topic.get_num_custom()  # None
            self.assertEqual(expected_num, actual_num)

    def test_get_all_custom(self):
        with self.app.app_context():
            topics = [
                Topic(name='Topic 1', supervisor_id=None, type_id=None, quota=10, is_custom=False, description=None,
                      required_skills=None, reference=None),
                Topic(name='Topic 2', supervisor_id=None, type_id=None, quota=20, is_custom=False, description=None,
                      required_skills=None, reference=None),
                Topic(name='Topic 3', supervisor_id=None, type_id=None, quota=30, is_custom=True, description=None,
                      required_skills=None, reference=None),
            ]
            db.session.add_all(topics)
            db.session.commit()
            custom_topics = Topic.get_all_custom()  # None
            self.assertEqual(1, len(custom_topics))
            self.assertEqual('Topic 3', custom_topics[0].name)
