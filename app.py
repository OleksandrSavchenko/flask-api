from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import *
import jwt
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = '1fdswf23fds'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:80989691699@localhost/invoice-app'
db = SQLAlchemy(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    print(data)

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], email=data['email'], password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({'public_id': new_user.public_id,
                        'name': new_user.name,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'])

    return jsonify({'message': 'New user created!', 'token': token.decode('UTF-8')})


@app.route('/user/<user_id>', methods=['PUT'])
def edit_user(user_id):
    return ''


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    return ''

# @app.route('/unprotected')
# def unprotected():
#     return jsonify({'message': 'Anyone can see this page'})
#
#
# @app.route('/protected')
# @token_required
# def protected():
#     return jsonify({'message': 'This page can see only authenticated users'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    unhashed_password = check_password_hash(pwhash=user.password, password=data['password'])

    if data and user and unhashed_password:
        token = jwt.encode({
            'name': user.name,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required'})


@app.route('/invoices', methods=['GET'])
def fetch_all_invoices():
    invoices = Invoice.query.all()
    return jsonify([e.serialize() for e in invoices])

if __name__ == '__main__':
    app.run(debug=True)

