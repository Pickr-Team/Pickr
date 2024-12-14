# get
def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Pickr | Login' in response.data


# post success(student)
def test_login_post_student(client):
    data = {
        'user_name': 'crystal',
        'password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    }
    response = client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['redirect'] == '/student/home'
    assert response.json['user_type'] == 'student'


# post success(supervisor)
def test_login_post_supervisor(client):
    data = {
        'user_name': 'clivia',
        'password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    }
    response = client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['redirect'] == '/supervisor/home'
    assert response.json['user_type'] == 'supervisor'


# post success(manager)
def test_login_post_admin(client):
    data = {
        'user_name': 'joojo',
        'password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92' 
    }
    response = client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['redirect'] == '/manager/home'
    assert response.json['user_type'] == 'manager'


# post fail
def test_login_post_invalid(client):
    data = {
        'user_name': 'invalid_user',
        'password_hash': 'invalid_password'
    }
    response = client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'Invalid username or password'
