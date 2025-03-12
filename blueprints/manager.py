from flask import Blueprint, session, redirect, url_for, request, render_template, jsonify, send_from_directory, flash
from functools import wraps

from models.report import Report
from models.result import Result
from models.semester import Semester
from models.student import Student
from models.supervisor import Supervisor
from models.selection import Selection
from models.type import Type
from models.deadline import Deadline
from models.topic import Topic
from models.note import Note
from exts import db
from sqlalchemy import text
import json
import pandas as pd
import os
from blueprints.base import get_graduation_year

bp = Blueprint("manager", __name__, url_prefix="/manager")


def require_manager(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in session or session['user_type'] != 'manager':
            print("Not logged in - require_manager")
            return redirect(url_for('base.login'))
        return f(*args, **kwargs)

    return decorated_function


@bp.route('/')
@require_manager
def redirect_to_home():
    return redirect(url_for('manager.index'))


@bp.route('/home')
@require_manager
def index():
    supervisor_id = Supervisor.get_id_by_username(user_name=session['user_name'])
    supervisor = Supervisor.get_by_id(id=supervisor_id)
    pre = request.args.get('pre')
    students = Student.get_all()

    deadline_1 = Deadline.get_first()
    deadline_2 = Deadline.get_second()
    supervisors = Supervisor.get_all()
    custom_selections = Selection.get_all_custom_selections()
    notes = Note.get_all()
    types = Type.get_all()
    topic_num = Topic.get_num_not_custom()
    custom_topic_num = Topic.get_num_custom()
    topics = Topic.get_all()
    num_success = Selection.get_num_of_status_3or4()
    num_waiting = Selection.get_num_of_status_0()
    num_process = Selection.get_num_of_status_1()
    num_verify = Selection.get_num_of_status_2()
    num_fail = Selection.get_num_of_status_5()
    total_quta = Topic.get_all_quota()
    static_topic_num = Selection.get_num_of_status_4()

    semester = Semester.get_latest()
    all_reports = Report.get_all()

    return render_template('manager/index.html', supervisor=supervisor, deadline_1=deadline_1, deadline_2=deadline_2,
                           notes=notes, students=students, supervisors=supervisors,
                           custom_selections=custom_selections, topic_num=topic_num, types=types,
                           custom_topic_num=custom_topic_num, num_success=num_success, num_waiting=num_waiting,
                           num_process=num_process, num_verify=num_verify, num_fail=num_fail,
                           static_topic_num=static_topic_num, pre=pre, total_quta=total_quta, topics=topics,
                           supervisor_id=supervisor_id, semester=semester, all_reports=all_reports)


# Manager process all the selections
@bp.route('/process')
@require_manager
def process():
    selections = Selection.get_all_order_by_submit_time()
    success = 0
    fail = 0
    for selection in selections:
        for priority in ['first', 'second', 'third']:
            selection_successful = False
            if not selection.topic_is_full(priority):
                selection.update_status(status=4)  # 4:success(Supervisor's Topic)
                selection.update_final_topic_id(topic_id=getattr(selection, f'{priority}_topic_id'))
                success += 1
                selection_successful = True
                break
        if not selection_successful:
            selection.update_status(status=5)  # 5:fail
            fail += 1
    # print("Success count: {}".format(success))
    # print("Fail count: {}".format(fail))
    # print("Total count: {}".format(len(selections)))
    return redirect(url_for('manager.index'))


# Manager reset all the failed selections
@bp.route('/refresh')
@require_manager
def refresh():
    selections = Selection.get_all_status_5()
    for selection in selections:
        selection.update_status(status=0)
        selection.update_first_topic_id(topic_id=None)
        selection.update_second_topic_id(topic_id=None)
        selection.update_third_topic_id(topic_id=None)

    return redirect(url_for('manager.index'))


# Manager create new type
@bp.route('/new_type')
@require_manager
def new_type():
    return render_template('manager/type/new_type.html')


@bp.route('/new/<string:_type>')
@require_manager
def go_to_new_page(_type):
    if _type == 'student':
        return render_template('manager/student/new_student.html')
    elif _type == 'supervisor':
        return render_template('manager/supervisor/new_supervisor.html')
    elif _type == 'supTopic':
        types = Type.get_all()
        supervisors = Supervisor.get_all()
        return render_template('supervisor/topic/new_topic.html', types=types, supervisors=supervisors)
    else:
        return ''


# Manager edit note
@bp.route('/new_note/<int:note_id>')
@require_manager
def edit_note(note_id):
    note = Note.get_by_id(id=note_id)
    return render_template('manager/note/edit_note.html', note=note)


# Manager edit type
@bp.route('/edit_type/<int:type_id>')
@require_manager
def edit_type(type_id):
    type_item = Type.get_by_id(id=type_id)
    topics = Topic.get_by_type_id(type_id=type_id)
    return render_template('manager/type/edit_type.html', type=type_item, topics=topics)


# Manager update note
@bp.route('/update_note/<int:note_id>', methods=['POST'])
@require_manager
def update_note(note_id):
    note = Note.get_by_id(id=note_id)
    title = request.form.get('title')
    content = request.form.get('content')
    note.update(title=title, content=content)
    return redirect(url_for('manager.index'))


# Manager update type
@bp.route('/update_type/<int:type_id>', methods=['POST'])
@require_manager
def update_type(type_id):
    type_item = Type.get_by_id(id=type_id)
    name = request.form.get('name')
    type_item.update(name=name)
    return redirect(url_for('manager.index'))


# Manager update student
@bp.route('/update_student/<int:student_id>', methods=['POST'])
@require_manager
def update_student(student_id):
    student = Student.get_by_id(id=student_id)
    chinese_name = request.form.get('chinese_name')
    english_name = request.form.get('english_name')
    class_number = request.form.get('class_number')
    email = request.form.get('email')
    user_name = request.form.get('username')

    student.update(chinese_name=chinese_name, english_name=english_name, class_number=class_number, email=email,
                   user_name=user_name)
    return redirect(url_for('manager.index', pre='student'))


# Manager update supervisor
@bp.route('/update_supervisor/<int:supervisor_id>', methods=['POST'])
@require_manager
def update_supervisor(supervisor_id):
    supervisor = Supervisor.get_by_id(id=supervisor_id)
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    position = request.form.get('position')
    user_name = request.form.get('username')
    email = request.form.get('email')
    expertise = request.form.get('expertise')

    topics = Topic.get_by_supervisor_id_not_custom(supervisor_id=supervisor_id)

    total_quota = 0
    for topic in topics:
        total_quota += topic.quota

    if total_quota > int(position):
        return render_template('manager/supervisor/edit_supervisor.html',
                               message='Can not save your modify, excess quota, supervisor already have ' + str(
                                   total_quota) + ' quta.',
                               supervisor=supervisor)

    supervisor.update(first_name=first_name, last_name=last_name, position=position,
                      user_name=user_name, email=email, expertise=expertise)
    return redirect(url_for('manager.index', pre='supervisor'))


@bp.route('/reset_password', methods=['POST'])
@require_manager
def reset_password():
    user_id = request.form['user_id']
    user_type = request.form['user_type']
    new_password = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'

    if user_type == 'student':
        student = Student.query.filter_by(id=user_id).first()
        student.password = new_password
        db.session.commit()
        return jsonify(status='success')
    elif user_type == 'supervisor':
        supervisor = Supervisor.query.filter_by(id=user_id).first()
        supervisor.password = new_password
        db.session.commit()
        return jsonify(status='success')


# Manager create new note
@bp.route('/new_note')
@require_manager
def new_note():
    return render_template('manager/note/new_note.html')


@bp.route('/get_temp/<string:_type>')
@require_manager
def get_temp(_type):
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    root_directory = os.path.dirname(current_directory)
    directory_path = os.path.join(root_directory, 'static', 'file')
    filename = _type + '_example.xlsx'
    return send_from_directory(directory_path, filename, as_attachment=True)


def get_type_id_by_required_skills(required_skills):
    required_skills_lower = required_skills.lower()

    if 'machine' in required_skills_lower or 'deep' in required_skills_lower or 'ai' in required_skills_lower or 'python' in required_skills_lower:
        return Type.get_by_title('Machine Learning').id
    else:
        return Type.get_by_title('Software Development').id


@bp.route('/import/<string:_type>', methods=['POST'])
@require_manager
def import_file(_type):
    file = request.files['file']
    if file:
        df = pd.read_excel(file)
        df.columns = df.columns.str.strip()
        if _type == 'student':
            for _index, row in df.iterrows():
                cleaned_row = {key: value.strip() if isinstance(value, str) else value for key, value in row.items()}
                _new_student = Student(
                    chinese_name=cleaned_row['chinese_name'],
                    english_name=cleaned_row['english_name'],
                    class_number=cleaned_row['class_number'],
                    email=cleaned_row['email'],
                    password='8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
                    user_name=cleaned_row['user_name']
                )
                db.session.add(_new_student)
            db.session.commit()
        elif _type == 'supervisor':
            for _index, row in df.iterrows():
                cleaned_row = {key: value.strip() if isinstance(value, str) else value for key, value in row.items()}
                _new_supervisor = Supervisor(
                    first_name=cleaned_row['first_name'],
                    last_name=cleaned_row['last_name'],
                    position=cleaned_row['position'],
                    user_name=cleaned_row['user_name'],
                    password='8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
                    email=cleaned_row['email'],
                    is_admin=False
                )
                db.session.add(_new_supervisor)
            db.session.commit()
        elif _type == 'supTopic':
            for _index, row in df.iterrows():
                cleaned_row = {key: value.strip() if isinstance(value, str) else value for key, value in row.items()}
                supervisor_name = cleaned_row['Staff member']
                supervisor = Supervisor.get_by_name(supervisor_name)
                expertise = cleaned_row['Staff Expertise (Projects/Research Interests)']
                supervisor.update(expertise=expertise)
                _new_topic = Topic(
                    name=cleaned_row['Proposed Titles'],
                    supervisor_id=supervisor.id,
                    quota=cleaned_row['Number of Students to Supervise'],
                    is_custom=False,
                    type_id=get_type_id_by_required_skills(cleaned_row['Required skills']),
                    description=cleaned_row['Topic details'],
                    required_skills=cleaned_row['Required skills'],
                    reference=cleaned_row['References']
                )
                db.session.add(_new_topic)
            db.session.commit()
        return redirect(url_for('manager.index'))
    else:
        return redirect(url_for('base.error', message='No file uploaded'))


# Manager add new note
@bp.route('/add_note', methods=['POST'])
@require_manager
def add_note():
    title = request.form.get('title')
    content = request.form.get('content')

    _new_note = Note(title=title, content=content)
    _new_note.add()
    return redirect(url_for('manager.index'))


@bp.route('/detail/<string:_type>/<int:id>')
@require_manager
def detail(_type, id):
    if _type == 'supervisor':
        topics = Topic.get_by_supervisor_id(supervisor_id=id)
        supervisor = Supervisor.get_by_id(id=id)
        return render_template('manager/supervisor/supervisor_status.html', topics=topics, supervisor=supervisor)
    elif _type == 'student':
        selection = Selection.get_by_student_id(student_id=id)
        student = Student.get_by_id(id=id)
        return render_template('manager/student/student_status.html', selection=selection, student=student)
    elif _type == 'topic':
        selection = Selection.get_by_id(id)
        supervisors = Supervisor.get_all()
        types = Type.get_all()
        return render_template('manager/selection/check_custom_selection.html', selection=selection,
                               supervisors=supervisors, types=types)
    else:  # elif _type == 'supTopic':
        topic = Topic.get_by_id(id)
        return render_template('base/topic_detail.html', topic=topic)


# Manager update deadline
@bp.route('/update_deadline', methods=['POST'])
@require_manager
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
    elif round_num == 2:
        deadline = Deadline.get_second()

    if reset:
        deadline.reset()
        return json.dumps({'success': True, 'reset': True})

    deadline.update(submit_time=submit_time, result_time=result_time, note=note)
    return json.dumps({'success': True})


@bp.route('/delete/<string:_type>/<int:_id>')
@require_manager
def delete(_type, _id):
    if _type == 'student':
        student = Student.get_by_id(id=_id)
        selection = Selection.get_by_student_id(student_id=_id)
        if student:
            if selection is None:
                student.delete()
                return jsonify(success=True, message='Delete Successfully')
            else:
                return jsonify(success=False, message='Can not delete this student, student has selected topics.')
        else:
            return jsonify(success=False, message='Student does not exist')
    elif _type == 'supervisor':
        supervisor = Supervisor.get_by_id(id=_id)
        topics = Topic.get_by_supervisor_id(supervisor_id=_id)
        if supervisor:
            if len(topics) == 0:
                supervisor.delete()
                return jsonify(success=True, message='Delete Successfully')
            else:
                return jsonify(success=False, message='Can not delete this supervisor, supervisor has topics.')
        else:
            return jsonify(success=False, message='Supervisor does not exist')
    elif _type == 'supTopic':
        topic = Topic.get_by_id(id=_id)
        if topic:
            if topic.get_selected_num_final() > 0 or topic.get_selected_num() > 0:
                return jsonify(success=False, message='Can not delete this topic, students have selected this topic.')
            else:
                topic.delete()
                return jsonify(success=True, message='Delete Successfully')
        else:
            return jsonify(success=False, message='Topic does not exist')
    elif _type == 'type':
        type_item = Type.get_by_id(id=_id)
        topics = Topic.get_by_type_id(type_id=_id)
        if type_item:
            if len(topics) == 0:
                type_item.delete()
                return jsonify(success=True, message='Delete Successfully')
            else:
                return jsonify(success=False, message='Can not delete this type, type has topics.')
        else:
            return jsonify(success=False, message='Type does not exist')
    elif _type == 'note':
        note = Note.get_by_id(id=_id)
        if note:
            note.delete()
            return jsonify(success=True, message='Delete Successfully')
        else:
            return jsonify(success=False, message='Note does not exist')
    else:
        return jsonify(success=False, message='Invalid Type')


# Manager reset the selections, students and reports
@bp.route('/resetting')
@require_manager
def resetting():
    db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))
    tables = ['selections', 'reports', 'students']
    for table in tables:
        db.session.execute(text(f'TRUNCATE TABLE {table};'))
    db.session.commit()
    return jsonify(success=True)


@bp.route('/fail_students')
@require_manager
def fail_students():
    selections = Selection.get_all_status_5()
    students = []
    for selection in selections:
        student = Student.get_by_id(id=selection.student_id)
        if student is not None:
            students.append(student)
    return jsonify(students=[student.to_json() for student in students])


# Manager add new type
@bp.route('/add_type', methods=['POST'])
@require_manager
def add_type():
    name = request.form.get('name')
    _new_type = Type(name=name)
    _new_type.add()
    return redirect(url_for('manager.index'))


# Manager add new student
@bp.route('/add_student', methods=['POST'])
@require_manager
def add_student():
    chinese_name = request.form.get('chinese_name')
    english_name = request.form.get('english_name')
    class_number = request.form.get('class_number')
    email = request.form.get('email')
    user_name = request.form.get('username')
    password = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'  # 123456
    _new_student = Student(chinese_name=chinese_name, english_name=english_name, class_number=class_number,
                           email=email, password=password, user_name=user_name)
    _new_student.add()
    return redirect(url_for('manager.index', pre='student'))


# Manager add new supervisor
@bp.route('/add_supervisor', methods=['POST'])
@require_manager
def add_supervisor():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    position = request.form.get('position')
    user_name = request.form.get('username')
    password = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    email = request.form.get('email')
    expertise = request.form.get('expertise')

    _new_supervisor = Supervisor(first_name=first_name, last_name=last_name, position=position,
                                 user_name=user_name, password=password, email=email, is_admin=False,
                                 expertise=expertise)
    _new_supervisor.add()
    return redirect(url_for('manager.index', pre='supervisor'))


# Manager update custom selection
@bp.route('/update_custom_selection/<int:selection_id>', methods=['POST'])
@require_manager
def update_custom_selection(selection_id):
    selection = Selection.get_by_id(selection_id)
    supervisor_id = request.form.get('supervisor')
    topic_name = request.form.get('name')
    description = request.form.get('description')
    type_id = request.form.get('type')
    status = request.form.get('status')

    if status == '3':  # 3 - success(custom Topic)
        selection.final_topic_id = selection.first_topic_id
    elif status == '2':  # 2 - waiting for verify(custom Topic)
        selection.final_topic_id = None

    selection.update_status(status=status)
    selection.update_first_topic_supervisor_id(supervisor_id=supervisor_id)
    selection.update_first_topic_name(name=topic_name)
    selection.update_first_topic_description(description=description)
    selection.update_first_topic_type_id(type_id=type_id)
    return redirect(url_for('manager.index', pre='custom_selection'))


# @bp.route('/topic_detail/<int:topic_id>', methods=['GET'])
# @require_manager
# def topic_detail(topic_id):
#     topic = Topic.get_by_id(topic_id)
#     types = Type.get_all()
#     supervisors = Supervisor.get_all()
#     return render_template('manager/topic/topic_detail.html', topic=topic, types=types, supervisors=supervisors)


@bp.route('/edit/<string:_type>/<int:id>', methods=['GET'])
@require_manager
def edit(_type, id):
    if _type == 'student':
        student = Student.get_by_id(id=id)
        return render_template('manager/student/edit_student.html', student=student)
    elif _type == 'supervisor':
        supervisor = Supervisor.get_by_id(id=id)
        return render_template('manager/supervisor/edit_supervisor.html', supervisor=supervisor)
    elif _type == 'supTopic':
        topic = Topic.get_by_id(id=id)
        types = Type.get_all()
        return render_template('supervisor/topic/edit_topic.html', topic=topic, types=types)
    else:
        pass


@bp.route('/semester/<graduation_year>/<num>/<start_time>')
@require_manager
def update_semester_start_date(graduation_year, num, start_time):
    is_reset = request.args.get('isReset', 'false') == 'true'

    if is_reset:
        existing_semester = Semester.query.filter_by(graduation_year=graduation_year).first()
        if existing_semester:
            if num == '1':
                existing_semester.update(first_semester_start_date=None)
            else:
                existing_semester.update(second_semester_start_date=None)
            return Result.success(f"Semester {num} start date reset successfully for year {graduation_year}.")
        else:
            return Result.error(f"No semester found for year {graduation_year}.")

    existing_semester = Semester.query.filter_by(graduation_year=graduation_year).first()
    if existing_semester is None:
        if num == '1':
            semester = Semester(graduation_year, start_time, None)
        else:
            semester = Semester(graduation_year, None, start_time)
        semester.add()
    else:
        if num == '1':
            existing_semester.update(first_semester_start_date=start_time)
        else:
            existing_semester.update(second_semester_start_date=start_time)

    return Result.success(f"Semester {num} start date updated successfully for year {graduation_year}.")


@bp.route('/to-supervisor')
@require_manager
def switch_to_supervisor_page():
    return redirect(url_for('supervisor.index'))


@bp.route('/report')
@require_manager
def review_weekly_report():
    report_id = request.args.get('report_id')
    report = Report.get_by_id(report_id)
    supervisor_name = report.student.get_supervisor_name()
    graduation_year = get_graduation_year()
    return render_template('report/report_detail.html', report=report, supervisor_name=supervisor_name, graduation_year=graduation_year)
