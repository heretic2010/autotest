# autotest_api

Веб-сервис храненящий информацию о пользователях. Запись списка пользователей содержит:
- id
- username
- email
- department 
- date_joined

Приложение написанно с использованием фреймворка Flask.

В качестве базы данных используется SQLite3.

Для тестирования веб-сервиса использовался фреймворк pytest.

**Endpoints:**
GET:
- / 
- /department:
  /department?name={department_name}
- /users:
  /users?department={department_name}
  /users?username={user_name}
GET:
- /api:
  /api/users?department={department_name}
  /api/users?username={user_name}
  /api/users/<id>
  /api/department
POST:
  - /api/addnew
PUT:
  - /api/update/<id>
DELETE:
  - /api/delete/<id>

**Использованные библиотеки:**
  - Flask_SQLAlchemy==2.5.1
  - flask_marshmallow==0.14.0
  - pytest==6.2.4
  - Flask==1.1.2
  - marshmallow-sqlalchemy
  - requests==2.25.1
  
**Docker-compose**
  
Для запуска тестов и приложения используйте команду:
docker-compose up


