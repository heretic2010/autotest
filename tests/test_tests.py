from flask import json
import pytest

'''

api tests
functional tests
data base tests

put in different files?

'''




@pytest.mark.parametrize("test_input", ['Oleg', "Vasia Orlov", "Danil Vlasov"])
def test_check_content_type_names(client, test_input):
    response = client.get(f'/api/users?username={test_input}')
    data = json.loads(response.get_data(as_text=True))
    assert response.headers["Content-Type"] == "application/json"
    assert data[0]['username'] == test_input

@pytest.mark.parametrize("test_input", ['Ol', "Vasi", "D"])
def test_check_content_not_full_name(client, test_input):
    response = client.get(f'/api/users?username={test_input}')
    data = json.loads(response.get_data(as_text=True))
    assert response.headers["Content-Type"] == "application/json"
    assert data[0]['username'].startswith(test_input)

@pytest.mark.parametrize("test_input", ['frontend', "backend"])
def test_check_content_department(client, test_input):
    response = client.get(f'/api/users?department={test_input}')
    data = json.loads(response.get_data(as_text=True))
    assert response.headers["Content-Type"] == "application/json"
    assert data[0]['department'] == test_input

@pytest.mark.parametrize("test_input", ['fro', "backen"])
def test_check_content_not_ful_department(client, test_input):
    response = client.get(f'/api/users?department={test_input}')
    data = json.loads(response.get_data(as_text=True))
    assert response.headers["Content-Type"] == "application/json"
    assert data[0]['department'].startswith(test_input)

def test_chek_content_json(client):
    response = client.get('/api/users/1')
    data = json.loads(response.get_data(as_text=True))

    assert len(data) == 5
    assert data['username'] == 'Oleg'

def test_add(client):
    response = client.post(
        '/api/addnew',
        data=json.dumps(
            {'id': '8', 'username': 'Victor Kozlov', 'email': 'kozlov@gmail.com', 'department': 'backend',
             'date_joined': '1990-03-03 12:33:03'}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200

    assert data['id'] == 8

def test_put(client):
    response = client.put(
        '/api/update/11',
        data=json.dumps({'id': '11', 'username': 'Honey Djo', 'email': 'H123_Djo@gmail.com', 'department': 'sales',
                         'date_joined': '1992-02-02 13:25:55'}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200

    assert data['email'] == 'H123_Djo@gmail.com'


def test_delete(client):
    response = client.delete(
        '/api/delete/4',
        data=json.dumps(
            {'id': '4', 'username': 'Badjaj Aqumba', 'email': 'aqumba@gmail.com', 'department': 'sales',
             'date_joined': '1950-05-01 09:25:10'}),
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

