from datetime import datetime
# from app import app as flask_app
from random import randint
import pytest
import os.path
import logging
from app import people_schema, Emp

import sqlite3
import requests
# вариант тестирования через встроенный тестовый клиент фласка, первоначально тесты запускались с ним, осатвленн как альтернативный вариант
# @pytest.fixture
# def app():
#     yield flask_app
@pytest.fixture()

def paths():
    routs = 'http://127.0.0.1:3000/'
    return routs

@pytest.fixture
def client():
    return requests # не понял задачу по тестовому клиенту и решил реализовать вот так -_-

# создвает список имен сотрудников содержащихся в базе данных
def all_name():
    all_name = Emp.query.with_entities(Emp.username)
    result = people_schema.dump(all_name, many=True)
    templist = []
    for items in result:
        templist.append(items['username'])
    return templist

# запрашивает username из функции all_name и возвращает первые две буквы
def half_names():
    list_names = all_name()
    temp_storage = []
    for items in range(len(list_names)):
        temp_storage.append(list_names[items][:2])
    return temp_storage
# запрашивает в базе данных список департаментов и возвращает ее в фикстуру
def all_departments():
    all_departments = Emp.query.with_entities(Emp.department).distinct()
    result = people_schema.dump(all_departments, many=True)
    templisе_department = []
    for items in result:
        templisе_department.append(items['department'])
    return templisе_department

# Добавляет случайный айди для проверки
@pytest.fixture
def random_id():
    all_id = Emp.query.with_entities(Emp.id)
    result = people_schema.dump(all_id, many=True)
    templist=[]
    for items in result:
        templist.append(items['id'])
    randomid = templist[randint(0, len(templist) - 1)]
    return randomid

# фикстура для проверки имен сотрудников
@pytest.fixture(params=all_name())
def username(request):
    return request.param
#  фикстура для проверки эндпоинта api user
@pytest.fixture(params=half_names())
def parts_username(request):
    return request.param
#  фикстура для проверки эндпоинта api department
@pytest.fixture(params=all_departments())
def all_dep(request):
    return request.param

# хук для логирования в файл

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):


    outcome = yield # обработка идет после прохождения тестов
    rep = outcome.get_result()  # получение результатов
    date = datetime.now().strftime("%Y_%m_%d-%H_%M")

    # вызовы упавших тестов
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists(f"volume_path/report_{date}.txt") else "w"
        with open(f"volume_path/report_{date}.txt", mode) as f:

            if "tmp_path" in item.fixturenames:
                extra = " ({})".format(item.funcargs["tmp_path"])
            else:
                extra = ""

            f.write('[FAILED]: ' + rep.nodeid + extra + "\n")
            logging.info('[FAILED]: ' + rep.nodeid + ' ' + extra + " " + date)

    # вызовы успешно пройденных тестов
    elif rep.when == "call" and rep.passed:
        mode = "a" if os.path.exists(f'volume_path/report_{date}.txt') else "w"
        with open(f"volume_path/report_{date}.txt", mode) as f:

            if "tmp_path" in item.fixturenames:
                extra = " ({})".format(item.funcargs["tmp_path"])
            else:
                extra = ""

            f.write('[PASSED]: ' +rep.nodeid + extra + "\n")
            logging.info('[PASSED]: ' + rep.nodeid + ' '+ extra + " "+ date)

# делает необходимые изменения в базе данных для повторного прохождения тестов \ костыльный rollback db
@pytest.fixture
def support_for_delete():
    try:
        sqlite_connection = sqlite3.connect('volume_path/app.db')
        cursor = sqlite_connection.cursor()
        print("\n Подключен к SQLite")

        sqlite_insert_query = """INSERT INTO emp
                              (id, username, email, department, date_joined)
                              VALUES
                              (4, 'Badjaj Aqumba', 'aqumba@gmail.com','sales', '1950-05-01 09:25:10' );"""  # добавляет запись о пользователе в базу данных


        sqlite_insert_query2 = """Update emp set username = 'Rakamakofo', email = 'raka@gmail.com', 
        department = 'sales', date_joined = '1975-04-11 09:26:10' WHERE id = 11;
        """                                                                                                  # откатывает изменения в базе данных
        sqlite_insert_query3 = """DELETE from emp where id = 8;"""                                           # удаляет запись с "айди" 8 из базы данных
        cursor.execute(sqlite_insert_query)
        cursor.execute(sqlite_insert_query2)
        cursor.execute(sqlite_insert_query3)
        sqlite_connection.commit()

        print("\n Запись успешно вставлена ​​ в таблицу Emp ", cursor.rowcount)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    yield

@pytest.fixture(autouse=True) # stdout
def stdout_msg():
    print("O_o", end=' ')