import json

from flask import session

from models.selection import Selection
from models.student import Student
from models.topic import Topic


def student_login(client, _type, status):
    if _type == 'NoSelection':
        user_name = 'crystal'
    elif _type == 'NotCustom':
        if status == 'fail':
            user_name = 'wangwu'
        else:
            user_name = 'zhangsan'
    else:
        user_name = 'lisi'
    data = {
        'user_name': user_name,
        'password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    }
    response = client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['redirect'] == '/student/home'
    assert response.json['user_type'] == 'student'


def test_submit_fail(client):
    student_login(client, 'NoSelection', 'fail')
    response = client.get('/student/submit')
    assert response.status_code == 302
    assert response.location == '/student/home?error=You+have+not+selected+any+topic'


def test_submit_fail_not_custom(client):
    student_login(client, 'NotCustom', 'fail')
    response = client.get('/student/submit')
    assert response.status_code == 302
    assert response.location == '/student/home?error=You+have+not+full+all+three+choices'


def test_submit_success_not_custom(client):
    student_login(client, 'NotCustom', 'success')
    response = client.get('/student/submit')
    _sel = Selection.get_by_id(1)
    assert response.status_code == 302
    assert _sel.status == 1
    assert response.location == '/student/home?message=Successfully+submit'


# when submit custom selection it won't fail
# def test_submit_fail_custom(client):
#     student_login(client, 'Custom', 'fail')
#     response = client.get('/student/submit')
#     assert response.status_code == 302
#     assert response.location == '/student/home?error=You+have+not+full+all+three+choices'


def test_submit_success_custom(client):
    student_login(client, 'Custom', 'success')
    response = client.get('/student/submit')
    _sel = Selection.get_by_id(3)
    assert response.status_code == 302
    assert _sel.status == 2
    assert response.location == '/student/home'


def test_update_custom_topic_success(client):
    student_login(client, 'NoSelection', 'success')
    data = {
        'topic_name': 'custom topic',
        'supervisor_id': 1,
        'description': 'custom topic description',
        'type_id': 1,
        'reset': False,
    }
    response = client.post('/student/update_custom_topic', data=data)
    assert response.status_code == 200
    # json.dumps({'success': True, 'topic_name': topic_name})
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data['success'] is True
    assert response_data['topic_name'] == 'custom topic'


def test_update_custom_topic_reset(client):
    student_login(client, 'Custom', 'success')
    data = {
        'topic_name': 'custom topic',
        'supervisor_id': 1,
        'description': 'custom topic description',
        'type_id': 1,
        'reset': 'true',
    }
    response = client.post('/student/update_custom_topic', data=data)
    assert response.status_code == 200
    # json.dumps({'success': True, 'topic_name': topic_name})
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data['success'] is True
    assert response_data['reset'] is True


def test_update_selection_fail_already_selected(client):
    student_login(client, 'NotCustom', 'fail')
    data = {
        'topic_id': 1,
        'reset': 'false',
        'choice_number': 1,
    }
    Selection.get_by_id(2).update(student_id=3, submit_time=None, status=None, first_topic_id=1, second_topic_id=1, third_topic_id=1)
    response = client.post('/student/update_selection', data=data)
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data['success'] is False
    assert response_data['error'] == 'You have already selected this topic'


def test_update_selection_fail_not_existed(client):
    student_login(client, 'NotCustom', 'fail')
    data = {
        'topic_id': 999,
        'reset': 'false',
        'choice_number': 1,
    }
    response = client.post('/student/update_selection', data=data)
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data['success'] is False
    assert response_data['error'] == 'Topic does not exist'


def test_update_selection_fail_topic_is_full(client):
    student_login(client, 'NotCustom', 'fail')
    data = {
        'topic_id': 3,
        'reset': 'false',
        'choice_number': 1,
    }
    response = client.post('/student/update_selection', data=data)
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data['success'] is False
    assert response_data['error'] == 'This topic is full'


def test_update_selection_success(client):
    student_login(client, 'NotCustom', 'fail')
    selection = Selection.get_by_id(2)
    data = {
        'topic_id': 1,
        'reset': 'false',
        'choice_number': 1,
    }
    topic = Topic.get_by_id(1)
    response = client.post('/student/update_selection', data=data)
    response_data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert selection.first_topic_id == 1
    assert response_data['success'] is True
    assert response_data['topic_name'] == topic.name


def test_update_selection_reset(client):
    student_login(client, 'NotCustom', 'fail')
    data = {
        'topic_id': 1,
        'reset': 'true',
        'choice_number': 1,
    }
    response = client.post('/student/update_selection', data=data)
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data['success'] is True
    assert response_data['reset'] is True
