import json

from models.selection import Selection
from models.topic import Topic


def supervisor_login(client):
    data = {
        'user_name': 'supervisor_2',
        'password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    }  # quota: 10
    client.post('/login', data=data, follow_redirects=True)


def test_add_topic_fail(client):
    supervisor_login(client)
    topic_data = {
        'topic_name': 'new topic',
        'type': 1,
        'position': 100,
        'description': None,
        'required_skills': None,
        'reference': None,
    }
    res = client.post('/supervisor/add_topic', data=topic_data)
    assert res.status_code == 200
    assert b'Excess quota' in res.data


def test_add_topic_success(client):
    supervisor_login(client)
    topic_data = {
        'topic_name': 'new topic 123',
        'type': 1,
        'position': 1,
        'description': None,
        'required_skills': None,
        'reference': None,
    }
    res = client.post('/supervisor/add_topic', data=topic_data, follow_redirects=True)
    new_topic = Topic.query.filter_by(name='new topic 123').first()
    assert res.status_code == 200
    assert new_topic is not None


def test_delete_topic_fail_invalid_type(client):
    supervisor_login(client)
    res = client.get('/supervisor/delete/hello/1')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['success'] is False
    assert data['message'] == 'Type does match'


def test_delete_topic_fail_topic_not_existed(client):
    supervisor_login(client)
    res = client.get('/supervisor/delete/supTopic/999')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['success'] is False
    assert data['message'] == 'Topic does not exist'


def test_delete_topic_fail_topic_has_been_selected(client):
    supervisor_login(client)
    topic_data = {
        'topic_name': 'new topic 456',
        'type': 1,
        'position': 1,
        'description': None,
        'required_skills': None,
        'reference': None,
    }
    client.post('/supervisor/add_topic', data=topic_data, follow_redirects=True)
    new_topic = Topic.query.filter_by(name='new topic 456').first()
    selection = Selection(5)  # s1
    selection.update(final_topic_id=new_topic.id, status=3)
    selection.add()
    res = client.get(f'/supervisor/delete/supTopic/{new_topic.id}')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['success'] is False
    assert data['message'] == 'Can not delete this topic, students have selected this topic.'


def test_delete_topic_success(client):
    supervisor_login(client)
    topic_data = {
        'topic_name': 'new topic 789',
        'type': 1,
        'position': 1,
        'description': None,
        'required_skills': None,
        'reference': None,
    }
    client.post('/supervisor/add_topic', data=topic_data, follow_redirects=True)
    new_topic = Topic.query.filter_by(name='new topic 789').first()
    res = client.get(f'/supervisor/delete/supTopic/{new_topic.id}')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['success'] is True
    assert data['message'] == 'Delete successfully!'


def test_update_topic_fail_has_been_selected(client):
    supervisor_login(client)
    topic_data = {
        'topic_name': 'abc',
        'type': 1,
        'position': 1,
        'description': None,
        'required_skills': None,
        'reference': None,
    }
    client.post('/supervisor/add_topic', data=topic_data, follow_redirects=True)
    new_topic = Topic.query.filter_by(name='abc').first()
    selection = Selection(5)
    selection.update(final_topic_id=new_topic.id, status=3)
    selection.add()
    update_topic_data = {
        'topic_name': 'new name',
        'type': 1,
        'position': 0,
        'description': 'new desc',
        'required_skills': 'new skills',
        'reference': 'new refer',
    }
    res = client.post(f'/supervisor/update_topic/{new_topic.id}', data=update_topic_data, follow_redirects=True)
    assert res.status_code == 200
    assert b'students have selected this topic' in res.data


def test_update_topic_fail_excess_quota(client):
    supervisor_login(client)
    topic_data = {
        'topic_name': 'abc',
        'type': 1,
        'position': 1,
        'description': None,
        'required_skills': None,
        'reference': None,
    }
    client.post('/supervisor/add_topic', data=topic_data, follow_redirects=True)
    new_topic = Topic.query.filter_by(name='abc').first()
    update_topic_data = {
        'topic_name': 'new name',
        'type': 1,
        'position': 999,
        'description': 'new desc',
        'required_skills': 'new skills',
        'reference': 'new refer',
    }
    res = client.post(f'/supervisor/update_topic/{new_topic.id}', data=update_topic_data, follow_redirects=True)
    assert res.status_code == 200
    assert b'Can not save your modify, excess quota, you only have' in res.data


def test_update_topic_success(client):
    supervisor_login(client)
    topic_data = {
        'topic_name': 'abc',
        'type': 1,
        'position': 1,
        'description': None,
        'required_skills': None,
        'reference': None,
    }
    client.post('/supervisor/add_topic', data=topic_data, follow_redirects=True)
    new_topic = Topic.query.filter_by(name='abc').first()
    update_topic_data = {
        'topic_name': 'new name',
        'type': 1,
        'position': 1,
        'description': 'new desc',
        'required_skills': 'new skills',
        'reference': 'new refer',
    }
    res = client.post(f'/supervisor/update_topic/{new_topic.id}', data=update_topic_data, follow_redirects=True)
    assert res.status_code == 200
    updated_topic = Topic.query.filter_by(name='new name').first()
    assert updated_topic.description == 'new desc'
    assert updated_topic.required_skills == 'new skills'
    assert updated_topic.reference == 'new refer'

# todo: export_student_list + topic_poster, it's hard to test these two methods
