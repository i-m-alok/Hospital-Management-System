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

billed_for = db.Table(
    "bill",
    db.Column("patientId", db.Integer, db.ForeignKey('patient.id'), primary_key = True, nullable = False),
    db.Column("testId", db.Integer, db.ForeignKey('test.id'), nullable = True),
    db.Column("medicineId", db.Integer, db.ForeignKey('medicine.id'), nullable = True)
)
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True, autoincrement=True)
    patientSSN = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    age = db.Column(db.Integer, db.CheckConstraint('age<200') ,nullable = False)
    dateOfAdmission = db.Column(db.DateTime, default = datetime.utcnow)
    typeOfBed = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable = False)
    state = db.Column(db.String)
    city = db.Column(db.String)
    status = db.Column(db.String, nullable = False)
    bill_of_medicine  = db.relationship("Medicine", secondary = billed_for, backref = 'patient')
    bill_of_test = db.relationship("Test", secondary = billed_for, backref= 'patient')

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    medicineName = db.Column(db.String(30), nullable = False)
    quantityAvailable = db.Column(db.Integer, nullable = False)
    quantityIssued = db.Column(db.Integer, default = 0)
    rate = db.Column(db.Float, nullable = False)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    testName = db.Column(db.String(30), nullable = False)
    rate = db.Column(db.Float, nullable = False)