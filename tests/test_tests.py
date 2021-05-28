from flask import json

def test_users(client):
    res = client.get('/users')
    assert res.status_code == 200

def test_user(client):
    res = client.get('/users?user=Vlad')
    assert res.status_code == 200

def test_u(client):
    res = client.get('/users?user=V')
    assert res.status_code == 200

def test_add(client):
    response = client.post(
        '/api/addnew',
        data=json.dumps({'id':'7', 'username':'Victor', 'email':'vic@gmail.com', 'department':'sales', 'date_joined':'1990-01-01 12:24:00'}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['id'] == 7


def test_delete(client):
    response = client.post(
        '/api/delete/7',
        data=json.dumps({'id':'7', 'username':'Victor', 'email':'vic@gmail.com', 'department':'sales', 'date_joined':'1990-01-01 12:24:00'}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
