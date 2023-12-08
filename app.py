import secrets
from flask import Flask, render_template, session, request, redirect, url_for
from models.db_instance import db
from datetime import datetime
import json
from models.type import Type
from models.note import Note
from models.supervisor import Supervisor
from models.topic import Topic
from models.selection import Selection
from models.deadline import Deadline
from models.student import Student

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

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


'''Set up datetime'''
now = datetime.now()


@app.route('/')
def homepage():
    num_of_topics = Topic.get_num()
    num_of_supervisors = Supervisor.get_num()
    return render_template('home.html', num_of_topics=num_of_topics, num_of_supervisors=num_of_supervisors)


# Click 'My Pickr' button
@app.route('/my_pickr')
def my_pickr():
    if 'user_name' and 'user_type' in session:
        if session['user_type'] == 'student':
            return render_template('student.html', name=session['user_name'])
    else:
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')

        student = Student.query.filter_by(user_name=user_name).first()
        supervisor = Supervisor.query.filter_by(user_name=user_name).first()

        if student:
            if student.password == password:
                session['user_name'] = student.english_name
                session['user_type'] = 'student'
                return render_template('student.html', name=student.english_name)
            else:
                return render_template('login.html', message='Wrong password')

        elif supervisor:
            if supervisor.password == password:
                if supervisor.if_admin:
                    session['user_name'] = supervisor.user_name
                    session['user_type'] = 'admin'
                    return render_template('admin.html')
                else:
                    session['user_name'] = supervisor.user_name
                    session['user_type'] = 'supervisor'
                    return render_template('supervisor.html')
            else:
                return render_template('login.html', message='Wrong password')

        else:
            return render_template('login.html', message='User does not exist')

    else:
        return render_template('login.html', message='Please login')


@app.route('/logout')
def logout():
    session.pop('user_name', None)
    session.pop('user_type', None)
    return redirect(url_for('homepage'))


@app.route('/tutorial')
def tutorial():
    deadlines = Deadline.get_all()
    num = Deadline.get_num()
    notes = Note.get_all()
    return render_template('tutorial.html', deadlines=deadlines, notes=notes, num=num, year=now.year)


@app.route('/topic_list')
def topic_list():
    topics = Topic.get_all()
    types = Type.get_all()
    supervisors = Supervisor.get_all()
    return render_template('topic_list.html', topics=topics, types=types, supervisors=supervisors)


@app.route('/topic_filter')
def topic_filter():
    type_id = request.args.get('type_id')
    supervisor_id = request.args.get('supervisor_id')
    search_query = request.args.get('search_query')

    topics = Topic

    if search_query:
        topics = topics.get_by_name_or_id(search_query=search_query)
    elif supervisor_id:
        topics = topics.get_by_supervisor_id(supervisor_id=supervisor_id)
    elif type_id:
        topics = topics.get_by_type_id(type_id=type_id)

    if topics:
        return json.dumps({'topic_ids': [topic.id for topic in topics]})
    else:
        return json.dumps({'topic_ids': []})


@app.route('/topic_detail/<int:topic_id>')
def topic_detail(topic_id):
    topic = Topic.get_by_id(id=topic_id)
    return render_template('topic_detail.html', topic=topic)


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
    app.run(debug=True)
