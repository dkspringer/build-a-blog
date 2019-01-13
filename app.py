import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

with open('params.json') as file:
    params = json.load(file)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    params.get('user'),
    params.get('password'),
    params.get('ip'),
    params.get('port'),
    params.get('db_name')
)
db = SQLAlchemy(app)
app.secret_key = params.get('secret_key')
