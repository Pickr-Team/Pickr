from datetime import datetime

import json

import pytest
from flask import session, current_app
from sqlalchemy import text

from exts import db
from models.deadline import Deadline
from models.note import Note
from models.report import Report
from models.selection import Selection
from models.semester import Semester
from models.student import Student
from models.supervisor import Supervisor
from models.topic import Topic
from models.type import Type
from models.week import Week


def manager_login(client):
    data = {
        'user_name': 'joojo',
        'password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    }  # quota:15
    client.post('/login', data=data, follow_redirects=True)


def add_student(username, graduation_year=2025):
    student = Student('', '', '', '', f'{username}', '', graduation_year)
    student.add()
    return student


def add_topic(topic_name):
    topic = Topic(topic_name, None, 1, False, None, None, None, None)
    topic.add()
    return topic


def add_selection(student_id, first_topic, second_topic, third_topic):
    selection = Selection(student_id)
    selection.add()
    selection.update(status=1, submit_time=datetime.now(), first_topic_id=first_topic.id,
                     second_topic_id=second_topic.id, third_topic_id=third_topic.id)
    return selection


def test_reset_only_old_data(client):
    clear_all(Selection, Report, Student)
    manager_login(client)
    old_student = add_student('old_student', datetime.now().year - 2)
    current_student = add_student('current_student', datetime.now().year)
    old_selection = Selection(old_student.id)
    old_selection.add()
    current_selection = Selection(current_student.id)
    current_selection.add()

    response = client.get('/manager/resetting')

    assert response.status_code == 200
    data = response.get_json()
    assert data['code'] == 200

    assert db.session.query(Student).count() == 1
    assert db.session.query(Student).filter_by(id=current_student.id).count() == 1
    assert db.session.query(Selection).count() == 1

    assert 'students: 1' in data['message']  # delete 1 previous student
    assert 'selections: 1' in data['message']  # delete 1 previous selection


def test_reset_preserves_current_year_data(client):
    clear_all(Selection, Report, Student)
    manager_login(client)

    current_student = add_student('current_student', datetime.now().year)
    Selection(current_student.id).add()

    response = client.get('/manager/resetting')

    assert response.status_code == 200
    assert db.session.query(Student).count() == 1  # 数据应被保留
    assert 'students: 0' in response.get_json()['message']  # 没有旧数据被删除


def test_refresh(client):
    manager_login(client)
    topic_1 = add_topic('topic 1')
    topic_2 = add_topic('topic 2')
    topic_3 = add_topic('topic 3')
    add_student('student 1')
    se_1 = add_selection(1, topic_1, topic_2, topic_3)
    se_1.update_status(5)
    res = client.get('/manager/refresh', follow_redirects=True)
    assert res.status_code == 200
    assert se_1.status == 0
    assert se_1.first_topic_id is None
    assert se_1.second_topic_id is None
    assert se_1.third_topic_id is None


# it's the hardest method to test
# Expected Output:
# s1: t1, t2, t3, t1
# s2: t1, t2, t3, t2
# s3: t1, t2, t3, t3
# s4: t1, t2, t3, None
def test_zzz_process(client):
    manager_login(client)
    client.get('/manager/resetting')
    topic_1 = add_topic('topic 1')
    topic_2 = add_topic('topic 2')
    topic_3 = add_topic('topic 3')
    add_student('student 1')
    add_student('student 2')
    add_student('student 3')
    add_student('student 4')
    se_1 = add_selection(1, topic_1, topic_2, topic_3)
    se_2 = add_selection(2, topic_1, topic_2, topic_3)
    se_3 = add_selection(3, topic_1, topic_2, topic_3)
    se_4 = add_selection(4, topic_1, topic_2, topic_3)
    res = client.get('/manager/process', follow_redirects=True)
    assert res.status_code == 200
    assert se_1.final_topic_id == topic_1.id
    assert se_2.final_topic_id == topic_2.id
    assert se_3.final_topic_id == topic_3.id
    assert se_4.final_topic_id is None


def test_add_note(client):
    manager_login(client)
    note_data = {
        'title': 'note123',
        'content': 'note123content'
    }
    res = client.post('/manager/add_note', data=note_data, follow_redirects=True)
    assert res.status_code == 200
    new_note = Note.query.filter_by(title='note123').first()
    assert new_note is not None
    assert new_note.content == 'note123content'


def test_update_note(client):
    manager_login(client)
    note_data = {
        'title': 'note123',
        'content': 'note123content'
    }
    res = client.post('/manager/add_note', data=note_data, follow_redirects=True)
    assert res.status_code == 200
    new_note = Note.query.filter_by(title='note123').first()
    new_title = "Updated Note Title"
    new_content = "This note has been updated."
    response = client.post(f'/manager/update_note/{new_note.id}', data={'title': new_title, 'content': new_content},
                           follow_redirects=True)
    assert response.status_code == 200
    assert new_note.title == new_title
    assert new_note.content == new_content


def test_add_type(client):
    manager_login(client)
    response = client.post('/manager/add_type', data={'name': 'New Type'}, follow_redirects=True)
    assert response.status_code == 200
    new_type = Type.query.filter_by(name='New Type').first()
    assert new_type is not None


def test_update_type(client):
    manager_login(client)
    response = client.post('/manager/add_type', data={'name': 'New Type 2'}, follow_redirects=True)
    assert response.status_code == 200
    new_type = Type.query.filter_by(name='New Type 2').first()
    response = client.post(f'/manager/update_type/{new_type.id}', data={'name': 'abcd'}, follow_redirects=True)
    assert response.status_code == 200
    assert new_type is not None
    assert new_type.name == 'abcd'


def test_add_student(client):
    manager_login(client)
    client.get('/manager/resetting')
    response = client.post('/manager/add_student', data={
        'chinese_name': '张三',
        'english_name': 'Zhang San',
        'class_number': '101',
        'email': 'zhangsan@example.com',
        'username': 'zhangsan'
    })
    assert response.status_code == 302
    new_student = Student.query.filter_by(user_name='zhangsan').first()
    assert new_student is not None


def test_update_student(client):
    manager_login(client)
    existing_student = Student.query.filter_by(user_name='wangwu').first()
    assert existing_student is not None
    student_id = existing_student.id
    response = client.post(f'/manager/update_student/{student_id}', data={
        'chinese_name': '王五2',
        'english_name': 'Wang Wu',
        'class_number': '103',
        'email': 'wangwu@example.com',
        'username': 'wangwu2'
    })
    assert response.status_code == 302
    updated_student = Student.query.filter_by(id=student_id).first()
    assert updated_student.chinese_name == '王五2'
    assert updated_student.english_name == 'Wang Wu'
    assert updated_student.class_number == '103'
    assert updated_student.email == 'wangwu@example.com'
    assert updated_student.user_name == 'wangwu2'


def test_add_supervisor(client):
    manager_login(client)
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'position': '10',
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'expertise': 'null'
    }
    response = client.post('/manager/add_supervisor', data=data)
    assert response.status_code == 302
    new_supervisor = Supervisor.query.filter_by(user_name='johndoe').first()
    assert new_supervisor is not None
    assert new_supervisor.first_name == 'John'
    assert new_supervisor.last_name == 'Doe'
    assert new_supervisor.password == '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'


def test_update_supervisor(client):
    manager_login(client)
    new_supervisor = Supervisor(first_name='John', last_name='Doe', position='10',
                                user_name='johndoe',
                                password='8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
                                email='johndoe@example.com', is_admin=False, expertise='null')
    new_supervisor.add()

    new_topic = Topic(name='Test Topic', quota=5, supervisor_id=new_supervisor.id, is_custom=False, type_id=None,
                      description=None, required_skills=None, reference=None)
    new_topic.add()

    update_data = {
        'first_name': 'Jane',
        'last_name': 'Wang',
        'position': '5',
        'username': 'janedoe',
        'email': 'janedoe@example.com'
    }
    response = client.post(f'/manager/update_supervisor/{new_supervisor.id}', data=update_data)
    assert response.status_code == 302
    updated_supervisor = Supervisor.query.filter_by(user_name='janedoe').first()
    assert updated_supervisor is not None
    assert updated_supervisor.first_name == 'Jane'
    assert updated_supervisor.last_name == 'Wang'
    assert updated_supervisor.position == 5
    # fail
    update_data['position'] = '1'
    response = client.post(f'/manager/update_supervisor/{new_supervisor.id}', data=update_data)
    assert response.status_code == 200
    assert b'Can not save your modify, excess quota' in response.data


def test_reset_password(client):
    student = Student(None, None, None, '123456', 'abc', None, 2025)
    student.add()
    manager_login(client)
    res = client.post('/manager/reset_password', data={'user_id': student.id, 'user_type': 'student'})
    data = res.get_json()
    assert data['status'] == 'success'
    assert student.password == '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    supervisor = Supervisor(None, None, None, None, 'def', '678910', None, None)
    supervisor.add()
    res = client.post('/manager/reset_password', data={'user_id': supervisor.id, 'user_type': 'supervisor'})
    data = res.get_json()
    assert data['status'] == 'success'
    assert supervisor.password == '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'


def deadlines():
    Deadline.query.delete()
    first_deadline = Deadline(submit_time='2024-10-01 12:00:00', result_time='2024-10-01 14:00:00', note='First round')
    second_deadline = Deadline(submit_time='2024-10-10 12:00:00', result_time='2024-10-10 14:00:00',
                               note='Second round')
    first_deadline.add()
    second_deadline.add()


def test_update_deadline_reset(client):
    manager_login(client)
    round_num = 1
    deadlines()
    data = {
        'round_num': round_num,
        'submit_time': '12:30',
        'result_time': '14:30',
        'note': 'Updated note',
        'reset': 'true'
    }
    response = client.post('/manager/update_deadline', data=data, content_type='application/x-www-form-urlencoded')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    first_deadline = Deadline.get_first()
    second_deadline = Deadline.get_second()
    assert response_data['success'] is True
    assert response_data['reset'] is True
    assert first_deadline.submit_time is None
    assert first_deadline.result_time is None
    assert first_deadline.note is None
    assert second_deadline.submit_time is not None
    assert second_deadline.result_time is not None
    assert second_deadline.note is not None


def test_update_deadline_update(client):
    manager_login(client)
    round_num = 2
    deadlines()
    data = {
        'round_num': round_num,
        'submit_time': '13:15',
        'result_time': '15:15',
        'note': 'Another updated note'
    }
    response = client.post('/manager/update_deadline', data=data, content_type='application/x-www-form-urlencoded')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    second_deadline = Deadline.get_second()
    assert response_data['success'] is True
    assert second_deadline.submit_time == '13:15'
    assert second_deadline.result_time == '15:15'
    assert second_deadline.note == 'Another updated note'


def test_delete_student_success(client):
    manager_login(client)
    Selection.query.delete()
    Student.query.delete()
    student = Student(None, None, None, '123456', 'abc', None, 2025)
    student.add()
    res = client.get(f'/delete/student/{student.id}')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert data['message'] == 'Delete Successfully'


def test_delete_student_fail_student_has_selection(client):
    manager_login(client)
    Selection.query.delete()
    Student.query.delete()
    student = Student(None, None, None, '123456', 'abc', None, 2025)
    student.add()
    selection = Selection(student.id)
    selection.add()
    res = client.get(f'/delete/student/{student.id}')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is False
    assert data['message'] == 'Can not delete this student, student has selected topics.'


def test_delete_student_fail_student_does_not_exist(client):
    manager_login(client)
    Selection.query.delete()
    Student.query.delete()
    res = client.get('/delete/student/999')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is False
    assert data['message'] == 'Student does not exist'


def test_delete_supervisor_success(client):
    supervisor = Supervisor(None, None, None, None, 'abcdef', '678910', None, None)
    supervisor.add()
    manager_login(client)
    res = client.get(f'/delete/supervisor/{supervisor.id}')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert data['message'] == 'Delete Successfully'


def test_delete_topic_success(client):
    manager_login(client)
    topic = Topic(None, None, None, None, None, None, None, None)
    topic.add()
    res = client.get(f'/delete/supTopic/{topic.id}')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert data['message'] == 'Delete Successfully'


def test_delete_topic_fail_topic_has_been_selected(client):
    manager_login(client)
    topic = Topic(None, None, None, None, None, None, None, None)
    topic.add()
    student = Student(None, None, None, None, None, None, 2025)
    student.add()
    selection = Selection(student.id)
    selection.update_status(0)
    selection.update_first_topic_id(topic.id)
    selection.add()
    res = client.get(f'/delete/supTopic/{topic.id}')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is False
    assert data['message'] == 'Can not delete this topic, students have selected this topic.'


def test_delete_topic_fail_topic_not_exist(client):
    manager_login(client)
    res = client.get('/delete/supTopic/999')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is False
    assert data['message'] == 'Topic does not exist'


def test_delete_type_success(client):
    manager_login(client)
    _type = Type(None)
    _type.add()
    res = client.get(f'/delete/type/{_type.id}')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert data['message'] == 'Delete Successfully'


def test_delete_type_fail_type_has_topics(client):
    manager_login(client)
    _type = Type(None)
    _type.add()
    topic = Topic(None, None, None, None, _type.id, None, None, None)
    topic.add()
    res = client.get(f'/delete/type/{_type.id}')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is False
    assert data['message'] == 'Can not delete this type, type has topics.'


def test_delete_type_fail_type_not_exist(client):
    manager_login(client)
    res = client.get('/delete/type/999')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is False
    assert data['message'] == 'Type does not exist'


def test_delete_note_success(client):
    manager_login(client)
    note = Note(None, None)
    note.add()
    res = client.get(f'/delete/note/{note.id}')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert data['message'] == 'Delete Successfully'


def test_delete_note_fail_note_not_exist(client):
    manager_login(client)
    res = client.get('/delete/note/999')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is False
    assert data['message'] == 'Note does not exist'


def test_fail_students(client):
    manager_login(client)
    clear_all(Student, Selection)
    student_1 = add_student('s1')
    student_2 = add_student('s2')
    student_3 = add_student('s3')
    se_1 = Selection(student_1.id)
    se_2 = Selection(student_2.id)
    se_3 = Selection(student_3.id)
    se_1.update_status(5)
    se_2.update_status(5)
    se_3.update_status(4)
    se_1.add()
    se_2.add()
    se_3.add()
    res = client.get('/manager/fail_students')
    assert res.status_code == 200
    expected_json = {
        'students': [
            {'id': 1, 'user_name': 's1'},
            {'id': 2, 'user_name': 's2'}
        ]
    }
    res_data = json.loads(res.data)
    assert len(res_data['students']) == 2
    assert res_data['students'][0]['user_name'] == 's1'
    assert res_data['students'][1]['user_name'] == 's2'
    # pytest - s test_manager.py::test_fail_students


def test_update_custom_selection_status_3(client):
    manager_login(client)
    clear_all(Student, Selection)
    student_1 = add_student('s1')
    selection = Selection(student_1.id)
    selection.add()
    selection.update_first_topic_id(1)
    supervisor = Supervisor('', '', False, 10, 'abcdef', '678910', '', '')
    supervisor.add()
    response = client.post(
        f'/manager/update_custom_selection/{selection.id}',
        data={
            'supervisor': supervisor.id,
            'name': 'Test Topic',
            'description': 'This is a test description.',
            'type': None,
            'status': 3
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert selection.status == 3
    assert selection.first_topic.supervisor_id == supervisor.id
    assert selection.first_topic.name == 'Test Topic'
    assert selection.first_topic.description == 'This is a test description.'
    assert selection.first_topic.type_id is None
    assert selection.final_topic_id == selection.first_topic_id  # 因为 status 是 '3'


def clear_all(*tables):
    """Clear specified tables in reverse dependency order.
    Usage: clear_all(Student, Selection)  # 删除 Student 和 Selection 表
    """
    with current_app.app_context():
        db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))

        for model in tables:
            try:
                db.session.query(model).delete()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error clearing {model.__tablename__}: {str(e)}")

        db.session.execute(text('SET FOREIGN_KEY_CHECKS = 1;'))
        db.session.commit()


def test_update_custom_selection_status_2(client):
    manager_login(client)
    clear_all(Student, Selection)
    student_1 = add_student('s1')
    selection = Selection(student_1.id)
    selection.add()
    selection.update_first_topic_id(2)
    supervisor = Supervisor('', '', False, 10, 'abcdef', '678910', '', '')
    supervisor.add()
    response = client.post(
        f'/manager/update_custom_selection/{selection.id}',
        data={
            'supervisor': supervisor.id,
            'name': 'Test Topic',
            'description': 'This is a test description.',
            'type': None,
            'status': 2
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert selection.status == 2
    assert selection.first_topic.supervisor_id == supervisor.id
    assert selection.first_topic.name == 'Test Topic'
    assert selection.first_topic.description == 'This is a test description.'
    assert selection.first_topic.type_id is None
    assert selection.final_topic_id is None


def test_edit_student(client):
    manager_login(client)
    stu = add_student('Anna')
    response = client.get(f'/manager/edit/student/{stu.id}')
    assert response.status_code == 200
    assert b'Edit Student' in response.data
    supervisor = Supervisor('', '', False, 10, 'olaf', '678910', '', '')
    supervisor.add()
    response = client.get(f'/manager/edit/supervisor/{supervisor.id}')
    assert response.status_code == 200
    assert b'Edit Supervisor' in response.data
    response = client.get('/manager/edit/supTopic/1')
    assert response.status_code == 200
    assert b'Edit Topic' in response.data


def test_detail(client):
    manager_login(client)
    res = client.get('manager/detail/supervisor/1')
    assert res.status_code == 200
    assert b'Supervisor Info' in res.data
    res = client.get('manager/detail/student/1')
    assert res.status_code == 200
    assert b'Student Status' in res.data
    se = Selection.get_all()
    res = client.get(f'manager/detail/topic/{se[0].id}')
    assert res.status_code == 200
    assert b'Modify Status' in res.data
    topics = Topic.get_not_custom()
    res = client.get(f'manager/detail/supTopic/{topics[0].id}')
    assert res.status_code == 200
    html_content = res.data.decode('utf-8')
    assert topics[0].name in html_content
