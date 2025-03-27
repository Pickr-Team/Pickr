from datetime import datetime

from flask import Blueprint, session, redirect, url_for, request, render_template, jsonify, Response
from functools import wraps

from blueprints.utils import get_current_graduation_year
from models.report import Report
from models.result import Result
from models.student import Student
from models.supervisor import Supervisor
from models.selection import Selection
from models.type import Type
from models.topic import Topic
from models.pdf_generator import generate_topic_poster
from openpyxl import Workbook
from io import BytesIO

bp = Blueprint("supervisor", __name__, url_prefix="/supervisor")


# def require_supervisor(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user_name' not in session or session['user_type'] != 'supervisor':
#             print("Not logged in - require_supervisor")
#             return redirect(url_for('base.login'))
#         return f(*args, **kwargs)
#
#     return decorated_function


def require_supervisor_or_manager(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in session or session['user_type'] == 'student':
            return redirect(url_for('base.login'))
        return f(*args, **kwargs)

    return decorated_function


@bp.route('/')
@require_supervisor_or_manager
def redirect_to_home():
    return redirect(url_for('supervisor.index'))


@bp.route('/home')
@require_supervisor_or_manager
def index():
    supervisor_id = Supervisor.get_id_by_username(user_name=session['user_name'])
    supervisor = Supervisor.get_by_id(id=supervisor_id)
    topics = Topic.get_by_supervisor_id_not_custom(supervisor_id=supervisor_id)
    not_custom_selections = Selection.get_supervisor_selection_not_custom(supervisor_id=supervisor_id)
    custom_selections = Selection.get_supervisor_selection_custom(supervisor_id=supervisor_id)
    total_quta = 0
    for topic in topics:
        total_quta += topic.quota

    reports = Report.get_all_by_supervisor_id(supervisor_id)
    students = supervisor.get_all_students()
    is_manager = session['user_type'] == 'manager'

    return render_template('supervisor/index.html', topics=topics, supervisor=supervisor, total_quta=total_quta,
                           not_custom_selections=not_custom_selections, custom_selections=custom_selections,
                           reports=reports, students=students, is_manager=is_manager)


# Supervisor create new topic
@bp.route('/new_topic')
@require_supervisor_or_manager
def new_topic():
    types = Type.get_all()
    return render_template('supervisor/topic/new_topic.html', types=types)


# Supervisor add new topic
@bp.route('/add_topic', methods=['POST'])
@require_supervisor_or_manager
def add_topic():
    supervisor = request.form.get('supervisor')  # manager
    if supervisor:
        supervisor_id = supervisor
    else:
        supervisor_id = Supervisor.get_id_by_username(user_name=session['user_name'])
    topic_name = request.form.get('topic_name')
    type_id = request.form.get('type')
    position = request.form.get('position')
    description = request.form.get('description')
    required_skills = request.form.get('required_skills')
    reference = request.form.get('reference')

    supervisor = Supervisor.get_by_id(id=supervisor_id)
    topics = Topic.get_by_supervisor_id_not_custom(supervisor_id=supervisor_id)
    types = Type.get_all()

    total_quota = 0
    for topic_in in topics:
        total_quota += topic_in.quota

    if total_quota + int(position) > supervisor.position:
        return render_template('supervisor/topic/new_topic.html',
                               message='Excess quota, you only have ' + str(supervisor.position) + ' positions.',
                               types=types, topic_name=topic_name, type_id=type_id, position=position,
                               description=description,
                               required_skills=required_skills, reference=reference)
    _new_topic = Topic(quota=position, is_custom=False, required_skills=required_skills, reference=reference,
                       name=topic_name,
                       supervisor_id=supervisor_id,
                       description=description, type_id=type_id)
    _new_topic.add()
    if session['user_type'] == 'manager':
        return redirect(url_for('manager.index'))
    else:
        return redirect(url_for('supervisor.index'))


@bp.route('/delete/<string:_type>/<int:_id>')
@require_supervisor_or_manager
def delete(_type, _id):
    if _type == 'supTopic':
        topic = Topic.get_by_id(id=_id)
        if topic:
            if topic.get_selected_num_final() > 0 or topic.get_selected_num_total() > 0 or topic.get_selected_num() > 0:
                return jsonify(success=False, message='Can not delete this topic, students have selected this topic.')
            else:
                topic.delete()
                return jsonify(success=True, message='Delete successfully!')
        else:
            return jsonify(success=False, message='Topic does not exist')
    else:
        return jsonify(success=False, message='Type does match')


@bp.route('/edit_topic/<int:topic_id>')
@require_supervisor_or_manager
def edit_topic(topic_id):
    topic = Topic.get_by_id(id=topic_id)
    types = Type.get_all()
    return render_template('supervisor/topic/edit_topic.html', topic=topic, types=types)


# Supervisor edit topic
@bp.route('/detail_topic/<int:topic_id>')
@require_supervisor_or_manager
def detail_topic(topic_id):
    topic = Topic.get_by_id(id=topic_id)
    return render_template('base/topic_detail.html', topic=topic)


# Supervisor update topic
@bp.route('/update_topic/<int:topic_id>', methods=['POST'])
@require_supervisor_or_manager
def update_topic(topic_id):
    topic = Topic.get_by_id(id=topic_id)
    topic_name = request.form.get('topic_name')
    type_id = request.form.get('type')
    position = request.form.get('position')
    description = request.form.get('description')
    required_skills = request.form.get('required_skills')
    reference = request.form.get('reference')

    supervisor_id = Supervisor.get_id_by_username(user_name=session['user_name'])
    supervisor = Supervisor.get_by_id(id=supervisor_id)
    topics = Topic.get_by_supervisor_id_not_custom(supervisor_id=supervisor_id)
    types = Type.get_all()
    selected_num = topic.get_selected_num_final()

    total_quota = 0
    for topic_in in topics:
        total_quota += topic_in.quota

    if total_quota + int(position) - topic.quota > supervisor.position:
        return render_template('supervisor/topic/edit_topic.html',
                               message='Can not save your modify, excess quota, you only have ' + str(
                                   supervisor.position) + ' positions.',
                               topic=topic, types=types)

    if selected_num is not None and selected_num > int(position):
        return render_template('supervisor/topic/edit_topic.html',
                               message='Can not save your modify, excess quota, ' + str(
                                   selected_num) + ' students have selected this topic.',
                               topic=topic, types=types)

    topic.update(name=topic_name, supervisor_id=topic.supervisor_id, quota=position, is_custom=False, type_id=type_id,
                 description=description, required_skills=required_skills, reference=reference)
    if session['user_type'] == 'manager':
        return redirect(url_for('manager.index'))
    else:
        return redirect(url_for('supervisor.index'))


# Supervisor get the student list
@bp.route('/export_student_list')
@require_supervisor_or_manager
def export_student_list():
    supervisor_id = Supervisor.get_id_by_username(user_name=session['user_name'])
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


# Generate topic poster
@bp.route('/topic_poster')
@require_supervisor_or_manager
def topic_poster():
    supervisor_id = Supervisor.get_id_by_username(user_name=session['user_name'])
    topics = Topic.get_by_supervisor_id_not_custom(supervisor_id=supervisor_id)
    supervisor = Supervisor.get_by_id(id=supervisor_id)

    pdf_buffer = generate_topic_poster(supervisor, topics)
    pdf_buffer.seek(0)

    return Response(pdf_buffer, headers={
        'Content-Disposition': 'attachment;filename=topic_poster.pdf',
        'Content-Type': 'application/pdf'
    })


@bp.route('/report')
@require_supervisor_or_manager
def review_weekly_report():
    report_id = request.args.get('report_id')
    report = Report.get_by_id(report_id)

    report.mark_as_read()

    supervisor_id = Supervisor.get_id_by_username(user_name=session['user_name'])
    supervisor = Supervisor.get_by_id(id=supervisor_id)
    supervisor_name = supervisor.first_name + ' ' + supervisor.last_name

    graduation_year = get_current_graduation_year()
    return render_template('report/report_detail.html', supervisor_id=supervisor_id, report=report, supervisor_name=supervisor_name, graduation_year=graduation_year)


@bp.route('/report/comments', methods=['POST'])
@require_supervisor_or_manager
def comment_on_reports():
    data = request.get_json()
    report_id = data.get('report_id')
    comments = data.get('comments')
    Report.get_by_id(report_id).update(comments=comments)
    return Result.success('Provide feedback successfully!')
