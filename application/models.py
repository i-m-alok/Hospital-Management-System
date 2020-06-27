import flask
from application import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class userStore(db.Model):
    userName = db.Column(db.String(20), primary_key= True, nullable= False)
    password = db.Column(db.String(60), nullable= False)
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow, nullable= False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password, password)