from flask import flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:""@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = false

SQLAlchemy(app)