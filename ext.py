from flask import Flask
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "bh}3eGd'RM|~]8M+$uohNnk1"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth"