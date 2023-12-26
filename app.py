import os
import re
import secrets
from io import BytesIO

import pandas as pd

from flask import Flask, render_template, session, request, redirect, url_for, jsonify, Response, send_from_directory
from flask import send_file
from openpyxl import Workbook
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


'''Server start time'''
now = datetime.now()


@app.route('/')
def homepage():
    num_of_topics = Topic.get_num()
    num_of_supervisors = Supervisor.get_num()
    return render_template('home.html', num_of_topics=num_of_topics, num_of_supervisors=num_of_supervisors)


@app.route('/error')
def error():
    message = request.args.get('message')
    return render_template('error.html', message=message)


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
        error = request.args.get('error')
        deadlines = Deadline.get_all()
        return render_template('student.html', name=session['user_name'], selection=selection, supervisors=supervisors,
                               types=types, deadlines=deadlines, now=datetime.now(), error=error)
    else:
        return render_template('login.html')


@app.route('/supervisor')
def supervisor():
    if 'user_name' and 'user_type' in session:
        supervisor_id = Supervisor.get_id(user_name=session['user_name'])
        supervisor = Supervisor.get_by_id(id=supervisor_id)
        topics = Topic.get_by_supervisor_id_not_custom(supervisor_id=supervisor_id)
        not_custom_selections = Selection.get_supervisor_selection_not_custom(supervisor_id=supervisor_id)
        custom_selections = Selection.get_supervisor_selection_custom(supervisor_id=supervisor_id)

        total_quta = 0
        for topic in topics:
            total_quta += topic.quota

        return render_template('supervisor.html', topics=topics, supervisor=supervisor, total_quta=total_quta,
                               not_custom_selections=not_custom_selections, custom_selections=custom_selections)
    else:
        return render_template('login.html')


@app.route('/manager')
def manager():
    if 'user_name' and 'user_type' in session:
        supervisor_id = Supervisor.get_id(user_name=session['user_name'])
        supervisor = Supervisor.get_by_id(id=supervisor_id)
        pre = request.args.get('pre')
        students = Student.get_all()

        deadline_1 = Deadline.get_first()
        deadline_2 = Deadline.get_second()
        supervisors = Supervisor.get_all()
        custom_selections = Selection.get_all_custom_selections()
        notes = Note.get_all()
        topic_num = Topic.get_num()
        custom_topic_num = Topic.get_num_custom()
        num_success = Selection.get_num_of_status_3or4()
        num_waiting = Selection.get_num_of_status_0()
        num_process = Selection.get_num_of_status_1()
        num_verify = Selection.get_num_of_status_2()
        num_fail = Selection.get_num_of_status_5()
        total_quta = Topic.get_all_quota()
        static_topic_num = Selection.get_num_of_status_4()

        return render_template('manager.html', supervisor=supervisor, deadline_1=deadline_1, deadline_2=deadline_2,
                               notes=notes, students=students, supervisors=supervisors,
                               custom_selections=custom_selections, topic_num=topic_num,
                               custom_topic_num=custom_topic_num, num_success=num_success, num_waiting=num_waiting,
                               num_process=num_process, num_verify=num_verify, num_fail=num_fail, total_quta=total_quta,
                               static_topic_num=static_topic_num, pre=pre)
    else:
        return render_template('login.html')


@app.route('/submit')
def submit():
    student_id = Student.get_id(english_name=session['user_name'])
    selection = Selection.get_by_student_id(student_id=student_id)
    submit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if selection:
        if selection.if_custom:
            if selection.first_topic_id is None:
                return redirect(url_for('student', error='You have not selected any topic'))
            else:
                selection.update_status(status=2)
                selection.update_submit_time(submit_time=submit_time)
                return redirect(url_for('student'))
        else:
            if selection.first_topic_id is None or selection.second_topic_id is None or selection.third_topic_id is None:
                return redirect(url_for('student', error='You have full all three choices'))
            else:
                selection.update_status(status=1)
                selection.update_submit_time(submit_time=submit_time)
                return redirect(url_for('student'))
    else:
        return redirect(url_for('student', error='You have not selected any topic'))


@app.route('/process')
def process():
    selections = Selection.get_all_order_by_submit_time()
    success = 0
    fail = 0
    for selection in selections:
        for priority in ['first', 'second', 'third']:
            selection_successful = False
            if not selection.topic_is_full(priority):
                selection.update_status(status=4)
                selection.update_final_topic_id(topic_id=getattr(selection, f'{priority}_topic_id'))
                success += 1
                selection_successful = True
                break
        if not selection_successful:
            selection.update_status(status=5)
            fail += 1
    print("Success count: {}".format(success))
    print("Fail count: {}".format(fail))
    print("Total count: {}".format(len(selections)))
    return redirect(url_for('manager'))


@app.route('/refresh')
def refresh():
    selections = Selection.get_all_status_5()
    for selection in selections:
        selection.update_status(status=0)
        selection.update_first_topic_id(topic_id=None)
        selection.update_second_topic_id(topic_id=None)
        selection.update_third_topic_id(topic_id=None)

    return redirect(url_for('manager'))


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
        if topic.get_selected_num_final() > 0 or topic.get_selected_num() > 0:
            return jsonify(success=False, error='Can not delete this topic, students have selected this topic.')
        else:
            topic.delete()
            return jsonify(success=True)
    else:
        return jsonify(success=False, error='Topic does not exist')


@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    student = Student.get_by_id(id=student_id)
    selection = Selection.get_by_student_id(student_id=student_id)
    if student:
        if selection is None:
            student.delete()
            return jsonify(success=True)
        else:
            return jsonify(success=False, error='Can not delete this student, student has selected topics.')
    else:
        return jsonify(success=False, error='Student does not exist')


@app.route('/delete_supervisor/<int:supervisor_id>')
def delete_supervisor(supervisor_id):
    supervisor = Supervisor.get_by_id(id=supervisor_id)
    topics = Topic.get_by_supervisor_id(supervisor_id=supervisor_id)
    if supervisor:
        if len(topics) == 0:
            supervisor.delete()
            return jsonify(success=True)
        else:
            return jsonify(success=False, error='Can not delete this supervisor, supervisor has topics.')
    else:
        return jsonify(success=False, error='Supervisor does not exist')


@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    note = Note.get_by_id(id=note_id)
    if note:
        note.delete()
        return jsonify(success=True)
    else:
        return redirect(url_for('error', message='Note does not exist'))


@app.route('/new_topic')
def new_topic():
    types = Type.get_all()
    return render_template('new_topic.html', types=types)


@app.route('/new_note')
def new_note():
    return render_template('new_note.html')


@app.route('/new_student')
def new_student():
    return render_template('new_student.html')


@app.route('/new_supervisor')
def new_supervisor():
    return render_template('new_supervisor.html')


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
    topics = Topic.get_by_supervisor_id_not_custom(supervisor_id=supervisor_id)
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


@app.route('/add_student', methods=['POST'])
def add_student():
    chinese_name = request.form.get('chinese_name')
    english_name = request.form.get('english_name')
    class_number = request.form.get('class_number')
    email = request.form.get('email')
    password = request.form.get('password')
    user_name = request.form.get('username')

    new_student = Student(chinese_name=chinese_name, english_name=english_name, class_number=class_number,
                          email=email, password=password, user_name=user_name)
    new_student.add()
    return redirect(url_for('manager', pre='student'))


@app.route('/add_supervisor', methods=['POST'])
def add_supervisor():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    position = request.form.get('position')
    user_name = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    new_supervisor = Supervisor(first_name=first_name, last_name=last_name, position=position,
                                user_name=user_name, password=password, email=email, is_admin=False)
    new_supervisor.add()
    return redirect(url_for('manager', pre='supervisor'))


@app.route('/import_students', methods=['POST'])
def import_students():
    print('import_students')
    file = request.files['file']
    if file:
        df = pd.read_excel(file)
        for index, row in df.iterrows():
            new_student = Student(
                chinese_name=row['chinese_name'],
                english_name=row['english_name'],
                class_number=row['class_number'],
                email=row['email'],
                password=row['password'],
                user_name=row['user_name']
            )
            db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('manager', pre='student'))
    return redirect(url_for('error', message='No file uploaded'))


@app.route('/import_supervisors', methods=['POST'])
def import_supervisors():
    print('import_supervisors')
    file = request.files['file']
    if file:
        df = pd.read_excel(file)
        for index, row in df.iterrows():
            new_supervisor = Supervisor(
                first_name=row['first_name'],
                last_name=row['last_name'],
                position=row['position'],
                user_name=row['user_name'],
                password=row['password'],
                email=row['email'],
                is_admin=False
            )
            db.session.add(new_supervisor)
        db.session.commit()
        return redirect(url_for('manager', pre='supervisor'))
    return redirect(url_for('error', message='No file uploaded'))


@app.route('/get_template')
def get_template():
    directory = os.path.join(app.root_path, 'static', 'file')
    filename = 'students_example.xlsx'
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/get_template_supervisor')
def get_template_supervisor():
    directory = os.path.join(app.root_path, 'static', 'file')
    filename = 'supervisor_example.xlsx'
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/edit_topic/<int:topic_id>')
def edit_topic(topic_id):
    topic = Topic.get_by_id(id=topic_id)
    types = Type.get_all()
    return render_template('edit_topic.html', topic=topic, types=types)


@app.route('/edit_note/<int:note_id>')
def edit_note(note_id):
    note = Note.get_by_id(id=note_id)
    return render_template('edit_note.html', note=note)


@app.route('/edit_student/<int:student_id>')
def edit_student(student_id):
    student = Student.get_by_id(id=student_id)
    return render_template('edit_student.html', student=student)


@app.route('/edit_supervisor/<int:supervisor_id>')
def edit_supervisor(supervisor_id):
    supervisor = Supervisor.get_by_id(id=supervisor_id)
    return render_template('edit_supervisor.html', supervisor=supervisor)


@app.route('/check_custom_selection/<int:selection_id>')
def check_custom_selection(selection_id):
    selection = Selection.get_by_id(selection_id=selection_id)
    supervisors = Supervisor.get_all()
    types = Type.get_all()
    return render_template('check_custom_selection.html', selection=selection, supervisors=supervisors, types=types)


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
    topics = Topic.get_by_supervisor_id_not_custom(supervisor_id=supervisor_id)
    types = Type.get_all()
    selected_num = topic.get_selected_num_final()

    total_quta = 0
    for topic_in in topics:
        total_quta += topic_in.quota

    if total_quta + int(position) - topic.quota > supervisor.position:
        return render_template('edit_topic.html',
                               message='Can not save your modify, excess quota, you only have ' + str(
                                   supervisor.position) + ' positions.',
                               topic=topic, types=types)

    if selected_num is not None and selected_num > int(position):
        return render_template('edit_topic.html',
                               message='Can not save your modify, excess quota, ' + str(
                                   selected_num) + ' students have selected this topic.',
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


@app.route('/update_student/<int:student_id>', methods=['POST'])
def update_student(student_id):
    student = Student.get_by_id(id=student_id)
    chinese_name = request.form.get('chinese_name')
    english_name = request.form.get('english_name')
    class_number = request.form.get('class_number')
    email = request.form.get('email')
    password = request.form.get('password')
    user_name = request.form.get('username')

    student.update(chinese_name=chinese_name, english_name=english_name, class_number=class_number, email=email,
                   password=password, user_name=user_name)
    return redirect(url_for('manager', pre='student'))


@app.route('/update_supervisor/<int:supervisor_id>', methods=['POST'])
def update_supervisor(supervisor_id):
    supervisor = Supervisor.get_by_id(id=supervisor_id)
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    position = request.form.get('position')
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    email = request.form.get('email')

    topics = Topic.get_by_supervisor_id_not_custom(supervisor_id=supervisor_id)

    total_quta = 0
    for topic in topics:
        total_quta += topic.quota

    if total_quta > int(position):
        return render_template('edit_supervisor.html',
                               message='Can not save your modify, excess quota, supervisor already have ' + str(
                                   total_quta) + ' quta.',
                               supervisor=supervisor)

    supervisor.update(first_name=first_name, last_name=last_name, position=position,
                      user_name=user_name, password=password, email=email)
    return redirect(url_for('manager', pre='supervisor'))


@app.route('/update_custom_selection/<int:selection_id>', methods=['POST'])
def update_custom_selection(selection_id):
    selection = Selection.get_by_id(selection_id=selection_id)
    supervisor_id = request.form.get('supervisor')
    topic_name = request.form.get('name')
    description = request.form.get('description')
    type_id = request.form.get('type')
    status = request.form.get('status')

    if status == '3':
        selection.final_topic_id = selection.first_topic_id
    elif status == '2':
        selection.final_topic_id = None

    selection.update_status(status=status)
    selection.update_first_topic_supervisor_id(supervisor_id=supervisor_id)
    selection.update_first_topic_name(name=topic_name)
    selection.update_first_topic_description(description=description)
    selection.update_first_topic_type_id(type_id=type_id)
    return redirect(url_for('manager', pre='custom_selection'))


@app.route('/student_status/<int:student_id>')
def student_status(student_id):
    selection = Selection.get_by_student_id(student_id=student_id)
    student = Student.get_by_id(id=student_id)
    return render_template('student_status.html', selection=selection, student=student)


@app.route('/supervisor_status/<int:supervisor_id>')
def supervisor_status(supervisor_id):
    topics = Topic.get_by_supervisor_id(supervisor_id=supervisor_id)
    supervisor = Supervisor.get_by_id(id=supervisor_id)

    return render_template('supervisor_status.html', topics=topics, supervisor=supervisor)


@app.route('/topic_poster')
def topic_poster():
    supervisor_id = Supervisor.get_id(user_name=session['user_name'])
    topics = Topic.get_by_supervisor_id_not_custom(supervisor_id=supervisor_id)
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

    if not topic:
        return json.dumps({'success': False, 'error': 'Topic does not exist'})

    if topic.get_selected_num_final() == topic.quota:
        return json.dumps({'success': False, 'error': 'This topic is full'})

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


@app.route('/topic_search')
def topic_search():
    search_query = request.args.get('search_query')

    topics = Topic

    if search_query:
        topics = topics.get_by_name_or_id(search_query=search_query)

    if topics:
        return json.dumps({'topic_ids': [topic.id for topic in topics]})
    else:
        return json.dumps({'topic_ids': []})


@app.route('/topic_detail/<int:topic_id>')
def topic_detail(topic_id):
    topic = Topic.get_by_id(id=topic_id)
    return render_template('topic_detail.html', topic=topic)


@app.route('/topic_detail_custom/<int:topic_id>/')
def topic_detail_custom(topic_id):
    topic = Topic.get_by_id(id=topic_id)
    return render_template('topic_detail_custom.html', topic=topic)


@app.route('/export_student_list')
def export_student_list():
    supervisor_id = Supervisor.get_id(user_name=session['user_name'])
    not_custom_selections = Selection.get_supervisor_selection_not_custom(supervisor_id=supervisor_id)
    custom_selections = Selection.get_supervisor_selection_custom(supervisor_id=supervisor_id)
    wb = Workbook()
    ws = wb.active
    ws.title = 'Student List'

    columns = ['Topic name', 'Chinese Name', 'English Name', 'Class Number', 'Email']
    ws.append(columns)

    for selection in not_custom_selections:
        student = Student.get_by_id(selection.student_id)
        topic = Topic.get_by_id(selection.final_topic_id)
        row = [topic.name, student.chinese_name, student.english_name, student.class_number, student.email]
        ws.append(row)

    for selection in custom_selections:
        student = Student.get_by_id(selection.student_id)
        topic = Topic.get_by_id(selection.first_topic_id)
        row = [topic.name + '(Custom)', student.chinese_name, student.english_name, student.class_number, student.email]
        ws.append(row)

    virtual_workbook = BytesIO()
    wb.save(virtual_workbook)
    virtual_workbook.seek(0)

    return Response(
        virtual_workbook.getvalue(),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment;filename=student_list.xlsx'}
    )


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
