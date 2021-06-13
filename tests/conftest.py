import pytest
from app import app as flask_app
import logging
import time
from random import randint


from app import people_schema, ma, Emp, db

@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def all_name():
    all_name = Emp.query.with_entities(Emp.username)
    result = people_schema.dump(all_name, many=True)
    templist = []
    for items in result:
        templist.append(items['username'])
    return templist


def half_names():
    list_names = all_name()
    temp_storage = []
    for items in range(len(list_names)):
        temp_storage.append(list_names[items][:2])
    return temp_storage

def all_departments():
    all_departments = Emp.query.with_entities(Emp.department).distinct()
    result = people_schema.dump(all_departments, many=True)
    templisе_department = []
    for items in result:
        templisе_department.append(items['department'])
    return templisе_department

@pytest.fixture
def random_id():
    all_id = Emp.query.with_entities(Emp.id)
    result = people_schema.dump(all_id, many=True)
    templist=[]
    for items in result:
        templist.append(items['id'])
    randomid = templist[randint(0, len(templist) - 1)]
    return randomid


@pytest.fixture(params=all_name())
def username(request):
    return request.param

@pytest.fixture(params=half_names())
def parts_username(request):
    return request.param

@pytest.fixture(params=all_departments())
def all_dep(request):
    return request.param








# def pytest_terminal_summary(terminalreporter):
#
#     print('passed amount:', len(terminalreporter.stats['passed']))
#     # print('failed amount:', len(terminalreporter.stats['failed']))
#     # print('xfailed amount:', len(terminalreporter.stats['xfailed']))
#     # print('skipped amount:', len(terminalreporter.stats['skipped']))
#
#     duration = time.time() - terminalreporter._sessionstarttime
#     print('duration:', duration, 'seconds')

