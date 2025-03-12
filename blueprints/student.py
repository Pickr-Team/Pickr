from flask import Blueprint, session, redirect, url_for, request, render_template, jsonify
from functools import wraps

from blueprints.base import get_graduation_year
from models.report import Report
from models.result import Result
from models.semester import Semester
from models.student import Student
from models.supervisor import Supervisor
from models.selection import Selection
from models.type import Type
from models.deadline import Deadline
from models.topic import Topic
from datetime import datetime
from exts import db
import re
import json

bp = Blueprint("student", __name__, url_prefix="/student")


def require_student(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in session or session['user_type'] != 'student':
            return redirect(url_for('base.login'))
        return f(*args, **kwargs)

    return decorated_function


@bp.route('/')
@require_student
def redirect_to_home():
    return redirect(url_for('student.index'))


@bp.route('/home')
@require_student
def index():
    student_id = Student.get_id_by_english_name(english_name=session['user_name'])
    selection = Selection.get_by_student_id(student_id=student_id)
    supervisors = Supervisor.get_all()
    types = Type.get_all()
    error = request.args.get('error')
    deadlines = Deadline.get_all()

    semester = Semester.get_latest()
    graduation_year = get_graduation_year()
    if graduation_year == semester.graduation_year:
        _semester = semester
    else:
        _semester = None
    current_date = datetime.now().strftime('%Y-%m-%d')

    reports = Report.get_by_student_id(student_id)
    # group reports by (semester, week)
    report_dict = {}
    for report in reports:
        key = (report.semester, report.week)
        report_dict[key] = report

    return render_template('student/index.html', name=session['user_name'], selection=selection,
                           supervisors=supervisors,
                           types=types, deadlines=deadlines, now=datetime.now(), error=error, semester=_semester,
                           current_date=current_date, reports=report_dict)


# Student submit their selection
@bp.route('/submit')
@require_student
def submit():
    student_id = Student.get_id_by_english_name(english_name=session['user_name'])
    selection = Selection.get_by_student_id(student_id=student_id)
    submit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if selection:
        if selection.if_custom:
            # if selection.first_topic_id is None: # if selection.if_custom is true the first_topic_id will always existed
            #     return redirect(url_for('student.index', error='You have not selected any topic'))
            # else:
            selection.update_status(status=2)
            selection.update_submit_time(submit_time=submit_time)
            return redirect(url_for('student.index'))
        else:
            if selection.first_topic_id is None or selection.second_topic_id is None or selection.third_topic_id is None:
                return redirect(url_for('student.index', error='You have not full all three choices'))
            else:
                selection.update_status(status=1)
                selection.update_submit_time(submit_time=submit_time)
                return redirect(url_for('student.index', message='Successfully submit'))
    else:
        return redirect(url_for('student.index', error='You have not selected any topic'))


# Student update custom selection
@bp.route('/update_custom_topic', methods=['POST'])
@require_student
def update_custom_topic():
    student_id = Student.get_id_by_english_name(english_name=session['user_name'])
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


# Student update selection
@bp.route('/update_selection', methods=['POST'])
@require_student
def update_selection():
    student_id = Student.get_id_by_english_name(english_name=session['user_name'])
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

    # if topic:
    if match:
        if choice_number == 1:
            selection.first_topic_id = formatted_topic_id
        elif choice_number == 2:
            selection.second_topic_id = formatted_topic_id
        elif choice_number == 3:
            selection.third_topic_id = formatted_topic_id

    db.session.commit()
    return json.dumps({'success': True, 'topic_name': topic.name})
    # else:
    #     return json.dumps({'success': False, 'error': 'Topic does not exist'})


@bp.route('/handle_report', methods=['POST'])
@require_student
def handle_report():
    data = request.form
    required_fields = ['action', 'semester', 'week', 'current_plan', 'next_plan', 'issues', 'feedback']

    for field in required_fields:
        if field not in data or not data[field]:
            return Result.error(f"Missing or empty field: {field}"), 400

    student_id = Student.get_id_by_english_name(english_name=session['user_name'])
    semester = int(data['semester'])
    week = int(data['week'])
    action = data['action']

    report = Report.query.filter_by(
        student_id=student_id,
        semester=semester,
        week=week
    ).first()

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if action == 'create':
        if report:
            return Result.error("Report already exists. Use update instead."), 400
        new_report = Report(
            student_id=student_id,
            submit_time=current_time,
            update_time=current_time,
            semester=semester,
            week=week,
            current_plan=data['current_plan'],
            next_plan=data['next_plan'],
            issues=data['issues'],
            feedback=data['feedback']
        )
        new_report.add()
        return redirect(url_for('student.index'))

    elif action == 'update':
        if not report:
            return Result.error("Report not found. Create it first."), 404
        report.update(
            current_plan=data['current_plan'],
            next_plan=data['next_plan'],
            issues=data['issues'],
            feedback=data['feedback'],
            update_time=current_time
        )
        return redirect(url_for('student.index'))

    else:
        return Result.error("Invalid action"), 400
