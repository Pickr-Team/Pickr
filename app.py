from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models.deadline import Deadline
from models.student import Student
from models.topic import Topic
from models.selection import Selection
from models.db_instance import db

app = Flask(__name__)

'''Set up database'''
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'demo'
USERNAME = 'root'
PASSWORD = '20020316'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
db.init_app(app)


def create_tables():
    db.create_all()


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/topic_list')
def topic_list():
    return render_template('topic_list.html')


@app.route('/add_student')
def add_student():
    new_student = Student(
        chinese_name='王小明',
        english_name='Wang Xiaoming',
        email="202018020317@qq.com",
        password="123456"
    )
    db.session.add(new_student)
    db.session.commit()
    return "Add student successfully!"


@app.route('/get_student')
def get_student():
    student = Student.query.filter_by(id=1).first()
    return student.chinese_name

@app.route('/add_deadline')
def add_deadline():
    new_deadline = Deadline(
        round_num=1,
        submit_time='2021-01-01 00:00:00',
        result_time='2021-01-02 00:00:00',
        note='第一轮选题'
    )
    new_deadline.add()
    return "Add deadline successfully!"


if __name__ == '__main__':
    create_tables()
    app.run()
