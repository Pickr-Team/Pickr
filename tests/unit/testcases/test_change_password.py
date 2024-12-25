# get
def test_change_password(client):
    data = {
        'user_name': 'crystal',
        'password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    }
    response = client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200
    response = client.get('/change_password')
    assert response.status_code == 200
    assert b'Change Password' in response.data


#change_password success(student)
def test_change_password_student(client):
    data = {
        'user_name': 'crystal',
        'password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    }
    response = client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200
    change_pwd_data = {
        'new_password_hash': '96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e',
        'old_password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
    }
    _response = client.post('/change_password', data=change_pwd_data, follow_redirects=True)
    assert _response.status_code == 200
    assert _response.json['status'] == 'success'
    # assert response.json['redirect'] == '/login'  # /student/home


# change_password success(supervisor)
def test_change_password_supervisor(client):
    data = {
        'user_name': 'clivia',
        'password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    }
    response = client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['redirect'] == '/supervisor/home'
    assert response.json['user_type'] == 'supervisor'
    change_pwd_data = {
        'new_password_hash': '96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e',
        'old_password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
    }
    _response = client.post('/change_password', data=change_pwd_data, follow_redirects=True)
    assert _response.status_code == 200
    assert _response.json['status'] == 'success'


# change_password success(manager)
def test_change_password_admin(client):
    data = {
        'user_name': 'joojo',
        'password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    }
    response = client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['redirect'] == '/manager/home'
    assert response.json['user_type'] == 'manager'
    change_pwd_data = {
        'new_password_hash': '96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e',
        'old_password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
    }
    _response = client.post('/change_password', data=change_pwd_data, follow_redirects=True)
    assert _response.status_code == 200
    assert _response.json['status'] == 'success'


# change_password fail
def test_login_post_invalid(client):
    data = {
        'user_name': 'crystal',
        'password_hash': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    }
    response = client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['redirect'] == '/student/home'
    assert response.json['user_type'] == 'student'
    change_pwd_data = {
        'new_password_hash': '96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e',
        'old_password_hash': '123456',  # wrong password
    }
    _response = client.post('/change_password', data=change_pwd_data, follow_redirects=True)
    assert _response.status_code == 200
    assert _response.json['status'] == 'fail'
