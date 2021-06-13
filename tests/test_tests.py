from flask import json

import pytest

from app import people_schema, Emp

'''

Данное чудо тестит только 1 раз и нужно заново подкладывать бд - не реализован rallback() баззы данных.



'''

# проверка соответсвия имени пользователя в запросе и полученном json ответе \ проверяет все имена в базе данных
def test_check_content_type_names(client, username):
    response = client.get(f'/api/users?username={username}')
    data = json.loads(response.get_data(as_text=True))

    assert response.headers["Content-Type"] == "application/json"
    assert data[0]['username'] == username

# проверка получения ответа на неполный запрос по имени
def test_check_content_not_full_name(client, parts_username):
    response = client.get(f'/api/users?username={parts_username}')
    data = json.loads(response.get_data(as_text=True))

    assert response.headers["Content-Type"] == "application/json"
    assert data[0]['username'].startswith(parts_username)

# проверка ответа на запрос по имени департамента
def test_check_content_department(client, all_dep):
    response = client.get(f'/api/users?department={all_dep}')
    data = json.loads(response.get_data(as_text=True))

    assert response.headers["Content-Type"] == "application/json"
    assert data[0]['department'] == all_dep

# проверка ответа на запрос по части имени департамента \ параметризованно так потому что нет понимания нужно ли это все прятать в конфтест
@pytest.mark.parametrize("test_input", ['fro', "backen", 'sa'])
def test_check_content_not_ful_department(client, test_input):
    response = client.get(f'/api/users?department={test_input}')
    data = json.loads(response.get_data(as_text=True))

    assert response.headers["Content-Type"] == "application/json"
    assert data[0]['department'].startswith(test_input)

# проверка получения инфомрации на запрос по случайному айди и соответсвия полученного имнени в ответе и базе данных
def test_chek_content_json(client, random_id):
    response = client.get(f'/api/users/{random_id}')
    data = json.loads(response.get_data(as_text=True))
    man = Emp.query.get(random_id)
    result = people_schema.dump(man)
    assert len(data) == len(result)
    assert data['username'] == result['username']


# добавление нового сотрудника в базу данных
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

# изменение информации о сотруднике в бд
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


# удаление информации о сотруднике из бд
def test_delete(client):
    response = client.delete(
        '/api/delete/4',
        data=json.dumps(
            {'id': '4', 'username': 'Badjaj Aqumba', 'email': 'aqumba@gmail.com', 'department': 'sales',
             'date_joined': '1950-05-01 09:25:10'}),
        content_type='application/json',
    )

    assert response.status_code == 200

# проверка ответа веб страницы, т.к. ответ будет меняться при запуске всех тестов паралельно нет понимания, как проверить полноту и соответствие данных
def test_users(client):
    response = client.get('/users')

    assert response.status_code == 200


def test_user1(client, username):
    response = client.get(f'/users?user={username}')

    assert response.status_code == 200
    assert response.headers[0][1] == "text/html; charset=utf-8"

# проверка ответа главной страницы
def test_user(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.headers[0][1] == "text/html; charset=utf-8"
    assert response.headers[1][1] == "24"
