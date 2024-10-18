from flask import Blueprint, session, redirect, url_for, request, render_template
from functools import wraps
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
    student_id = Student.get_id(english_name=session['user_name'])
    selection = Selection.get_by_student_id(student_id=student_id)
    supervisors = Supervisor.get_all()
    types = Type.get_all()
    error = request.args.get('error')
    deadlines = Deadline.get_all()
    return render_template('student/index.html', name=session['user_name'], selection=selection, supervisors=supervisors,
                           types=types, deadlines=deadlines, now=datetime.now(), error=error)


# Student submit their selection
@bp.route('/submit')
@require_student
def submit():
    student_id = Student.get_id(english_name=session['user_name'])
    selection = Selection.get_by_student_id(student_id=student_id)
    submit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if selection:
        if selection.if_custom:
            if selection.first_topic_id is None:
                return redirect(url_for('student.index', error='You have not selected any topic'))
            else:
                selection.update_status(status=2)
                selection.update_submit_time(submit_time=submit_time)
                return redirect(url_for('student.index'))
        else:
            if selection.first_topic_id is None or selection.second_topic_id is None or selection.third_topic_id is None:
                return redirect(url_for('student.index', error='You have full all three choices'))
            else:
                selection.update_status(status=1)
                selection.update_submit_time(submit_time=submit_time)
                return redirect(url_for('student.index'))
    else:
        return redirect(url_for('student.index', error='You have not selected any topic'))


# Student update custom selection
@bp.route('/update_custom_topic', methods=['POST'])
@require_student
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
        db.session.commit()  # 这里不应该有关于db的代码，建议应该在student model中添加reset方法
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

