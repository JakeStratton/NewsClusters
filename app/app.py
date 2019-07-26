# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jake:passwordjake@localhost:5432/newsclusters'
app.secret_key = "ffrse!"

db = SQLAlchemy(app)