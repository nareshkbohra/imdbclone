from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from argon2 import PasswordHasher

db = SQLAlchemy()
login_manager = LoginManager()
password_hasher = PasswordHasher()
