from flask import json

'''
api tests
functional tests
data base tests

put in differents files?

'''


def test_check_content_type_equals_json(client):
    response = client.get('/api/people')
    assert response.headers["Content-Type"] == "application/json"


def test_chek_content_json(client):
    response = client.get('/api/people/1')
    data = json.loads(response.get_data(as_text=True))

    assert len(data) == 5
    assert data['username'] == 'Oleg'





def test_add(client):
    response = client.post(
        '/api/addnew',
        data=json.dumps({'id': '7', 'username': 'Victor', 'email': 'vic@gmail.com', 'department': 'sales',
                         'date_joined': '1990-01-01 12:24:00'}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200

    assert data['id'] == 7


def test_delete(client):
    response = client.delete(
        '/api/delete/7',
        data=json.dumps({'id': '7', 'username': 'Victor', 'email': 'vic@gmail.com', 'department': 'sales',
                         'date_joined': '1990-01-01 12:24:00'}),
        content_type='application/json',
    )

    assert response.status_code == 200


def test_users(client):
    response = client.get('/users')
    assert response.status_code == 200


def test_user(client):
    response = client.get('/users?user=Vlad')
    assert response.status_code == 200
    assert response.headers[0][1] == "text/html; charset=utf-8"


def test_u(client):
    res = client.get('/users?user=V')
    assert res.status_code == 200
