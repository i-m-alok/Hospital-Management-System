from flask import Flask, render_template, flash, session, redirect, request
from application import app, db
from application.forms import LoginForm
from application.models import *

def get_data(request):
    ssnId =  request.form.get('ssnId')
    name = request.form['name']
    age = request.form['age']
    dateOfAdmission = request.form['dateOfAdmission']
    typeOfBed = request.form['typeOfBed']
    address = request.form['address']
    state = request.form['state']
    city = request.form['city']
    return {'patientSSN':ssnId, 'name':name, 'age':age, 'dateOfAdmission':dateOfAdmission, 'typeOfBed':typeOfBed, 'address':address, 'state':state, 'city':city}

def get_data_from_patient_obj(patient_obj):
    ssnId=patient_obj.patientSSN
    name = patient_obj.name
    age =  patient_obj.age
    dateOfAdmission=  patient_obj.dateOfAdmission.date()
    typeOfBed=  patient_obj.typeOfBed
    address =  patient_obj.address
    state =  patient_obj.state
    city = patient_obj.city
    return {'patientSSN':ssnId, 'name':name, 'age':age, 'dateOfAdmission':dateOfAdmission, 'typeOfBed':typeOfBed, 'address':address, 'state':state, 'city':city}
#Home
@app.route('/home',methods=['GET','POST'])
def home():	
    if not session.get('userName'):
        return redirect('/')
    return render_template('create_patient.html')

#Create Patient Feature
@app.route('/add_patient', methods = ['GET', 'POST'])
def add_patient():
    if not session.get('userName'):
        redirect('/')
    if request.method == 'POST' and session.get('userName'):
        request_dic = get_data(request)
        #creating patient object
        patient = Patient(patientSSN = request_dic['patientSSN'], name = request_dic['name'], age = request_dic['age'], dateOfAdmission = request_dic['dateOfAdmission'], typeOfBed = request_dic['typeOfBed'], address = request_dic['address'], state = request_dic['state'], city = request_dic['city'], status = "Active")
        db.session.add(patient)
        try: 
            db.session.commit()
        except:
            flash("Your entered data is incorrect", "danger")
            return render_template("create_patient.html")
        flash("Patient creation initiated successfully", "success")
        return render_template("create_patient.html")
    else: 
        return redirect("/")

#View details of particular patient
@app.route('/view_patient', methods = ['GET', 'POST'])
def viewPatient():
    if not session.get('userName'):
        return redirect('/')
    if request.method == 'POST':
        patientid = request.form['search']
        if patientid:
            patient_obj = Patient.query.filter_by(id = patientid).first()
            patient_dict = get_data_from_patient_obj(patient_obj)
            return render_template('view.html', patientid = patientid,  name = patient_dict['name'], age = patient_dict['age'], dateOfAdmission = patient_dict['dateOfAdmission'], typeOfBed = patient_dict['typeOfBed'], address = patient_dict['address'], state = patient_dict['state'], city = patient_dict['city'])
        else: 
            flash("Please enter the patientId", 'danger')
    return render_template('view.html')

#Update Feature
@app.route("/get_patient", methods = ['GET', 'POST'])
def getPatient():
    if not session.get('userName'):
        return redirect('/')
    if request.method == 'POST':
        patientid = request.form['search']
        if patientid:
            patient_obj = Patient.query.filter_by(id = patientid).first()
            patient_dict = get_data_from_patient_obj(patient_obj)
            return render_template('update.html', patientid = patientid,  name = patient_dict['name'], age = patient_dict['age'], dateOfAdmission = patient_dict['dateOfAdmission'], typeOfBed = patient_dict['typeOfBed'], address = patient_dict['address'], state = patient_dict['state'], city = patient_dict['city'], task="update")
        else: 
            flash("Please enter the patientId", 'danger')
    return render_template('update.html', task="search")

@app.route("/update_patient", methods = ['GET', 'POST'])
def updatePatient():
    if not session.get('userName'):
        return redirect('/')
    if request.method == "POST":
        print(request.form)
        patientid = request.form['search']
        if patientid:
            patient_obj = Patient.query.filter_by(id = patientid).first()
            request_dic = get_data(request)
            try:
                print(-1)
                # request_dic = get_data(request)
                print(0)
                patient_obj.name = request_dic['name']
                print(1)
                patient_obj.age = request_dic['age']
                print(2)
                patient_obj.dateOfAdmission = request_dic['dateOfAdmission']
                patient_obj.typeOfBed = request_dic['typeOfBed']
                print(3)
                patient_obj.address = request_dic['address']
                print(4)
                patient_obj.state = request_dic['state']
                print(5)
                patient_obj.city = request_dic['city']
                print(6)
                db.session.commit()
                print(7)
                flash("Updated successfully :)", "success")
                return render_template('view.html', patientid = patientid,  name = patient_obj.name, age = patient_obj.age, dateOfAdmission = patient_obj.dateOfAdmission, typeOfBed = patient_obj.typeOfBed, address = patient_obj.address, state = patient_obj.state, city = patient_obj.city)
            except:
                flash("Invaild details entered", "danger")
        else: 
            flash("Please enter the patientId", 'danger')
    return render_template('update.html', task="search") 

        
#Show All Patients Feature
@app.route("/show_patients")
def show_patients():
    if not session.get('userName'):
        return redirect('/')
    patient = Patient.query.all()
    return render_template("show_patients.html", patient=patient)

#Login and Logout Feature
@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get("userName"):
        return redirect("/home")
    if request.method == 'POST':
        userid =  request.form['userid']
        password = request.form['password']
        user = userStore.query.filter_by(userName= userid).first() #fetch the user object from entered userid
        if user and user.password == password: #comparing if user is their with entered userid then compare its password
            session["userName"] = user.userName
            flash("You are logged in!!", "success")
            return render_template("create_patient.html")
        else:
            flash("You are invalid user!!", "danger")
    return render_template("index.html")
 
@app.route("/logout")
def logout():
    session['userName'] = False
    return redirect('/')