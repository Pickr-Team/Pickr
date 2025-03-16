from flask import Flask
from sqlalchemy import text
from models.selection import Selection
from models.student import Student
from exts import db
from models.supervisor import Supervisor
from models.topic import Topic
from models.type import Type
from models.deadline import Deadline
from models.semester import Semester
from models.report import Report
from models.note import Note

from config import TestConfig

app = Flask(__name__)
app.config.from_object(TestConfig)
db.init_app(app)


def init_db():
    with app.app_context():
        db.create_all()


def clear_db():
    with app.app_context():
        db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))
        db.drop_all()
        db.session.execute(text('SET FOREIGN_KEY_CHECKS = 1;'))
        db.create_all()
        db.session.commit()


def creat_one_student():
    with app.app_context():
        new_student = Student(
            chinese_name="赵程鑫",
            english_name="Chengxin Zhao",
            class_number="2020180",
            email="2020180@zy",
            password='8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
            user_name="202118020103"
        )
        db.session.add(new_student)
        db.session.commit()


def create_one_supervisor():
    with app.app_context():
        new_supervisor = Supervisor(
            first_name="Li",
            last_name="Clivia",
            is_admin=0,
            position=4,
            user_name="clivia",
            password="8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
            email="clivia@zy.cdut.edu.cn",
            expertise='expertise'
        )
        db.session.add(new_supervisor)
        db.session.commit()


def create_one_manager():
    with app.app_context():
        new_supervisor = Supervisor(
            first_name="Walker",
            last_name="Joojo",
            is_admin=1,
            position=0,
            user_name="joojo",
            password="8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
            email="joojo@zy.cdut.edu.cn",
            expertise='expertise'
        )
        db.session.add(new_supervisor)
        db.session.commit()


# run file in python console!!!
if __name__ == "__main__":
    init_db()
    clear_db()
    creat_one_student()
    create_one_supervisor()
    create_one_manager()