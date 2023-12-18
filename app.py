import re
import secrets
from flask import Flask, render_template, session, request, redirect, url_for, jsonify, Response
from models.db_instance import db
from datetime import datetime
import json

from models.pdf_generator import generate_topic_poster
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
            return redirect(url_for('student'))
        elif session['user_type'] == 'supervisor':
            return redirect(url_for('supervisor'))
        elif session['user_type'] == 'manager':
            return redirect(url_for('manager'))
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
                return redirect(url_for('student'))
            else:
                return render_template('login.html', message='Wrong password')

        elif supervisor:
            if supervisor.password == password:
                if supervisor.if_admin():
                    session['user_name'] = supervisor.user_name
                    session['user_type'] = 'manager'
                    return redirect(url_for('manager'))
                else:
                    session['user_name'] = supervisor.user_name
                    session['user_type'] = 'supervisor'
                    return redirect(url_for('supervisor'))
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


@app.route('/student')
def student():
    if 'user_name' and 'user_type' in session:
        student_id = Student.get_id(english_name=session['user_name'])
        selection = Selection.get_by_student_id(student_id=student_id)
        supervisors = Supervisor.get_all()
        types = Type.get_all()
        return render_template('student.html', name=session['user_name'], selection=selection, supervisors=supervisors,
                               types=types)
    else:
        return render_template('login.html')


@app.route('/supervisor')
def supervisor():
    if 'user_name' and 'user_type' in session:
        supervisor_id = Supervisor.get_id(user_name=session['user_name'])
        supervisor = Supervisor.get_by_id(id=supervisor_id)
        topics = Topic.get_by_supervisor_id(supervisor_id=supervisor_id)

        total_quta = 0
        for topic in topics:
            total_quta += topic.quota

        return render_template('supervisor.html', topics=topics, supervisor=supervisor, total_quta=total_quta)
    else:
        return render_template('login.html')


@app.route('/manager')
def manager():
    if 'user_name' and 'user_type' in session:
        supervisor_id = Supervisor.get_id(user_name=session['user_name'])
        supervisor = Supervisor.get_by_id(id=supervisor_id)

        deadline_1 = Deadline.get_first()
        deadline_2 = Deadline.get_second()

        students = Student.get_all()
        supervisors = Supervisor.get_all()

        notes = Note.get_all()
        return render_template('manager.html', supervisor=supervisor, deadline_1=deadline_1, deadline_2=deadline_2,
                               notes=notes, students=students, supervisors=supervisors)
    else:
        return render_template('login.html')


@app.route('/update_deadline', methods=['POST'])
def update_deadline():
    round_num = request.form.get('round_num')
    round_num = int(round_num)
    submit_time = request.form.get('submit_time')
    result_time = request.form.get('result_time')
    note = request.form.get('note')
    reset = request.form.get('reset') == 'true'
    deadline = None

    if round_num == 1:
        deadline = Deadline.get_first()
        print(deadline)
    elif round_num == 2:
        deadline = Deadline.get_second()

    if reset:
        deadline.reset()
        return json.dumps({'success': True, 'reset': True})

    deadline.update(submit_time=submit_time, result_time=result_time, note=note)
    return json.dumps({'success': True})


@app.route('/delete_topic/<int:topic_id>')
def delete_topic(topic_id):
    topic = Topic.get_by_id(id=topic_id)
    if topic:
        topic.delete()
        return jsonify(success=True)
    else:
        return jsonify(success=False), 404


@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    note = Note.get_by_id(id=note_id)
    if note:
        note.delete()
        return jsonify(success=True)
    else:
        return jsonify(success=False), 404


@app.route('/new_topic')
def new_topic():
    types = Type.get_all()
    return render_template('new_topic.html', types=types)


@app.route('/new_note')
def new_note():
    return render_template('new_note.html')


@app.route('/add_topic', methods=['POST'])
def add_topic():
    supervisor_id = Supervisor.get_id(user_name=session['user_name'])
    topic_name = request.form.get('topic_name')
    type_id = request.form.get('type')
    position = request.form.get('position')
    description = request.form.get('description')
    required_skills = request.form.get('required_skills')
    reference = request.form.get('reference')

    supervisor = Supervisor.get_by_id(id=supervisor_id)
    topics = Topic.get_by_supervisor_id(supervisor_id=supervisor_id)
    types = Type.get_all()

    total_quta = 0
    for topic_in in topics:
        total_quta += topic_in.quota

    if total_quta + int(position) > supervisor.position:
        return render_template('new_topic.html',
                               message='Excess quota, you only have ' + str(supervisor.position) + ' positions.',
                               types=types, topic_name=topic_name, type_id=type_id, position=position,
                               description=description,
                               required_skills=required_skills, reference=reference)

    new_topic = Topic(quota=position, is_custom=False, required_skills=required_skills, reference=reference,
                      name=topic_name,
                      supervisor_id=supervisor_id,
                      description=description, type_id=type_id)
    new_topic.add()
    return redirect(url_for('supervisor'))


@app.route('/add_note', methods=['POST'])
def add_note():
    title = request.form.get('title')
    content = request.form.get('content')

    new_note = Note(title=title, content=content)
    new_note.add()
    return redirect(url_for('manager'))


@app.route('/edit_topic/<int:topic_id>')
def edit_topic(topic_id):
    topic = Topic.get_by_id(id=topic_id)
    types = Type.get_all()
    return render_template('edit_topic.html', topic=topic, types=types)


@app.route('/edit_note/<int:note_id>')
def edit_note(note_id):
    note = Note.get_by_id(id=note_id)
    return render_template('edit_note.html', note=note)


@app.route('/update_topic/<int:topic_id>', methods=['POST'])
def update_topic(topic_id):
    topic = Topic.get_by_id(id=topic_id)
    print(topic_id)
    topic_name = request.form.get('topic_name')
    type_id = request.form.get('type')
    position = request.form.get('position')
    description = request.form.get('description')
    required_skills = request.form.get('required_skills')
    reference = request.form.get('reference')

    supervisor_id = Supervisor.get_id(user_name=session['user_name'])
    supervisor = Supervisor.get_by_id(id=supervisor_id)
    topics = Topic.get_by_supervisor_id(supervisor_id=supervisor_id)
    types = Type.get_all()

    total_quta = 0
    for topic_in in topics:
        total_quta += topic_in.quota

    if total_quta + int(position) - topic.quota > supervisor.position:
        return render_template('edit_topic.html',
                               message='Can not save your modify, excess quota, you only have ' + str(
                                   supervisor.position) + ' positions.',
                               topic=topic, types=types)

    topic.update(name=topic_name, supervisor_id=topic.supervisor_id, quota=position, is_custom=False, type_id=type_id,
                 description=description, required_skills=required_skills, reference=reference)
    print('find')
    return redirect(url_for('supervisor'))


@app.route('/update_note/<int:note_id>', methods=['POST'])
def update_note(note_id):
    note = Note.get_by_id(id=note_id)
    title = request.form.get('title')
    content = request.form.get('content')

    note.update(title=title, content=content)
    return redirect(url_for('manager'))


@app.route('/topic_poster')
def topic_poster():
    supervisor_id = Supervisor.get_id(user_name=session['user_name'])
    topics = Topic.get_by_supervisor_id(supervisor_id=supervisor_id)
    supervisor = Supervisor.get_by_id(id=supervisor_id)

    pdf_buffer = generate_topic_poster(supervisor, topics)
    pdf_buffer.seek(0)

    return Response(pdf_buffer, headers={
        'Content-Disposition': 'attachment;filename=topic_poster.pdf',
        'Content-Type': 'application/pdf'
    })


@app.route('/update_selection', methods=['POST'])
def update_selection():
    student_id = Student.get_id(english_name=session['user_name'])
    topic_id = request.form.get('topic_id')
    choice_number = int(request.form.get('choice_number'))
    reset = request.form.get('reset') == 'true'

    selection = Selection.get_by_student_id(student_id=student_id)
    if not selection:
        selection = Selection(student_id=student_id)
        selection.add()

    if reset:
        if choice_number == 1:
            selection.first_topic_id = None
        elif choice_number == 2:
            selection.second_topic_id = None
        elif choice_number == 3:
            selection.third_topic_id = None

        db.session.commit()
        return json.dumps({'success': True, 'reset': True})

    match = re.search(r'\d+', topic_id)
    formatted_topic_id = int(match.group())

    if formatted_topic_id in [selection.first_topic_id, selection.second_topic_id, selection.third_topic_id]:
        return json.dumps({'success': False, 'error': 'You have already selected this topic'})

    topic = Topic.get_by_id(id=formatted_topic_id)

    if topic:
        if match:
            if choice_number == 1:
                selection.first_topic_id = formatted_topic_id
            elif choice_number == 2:
                selection.second_topic_id = formatted_topic_id
            elif choice_number == 3:
                selection.third_topic_id = formatted_topic_id

        db.session.commit()
        return json.dumps({'success': True, 'topic_name': topic.name})
    else:
        return json.dumps({'success': False, 'error': 'Topic does not exist'})


@app.route('/update_custom_topic', methods=['POST'])
def update_custom_topic():
    student_id = Student.get_id(english_name=session['user_name'])
    topic_name = request.form.get('topic_name')
    supervisor_id = request.form.get('supervisor_id')
    description = request.form.get('description')
    type_id = request.form.get('type_id')
    reset = request.form.get('reset') == 'true'

    selection = Selection.get_by_student_id(student_id=student_id)
    if not selection:
        selection = Selection(student_id=student_id)
        selection.add()

    if reset:
        _id = selection.first_topic_id
        selection.first_topic_id = None
        Topic.get_by_id(id=_id).delete()
        db.session.commit()
        return json.dumps({'success': True, 'reset': True})

    new_topic = Topic(quota=1, is_custom=True, required_skills='Null', reference='Null', name=topic_name,
                      supervisor_id=supervisor_id,
                      description=description, type_id=type_id)
    new_topic_id = new_topic.add()

    selection.first_topic_id = new_topic_id
    selection.second_topic_id = None
    selection.third_topic_id = None

    db.session.commit()
    return json.dumps({'success': True, 'topic_name': topic_name})


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
