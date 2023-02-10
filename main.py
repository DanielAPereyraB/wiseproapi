from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/wiseproapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


class Profile(db.Model):
    profile_id = db.Column(db.Integer, primary_key=True)
    imagen = db.Column(db.String(100))
    user_id = db.Column(db.Integer)

    def __init__(self, imagen, user_id):
        self.imagen = imagen
        self.user_id = user_id


class Color(db.Model):
    color_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    hexadecimal = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __init__(self, name, hexadecimal,description):
        self.name = name
        self.hexadecimal = hexadecimal
        self.description = description


class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer)
    color_id = db.Column(db.Integer)

    def __init__(self, name, description, user_id, color_id):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.color_id = color_id


class PaymentMethod(db.Model):
    paymentmethod_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    color_id = db.Column(db.Integer)

    def __init__(self, name, description, color_id):
        self.name = name
        self.description = description
        self.color_id = color_id


class Icons(db.Model):
    icons_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Time(db.Model):
    time_id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.DateTime)
    tasks_id = db.Column(db.Integer)

    def __init__(self, date_start, tasks_id):
        self.date_start = date_start
        self.tasks_id = tasks_id


class Bills(db.Model):
    bills_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime)
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)

    def __init__(self, amount, date, description, user_id, category_id):
        self.amount = amount
        self.date = date
        self.description = description
        self.user_id = user_id
        self.category_id = category_id


class Income_Form(db.Model):
    incomeform_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    color_id = db.Column(db.Integer)

    def __init__(self, name, description, color_id):
        self.name = name
        self.description = description
        self.color_id = color_id


class Income(db.Model):
    income_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime)
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    incomeform_id = db.Column(db.Integer)

    def __init__(self, amount, date, description, user_id, category_id, incomeform_id):
        self.amount = amount
        self.date = date
        self.description = description
        self.user_id = user_id
        self.category_id = category_id
        self.incomeform_id = incomeform_id


class Savings(db.Model):
    savings_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    salary = db.Column(db.Float)
    savings_amount = db.Column(db.Float)
    date_end = db.Column(db.DateTime)
    user_id = db.Column(db.Integer)

    def __init__(self, date, salary, savings_amount, date_end, user_id):
        self.date = date
        self.salary = salary
        self.savings_amount = savings_amount
        self.date_end = date_end
        self.user_id = user_id


class Savings_Detail(db.Model):
    Savings_Detail_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime)
    description = db.Column(db.String(100))
    savings_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)


with app.app_context():
    db.create_all()


class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id','name','email')

# Una Respuesta
user_schema = UserSchema()

# Muchas Respuesta
users_schema = UserSchema(many=True)


@app.route('/user', methods=['GET'])
def get_user():
    all_user = User.query.all()
    result = users_schema.dump(all_user)
    return jsonify(result)


@app.route('/user/<id>', methods=['GET'])
def get_user_id(id):
    one_user = User.query.get(id)
    return user_schema.jsonify(one_user)


@app.route('/user', methods=['POST'])
def insert_user():
    name = request.json['name']
    email = request.json['email']

    new_user=User(name, email)

    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)


@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user_id = User.query.get(id)
    name = request.json['name']
    email = request.json['email']

    user_id.name = name
    user_id.email = email

    db.session.commit()

    return user_schema.jsonify(user_id)


@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user_id = User.query.get(id)
    db.session.delete(user_id)
    db.session.commit()
    return user_schema.jsonify(user_id)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'Mensaje': 'Bienvenidos'})


if __name__ == "__main__":
    app.run(debug=True)