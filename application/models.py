import flask
from application import db
from datetime import datetime




""" Table for login and logout """

class userstore(db.Model):                                                  
    username = db.Column(db.String(80),primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable= False)


""" Association table """

billed_for = db.Table(
    "bill",
    db.Column("patientId", db.Integer, db.ForeignKey('patient.id'), nullable = False),
    db.Column("testId", db.Integer, db.ForeignKey('test.id')),
    db.Column("medicineId", db.Integer, db.ForeignKey('medicine.id'))
)


""" Table for patients  """
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
    status = db.Column(db.String, nullable = True)
    bill_of_medicine  = db.relationship("Medicine", secondary = billed_for, backref = 'patient')
    bill_of_test = db.relationship("Test", secondary = billed_for, backref= 'patient')


""" Table for medicine"""
class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    medicineName = db.Column(db.String(30), nullable = False)
    quantityAvailable = db.Column(db.Integer, nullable = False)
    quantityIssued = db.Column(db.Integer, default = 0)
    rate = db.Column(db.Float, nullable = False)


""" Table for diagnosis"""
class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    testName = db.Column(db.String(30), nullable = False)
    rate = db.Column(db.Float, nullable = False)



