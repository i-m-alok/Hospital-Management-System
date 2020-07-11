from flask import Flask, render_template, flash, session, redirect, request
from application import app, db
from application.forms import LoginForm
from application.models import *


""" takes to createpatient form """ 

@app.route("/createpatient")
def pr():
	return render_template("create_patient.html")


"""  patient creation """
@app.route("/addpatient", methods=["POST", "GET"])
def patient_registration():
	if request.method=='POST':
		ssn = request.form['ssn']
		name = request.form['name']
		age = request.form['age']
		doa = request.form['doa']
		typeb = request.form['typeb']
		address = request.form['address']
		state = request.form['state']
		city= request.form['city']
		p= Patient( patientSSN = ssn, name = name, age = age, dateOfAdmission = doa, typeOfBed = typeb, address = address, state = state, city = city )
		db.session.add(p)
		db.session.commit()
		return render_template("create_patient.html", message = "Patient Details Inserted Successfully")
	else:
		return render_template("home.html", user_type='admin')



"""view patient"""
@app.route("/viewpatient")
def vp():
	pat=Patient.query.all()
	return render_template("view_patient.html", patient=pat)




""" for login """
@app.route("/", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
    	user = userstore.query.filter_by(username = form.username.data, password = form.password.data).first()
    	if user is None:
    		return render_template("login.html", form = form, message = "Wrong Credentials. Please Try Again.")
    	else:
    		session['user'] = user.username
    		if user.username[0:2]=='rd':
    			user_type='admin'
    		elif user.username[0:2]=='ph':
    			user_type='pharmacist'
    		else: 
    			user_type='diagnostic'
    		return render_template("home.html",user_type=user_type, login=True, message = "Successfully Logged In!", form = form)

    return render_template("login.html", form = form)




""" for logout """
@app.route("/logout")
def logout():
	session['user']=False
	return redirect('/')
