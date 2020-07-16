from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
# if app.debug == True:
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Mishra981205@localhost/testing"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# else: 
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ngdhvhfmbhjnxz:7d2fe20442e5a276d103e9f8aab0cbf4c653e2204204f471e3ca59f36f9029e7@ec2-54-234-44-238.compute-1.amazonaws.com:5432/dfo5htqi24l5ek'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from application import routes

if __name__ == '__main__':
    app.run()