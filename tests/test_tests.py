import pytest

from app import people_schema, Emp

""" Если запускать тесты из под Docker Toolbox необходимо изменить routs в conftest.py -  
IP address of the Docker Toolbox virtual machine: host> docker-machine ip default 192.168.99.100 """


# проверка соответсвия имени пользователя в запросе и полученном json ответе \ проверяет все имена в базе данных
def test_check_content_type_names(client, username, paths):
    response = client.get(f'{paths}/api/users?username={username}')

    data = response.json()
    user_name = Emp.query.filter(Emp.username.contains(username))

    result = people_schema.dump(user_name, many=True)

    assert response.headers["Content-Type"] == "application/json"
    assert data[0]['username'] == result[0]['username']


# проверка получения ответа на неполный запрос по имени
def test_check_content_not_full_name(client, parts_username, paths):
    response = client.get(f'{paths}/api/users?username={parts_username}')
    data = response.json()
    user_name = Emp.query.filter(Emp.username.contains(parts_username))

    result = people_schema.dump(user_name, many=True)

    assert response.headers["Content-Type"] == "application/json"
    assert data[0]['username'].startswith(parts_username)
    assert data[0]['username'] == result[0]['username']


# проверка ответа на запрос по имени департамента
def test_check_content_department(client, all_dep, paths):
    response = client.get(f'{paths}/api/users?department={all_dep}')

    data = response.json()

    depart = Emp.query.filter(Emp.department.contains(all_dep))

    result = people_schema.dump(depart, many=True)

    assert response.headers["Content-Type"] == "application/json"
    assert data[0]['department'] == result[0]['department']


# проверка ответа на запрос по части имени департамента \ параметризованно так потому что нет понимания нужно ли это все прятать в конфтест
@pytest.mark.parametrize("test_input", ['fro', "backen", 'sa'])
def test_check_content_not_ful_department(client, test_input, paths):
    response = client.get(f'{paths}/api/users?department={test_input}')

    data = response.json()
    depart = Emp.query.filter(Emp.department.contains(test_input))

    result = people_schema.dump(depart, many=True)
    assert response.headers["Content-Type"] == "application/json"
    assert data[0]['department'].startswith(test_input)
    assert data[0]['department'] == result[0]['department']


# # проверка получения инфомрации на запрос по случайному айди и соответсвия полученного имнени в ответе и базе данных
def test_chek_content_json(client, random_id, paths):
    response = client.get(f'{paths}/api/users/{random_id}')
    data = response.json()
    man = Emp.query.get(random_id)
    result = people_schema.dump(man)
    assert len(data) == len(result)
    assert data['username'] == result['username']


# добавление нового сотрудника в базу данных
def test_add(client, paths):
    response = client.post(
        f'{paths}/api/addnew',
        json=
        {'id': '8', 'username': 'Victor Kozlov', 'email': 'kozlov@gmail.com', 'department': 'backend',
         'date_joined': '1990-03-03 12:33:03'})

    data = response.json()
    man = Emp.query.get(8)
    result = people_schema.dump(man)

    assert response.status_code == 200
    assert data['id'] == result['id']


# изменение информации о сотруднике в бд
def test_put(client, paths):
    response = client.put(
        f'{paths}/api/update/11',
        json={'id': '11', 'username': 'Honey Djo', 'email': 'H123_Djo@gmail.com', 'department': 'sales',
              'date_joined': '1992-02-02 13:25:55'}
    )

    data = response.json()

    man = Emp.query.get(11)
    result = people_schema.dump(man)

    assert response.status_code == 200

    assert data['username'] == result['username']



# # удаление информации о сотруднике из бд | support_for_delete обнавляет значения базы данных для прохождения тестов test_delete, test_put, test_add
def test_delete(client, support_for_delete, paths):
    support_for_delete
    response = client.delete(
        f'{paths}/api/delete/4'
    )

    assert response.status_code == 200


# # проверка ответа главной страницы
def test_user(client, paths):
    response = client.get(f'{paths}')

    assert response.status_code == 200
    # assert response.headers[0][1] == "text/html; charset=utf-8"
    # assert response.headers[1][1] == "24"
