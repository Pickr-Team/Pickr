from unittest import TestCase
from flask import Flask
from models.student import Student
from config import *
from exts import db
import secrets
from unittest.mock import patch, Mock

class TestStudent(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config.from_object(TestConfig)
        cls.db = db
        cls.db.init_app(cls.app)
        from models.student import Student
        from models.supervisor import Supervisor
        from models.selection import Selection
        from models.topic import Topic
        from models.type import Type
        from models.deadline import Deadline
        from models.note import Note
        from models.semester import Semester
        from models.report import Report
        from models.week import Week

        with cls.app.app_context():
            cls.db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            cls.db.drop_all()

    def tearDown(self):
        # clear data after each test
        with self.app.app_context():
            self.db.session.query(Student).delete()
            self.db.session.commit()

    def test_add(self):
        with self.app.app_context():
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
            added_student = self.db.session.query(Student).filter_by(email='zhangsan@example.com').first()
            self.assertIsNotNone(added_student)
            self.assertEqual(added_student.chinese_name, '张三')
            self.assertEqual(added_student.english_name, 'zhangsan')
            self.assertEqual(added_student.email, 'zhangsan@example.com')
            self.assertEqual(added_student.password, 'password123')
            self.assertEqual(added_student.user_name, 'zhangsan')
            self.assertEqual(added_student.class_number, 'CS101')
            self.assertEqual(added_student.graduation_year, 2025)

    def test_to_json(self):
        with self.app.app_context():
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
            self.assertIsNotNone(student)
            json_result = student.to_json()
            expected_json = {
                'id': student.id,
                'chinese_name': '张三',
                'english_name': 'zhangsan',
                'email': 'zhangsan@example.com',
                'user_name': 'zhangsan',
                'class_number': 'CS101'
            }
            self.assertDictEqual(json_result, expected_json)

    def test_get_by_name_username_class_number(self):
        with self.app.app_context():
            student_1 = Student(
                chinese_name='张三',
                english_name='zhangsan',
                email='zhangsan@example.com',
                password='password123',
                user_name='zhangsan',
                class_number='CS101',
                graduation_year=2025
            )
            student_1.add()
            student_2 = Student(
                chinese_name='李四',
                english_name='lisi',
                email='lisi@example.com',
                password='password123',
                user_name='lisi',
                class_number='CS101',
                graduation_year=2025
            )
            student_2.add()
            # chinese_name
            results = Student.get_by_name_username_class_number('张').all()
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].chinese_name, '张三')
            # english_name
            results = Student.get_by_name_username_class_number('zhang').all()
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].english_name, 'zhangsan')
            # class_number
            results = Student.get_by_name_username_class_number('CS101').all()
            self.assertEqual(len(results), 2)
            # user_name
            results = Student.get_by_name_username_class_number('san').all()
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].user_name, 'zhangsan')

    def test_1_get_id_by_english_name(self):
        with self.app.app_context():
            student_1 = Student(
                chinese_name='张杰',
                english_name='zhangjie',
                email='zhangjie@example.com',
                password='password123',
                user_name='zhangjie',
                class_number='CS101',
                graduation_year=2025
            )
            student_1.add()
            id_num = Student.get_id_by_english_name('zhangjie')
            assert id_num == 1

    def test_update(self):
        with self.app.app_context():
            student_1 = Student(
                chinese_name='张三',
                english_name='zhangsan',
                email='zhangsan@example.com',
                password='password123',
                user_name='zhangsan',
                class_number='CS101',
                graduation_year=2025
            )
            student_1.add()
            added_student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            self.assertIsNotNone(added_student)
            added_student.update(chinese_name='李四', english_name='lisi', email='lisi@qq.com', user_name='lisi', class_number='SES6', graduation_year=2025)
            self.assertEqual(added_student.chinese_name, '李四')
            self.assertEqual(added_student.english_name, 'lisi')
            self.assertEqual(added_student.email, 'lisi@qq.com')
            self.assertEqual(added_student.user_name, 'lisi')
            self.assertEqual(added_student.class_number, 'SES6')
            self.assertEqual(added_student.graduation_year, 2025)

    def test_update_pwd(self):
        with self.app.app_context():
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
            added_student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            self.assertIsNotNone(added_student)
            added_student.update_pwd('123456')
            self.assertEqual(added_student.password, '123456')

    def test_delete(self):
        with self.app.app_context():
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
            added_student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            self.assertIsNotNone(added_student)
            added_student.delete()
            deleted_student = self.db.session.query(Student).filter_by(user_name='zhangsan').first()
            self.assertIsNone(deleted_student)

    def test_get_by_id(self):
        with self.app.app_context():
            student = Student(
                chinese_name='张三123',
                english_name='zhangsan',
                email='zhangsan@example.com',
                password='password123',
                user_name='zhangsan123',
                class_number='CS101',
                graduation_year=2025
            )
            student.add()
            added_obj = Student.get_by_id(student.id)
            self.assertIsNotNone(added_obj)
            assert added_obj.user_name == 'zhangsan123'
            assert added_obj.chinese_name == '张三123'

    def test_get_num(self):
        with self.app.app_context():
            student_1 = Student(
                chinese_name='张三',
                english_name='zhangsan',
                email='zhangsan@example.com',
                password='password123',
                user_name='zhangsan',
                class_number='CS101',
                graduation_year=2025
            )
            student_1.add()
            student_2 = Student(
                chinese_name='李四',
                english_name='lisi',
                email='lisi@example.com',
                password='password123',
                user_name='lisi',
                class_number='CS101',
                graduation_year=2025
            )
            student_2.add()
            num = Student.get_num()
            assert num == 2

    def test_get_all(self):
        with self.app.app_context():
            student_1 = Student(
                chinese_name='张三',
                english_name='zhangsan',
                email='zhangsan@example.com',
                password='password123',
                user_name='zhangsan',
                class_number='CS101',
                graduation_year=2025
            )
            student_1.add()
            student_2 = Student(
                chinese_name='李四',
                english_name='lisi',
                email='lisi@example.com',
                password='password123',
                user_name='lisi',
                class_number='CS101',
                graduation_year=2025
            )
            student_2.add()
            objs = Student.get_all()
            assert len(objs) == 2
            assert objs[0].user_name == 'lisi'
            assert objs[1].user_name == 'zhangsan'

