from flask import Flask, render_template, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Emp(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(200), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.isoformat)

    def __init__(self, id, username, email, department, date_joined):
        self.id = id
        self.username = username
        self.email = email
        self.department = department
        self.date_joined = date_joined

    def __repr__(self):
        return 'User %r' % self.id


class PeopleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'department', 'date_joined')


people_schema = PeopleSchema()


@app.route('/api/users/<id>', methods=['GET'])
def get_man(id):
    man = Emp.query.get(id)
    return people_schema.jsonify(man)


@app.route('/api/users', methods=['GET'])
def user_items_api():
    user = request.args.get("username")
    department = request.args.get("department")

    if user != None:

        items = Emp.query.filter(Emp.username.contains(user))
        result = people_schema.dump(items, many=True)
        return jsonify(result)

    elif department != None:

        items = Emp.query.filter(Emp.department.contains(department))
        result = people_schema.dump(items, many=True)
        return jsonify(result)

    else:
        items = Emp.query.all()
        result = people_schema.dump(items, many=True)
        return jsonify(result)


@app.route('/api/department', methods=['GET'])
def department_items_api():
    department = request.args.get("name")
    if department != None:

        item = Emp.query.filter(Emp.department.contains(department)).with_entities((Emp.department)).distinct()
        result = people_schema.dump(item, many=True)
        return jsonify(result)

    else:
        item = Emp.query.with_entities(Emp.department)
        result = people_schema.dump(item, many=True)
        return jsonify(result)


@app.route('/api/addnew', methods=['POST'])
def add_man():
    id = request.json['id']
    username = request.json['username']
    email = request.json['email']
    department = request.json['department']
    date_joined = request.json['date_joined']

    new_man = Emp(id, username, email, department, datetime.fromisoformat(date_joined))
    db.session.add(new_man)
    db.session.commit()
    return people_schema.jsonify(new_man)


@app.route('/api/update/<id>', methods=['PUT'])
def update_man(id):
    people = Emp.query.get(id)
    id = request.json['id']
    username = request.json['username']
    email = request.json['email']
    department = request.json['department']
    date_joined = request.json['date_joined']

    people.id = id
    people.username = username
    people.email = email
    people.department = department
    people.date_joined = datetime.fromisoformat(date_joined)

    db.session.commit()
    return people_schema.jsonify(people)


@app.route('/api/delete/<id>', methods=['DELETE'])
def delete_man(id):
    man = Emp.query.get(id)
    db.session.delete(man)
    db.session.commit()
    return people_schema.jsonify(man)


@app.route('/')
def hello_app():
    return 'Welcome to test web app!'


@app.route('/users')
def user_items():
    user = request.args.get("username")
    department = request.args.get("department")

    if user != None:

        items = Emp.query.filter(Emp.username.contains(user))
        return render_template('users.html', items=items)

    elif department != None:

        items = Emp.query.filter(Emp.department.contains(department))
        return render_template('users.html', items=items)

    else:
        items = Emp.query.all()
        return render_template('users.html', items=items)


@app.route('/department')
def department_items():
    department = request.args.get("name")
    if department != None:
        items = Emp.query.filter(Emp.department.contains(department)).with_entities((Emp.department)).distinct()

        return render_template('users.html', items=items)

    else:
        items = Emp.query.with_entities(Emp.department)

        return render_template('users.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
