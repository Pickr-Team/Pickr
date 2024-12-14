import json


# get topic list
def test_topic_list(client):
    response = client.get('/list')
    assert response.status_code == 200
    assert b'Topic List' in response.data


# topic search success
def test_topic_search(client):
    response = client.get('/search?search_query=Supervisor Topic')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['topic_ids'] == [1, 2, 3]


# topic search fail
def test_topic_search_no_result(client):
    response = client.get('/search?search_query=nothing')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['topic_ids'] == []


# supervisor topic detail
def test_topic_detail(client):
    response = client.get('/topic_detail/1', follow_redirects=True)
    assert response.status_code == 200


# supervisor topic detail
def test_topic_detail_not_existed(client):
    response = client.get('/topic_detail/999', follow_redirects=True)
    assert response.status_code == 404


# # topic detail
def test_custom_topic_detail(client):
    response = client.get('/topic_detail_custom/4', follow_redirects=True)
    assert response.status_code == 200

# custom topic detail
def test_custom_topic_detail_not_existed(client):
    response = client.get('/topic_detail_custom/999', follow_redirects=True)
    assert response.status_code == 404