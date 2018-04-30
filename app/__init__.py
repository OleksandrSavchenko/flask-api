from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import jwt
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = '1fdswf23fdsaf4t234gfqew'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sod2664@localhost/invoice-app'
db = SQLAlchemy(app)
