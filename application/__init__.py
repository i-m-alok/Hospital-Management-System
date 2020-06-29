from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:*******/Hospital"
db = SQLAlchemy(app)

from application import routes