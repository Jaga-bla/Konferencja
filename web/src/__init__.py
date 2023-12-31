from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from .config import Config


app = Flask(__name__)
app.config.from_object("src.config.Config")
db = SQLAlchemy(app)
app.secret_key = app.config['SECRET_KEY']

bcrypt = Bcrypt(app)


from src.routes.routes import *

from .models import models