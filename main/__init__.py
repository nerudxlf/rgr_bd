from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///work.db'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)
manager = LoginManager(app)

from main import  routs, work_with_db

db.create_all()
