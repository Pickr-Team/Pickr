# base and basic functions
from flask import Blueprint, render_template, session, request, url_for, redirect, jsonify, flash

from models.result import Result
from models.supervisor import Supervisor
from models.student import Student
from models.topic import Topic
from models.deadline import Deadline
from models.note import Note
from models.type import Type
from datetime import datetime
from functools import wraps
import json

bp = Blueprint("base", __name__)


@bp.route("/")
def home():
    num_of_topics = Topic.get_num_not_custom()
    num_of_supervisors = Supervisor.get_num()
    return render_template('base/home.html', num_of_topics=num_of_topics, num_of_supervisors=num_of_supervisors)


@bp.route('/tutorial')
def tutorial():
    deadlines = Deadline.get_all()
    num = Deadline.get_num()
    notes = Note.get_all()
    # Server start time
    now = datetime.now()
    return render_template('base/tutorial.html', deadlines=deadlines, notes=notes, num=num, year=now.year)


@bp.route('/my_pickr')
def my_pickr():
    if 'user_name' and 'user_type' in session:
        if session['user_type'] == 'student':
            return redirect(url_for('student.index'))
        elif session['user_type'] == 'supervisor':
            return redirect(url_for('supervisor.index'))
        elif session['user_type'] == 'manager':
            return redirect(url_for('manager.index'))
    else:
        return render_template('base/login.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password_hash = request.form['password_hash']
        student = Student.query.filter_by(user_name=user_name).first()
        supervisor = Supervisor.query.filter_by(user_name=user_name).first()
        if student and student.password == password_hash:
            session['user_name'] = student.english_name
            session['user_id'] = student.id
            session['user_type'] = 'student'
            return jsonify(status='success', redirect=url_for('student.index'), user_type=session['user_type'])
        elif supervisor and supervisor.password == password_hash:
            session['user_name'] = supervisor.user_name
            session['user_id'] = supervisor.id
            session['user_type'] = 'supervisor' if not supervisor.if_admin() else 'manager'
            redirect_url = url_for('manager.index') if supervisor.if_admin() else url_for('supervisor.index')
            return jsonify(status='success', redirect=redirect_url, user_type=session['user_type'])
        else:
            return jsonify(status='fail', message='Invalid username or password')
    else:
        return render_template('base/login.html')


def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in session:
            print("Not logged in")
            return redirect(url_for('base.login'))
        return f(*args, **kwargs)

    return decorated_function


@bp.route('/logout')
@require_login
def logout():
    session.pop('user_name', None)
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('base.login'))


@bp.route('/change_password', methods=['GET', 'POST'])
@require_login
def change_password():
    if request.method == 'POST':
        new_password_hash = request.form['new_password_hash']
        old_password_hash = request.form['old_password_hash']
        user_id = session['user_id']
        user_type = session['user_type']

        user = None
        if user_type == 'student':
            user = Student.get_by_id(user_id)
        else:
            user = Supervisor.get_by_id(user_id)

        if user and user.password == old_password_hash:
            user.update_pwd(new_password_hash)
            session.pop('user_name', None)
            session.pop('user_id', None)
            session.pop('user_type', None)
            flash('Change successfully! Please login again!', category='success')
            return jsonify(status='success', redirect=url_for('base.login'))
        else:
            return jsonify(status='fail', message='The old password is incorrect, change failed')
    else:
        return render_template('base/change_password.html')


@bp.route('/error')
def error():
    message = request.args.get('message')
    return render_template('base/error.html', message=message)


@bp.route('/list')
def topic_list():
    topics = Topic.get_all()
    types = Type.get_all()
    supervisors = Supervisor.get_all()
    return render_template('base/topic_list.html', topics=topics, types=types, supervisors=supervisors)


@bp.route('/search')
def topic_search():
    search_query = request.args.get('search_query')
    topics = Topic
    if search_query:
        topics = topics.get_by_name_or_id(search_query=search_query)
    if topics:
        return json.dumps({'topic_ids': [topic.id for topic in topics]})
    else:
        return json.dumps({'topic_ids': []})


@bp.route('/topic_detail/<int:topic_id>')
def topic_detail(topic_id):
    topic = Topic.get_by_id(id=topic_id)
    if topic:
        return render_template('base/topic_detail.html', topic=topic)
    else:
        return render_template('base/error.html', message='The topic is not existed'), 404


@bp.route('/topic_detail_custom/<int:topic_id>/')
def topic_detail_custom(topic_id):
    topic = Topic.get_by_id(id=topic_id)
    if topic:
        return render_template('base/topic_detail_custom.html', topic=topic)
    else:
        return render_template('base/error.html', message='The topic is not existed'), 404


@bp.route('/delete/<_type>/<_id>')
def delete_middle_ware(_type, _id):
    user_type = session['user_type']
    target_url = f'/{user_type}/delete/{_type}/{_id}'
    return redirect(target_url)