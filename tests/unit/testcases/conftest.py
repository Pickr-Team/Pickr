from datetime import datetime

import pytest
from flask import Flask

from models.student import Student
from models.supervisor import Supervisor
from models.selection import Selection
from models.topic import Topic
from models.type import Type
from models.deadline import Deadline
from models.note import Note
from exts import db
from blueprints.base import bp as base_bp
from blueprints.manager import bp as manager_bp
from blueprints.student import bp as student_bp
from blueprints.supervisor import bp as supervisor_bp
import secrets
from config import TestConfig


def insert_test_data(app):
    with app.app_context():
        db.create_all()

        # student doesn't have a selection
        student = Student('杨玉婷', 'Crystal', 'crystal@qq.com',
                          '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'crystal', 'SES1')
        # student have a selection
        student_2 = Student('张三', 'Zhangsan', 'zhangsan@qq.com',
                          '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'zhangsan', 'SES1')
        # student have a selection(fail)
        student_3 = Student('王五', 'wangwu', 'wangwu@qq.com',
                          '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'wangwu', 'SES1')
        # student have a custom selection
        student_4 = Student('李四', 'Lisi', 'lisi@qq.com',
                          '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'lisi', 'SES1')
        #
        student_5 = Student('老刘', 'laoliu', 'laoliu@qq.com',
                          '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'laoliu', 'SES1')

        supervisor = Supervisor('Clivia', 'Li', False, 15, 'clivia',
                                '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'clivia@qq.com',
                                'software development')
        supervisor_2 = Supervisor('Supervisor', '2', False, 10, 'supervisor_2',
                                '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'clivia@qq.com',
                                'software development')

        manager = Supervisor('Joojo', 'Walker', True, 15, 'joojo',
                             '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'joojo@qq.com',
                             'machine learning')

        _type = Type('Machine Learning')

        sup_topic_1 = Topic('Supervisor Topic 1', 1, 5, False, 1, None, None, None)
        sup_topic_2 = Topic('Supervisor Topic 2', 1, 5, False, 1, None, None, None)
        sup_topic_3 = Topic('Supervisor Topic 3', 1, 0, False, 1, None, None, None) # topic is full

        stu_topic = Topic('Student Topic', None, 1, True, 1, None, None, None)

        selection_not_custom = Selection(2)  # s1
        selection_not_custom.update(student_id=2, submit_time=None, status=1, first_topic_id=1, second_topic_id=2, third_topic_id=3, final_topic_id=None)
        selection_not_custom_fail = Selection(3)  # s2
        selection_custom = Selection(4)  # s3
        selection_custom.update(student_id=4, submit_time=None, status=1, first_topic_id=4, second_topic_id=2, third_topic_id=3, final_topic_id=None)

        db.session.add_all([student, student_2, student_3, student_4, student_5,
                            supervisor, supervisor_2, manager, _type, sup_topic_1, sup_topic_2, sup_topic_3, stu_topic,
                            selection_not_custom, selection_not_custom_fail, selection_custom])
        db.session.commit()


# @pytest.fixture: define a variable
@pytest.fixture
def app():
    app = Flask(__name__, template_folder='../../../templates')
    app.config.from_object(TestConfig)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(base_bp)
    app.register_blueprint(manager_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(supervisor_bp)
    app.secret_key = secrets.token_hex(16)
    db.init_app(app)

    insert_test_data(app)

    # before yield: setUp a variable, after yield: teardown the variable
    yield app

    with app.app_context():
        db.session.remove()
        # db.session.query(Selection).delete()
        # db.session.query(Student).delete()
        # db.session.query(Topic).delete()
        # db.session.query(Type).delete()
        # db.session.query(Supervisor).delete()
        # db.session.query(Note).delete()
        # db.session.query(Deadline).delete()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def _setup_app_context_for_test(request, app):
    """
    Given app is session-wide, sets up a app context per test to ensure that
    app and request stack is not shared between tests.
    """
    ctx = app.app_context()
    ctx.push()
    yield  # tests will run here
    ctx.pop()