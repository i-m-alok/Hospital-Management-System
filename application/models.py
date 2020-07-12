import flask
from application import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    userName = db.Column(db.String(20), primary_key=True,
                         unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # roleId here is foreign key which references to role table
    roleId = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role')


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    role = db.Column(db.String, nullable=False)


billing = db.Table('bill',
                   db.Column('id', db.Integer, primary_key=True,
                             unique=True, nullable=False),
                   db.Column('patientId', db.Integer, db.ForeignKey(
                       'patient.id'), nullable=False),
                   db.Column('medicineId', db.Integer,
                             db.ForeignKey('medicine.id')),
                   db.Column('testId', db.Integer, db.ForeignKey('test.id')),
                   db.Column('pieces', db.Integer),
                   db.Column('cost', db.Float, nullable=False)
                   )


class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    patientSSN = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, db.CheckConstraint(
        'age>0 and age<200'), nullable=False)
    dateOfAdmission = db.Column(db.DateTime, default=datetime.utcnow)
    typeOfBed = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    state = db.Column(db.String)
    city = db.Column(db.String)
    status = db.Column(db.String, nullable=False)
    medicine_bill = db.relationship('Medicine', secondary=billing)
    test_bill = db.relationship('Test', secondary=billing)


class Medicine(db.Model):
    __tablename__ = 'medicine'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    available = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)


class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    cost = db.Column(db.Float, nullable=False)
