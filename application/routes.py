from datetime import date
from flask import Flask, render_template, flash, session, redirect, request, url_for
from application import app, db
from application.forms import LoginForm
from application.models import *


def get_data(request):
    ssnId = request.form.get('ssnId')
    name = request.form['name']
    age = request.form['age']
    dateOfAdmission = request.form['dateOfAdmission']
    typeOfBed = request.form['typeOfBed']
    address = request.form['address']
    state = request.form['state']
    city = request.form['city']
    return {'patientSSN': ssnId, 'name': name, 'age': age, 'dateOfAdmission': dateOfAdmission, 'typeOfBed': typeOfBed, 'address': address, 'state': state, 'city': city}


def get_data_from_patient_obj(patient_obj):
    ssnId = patient_obj.patientSSN
    name = patient_obj.name
    age = patient_obj.age
    dateOfAdmission = patient_obj.dateOfAdmission.date()
    typeOfBed = patient_obj.typeOfBed
    address = patient_obj.address
    state = patient_obj.state
    city = patient_obj.city
    return {'patientSSN': ssnId, 'name': name, 'age': age, 'dateOfAdmission': dateOfAdmission, 'typeOfBed': typeOfBed, 'address': address, 'state': state, 'city': city}

def calculateRoomCharges(typeofBed, noOfDays):
    if typeofBed == 'type-1':
        return noOfDays * 2000
    elif typeofBed == 'type-2':
        return noOfDays * 4000
    else:
        return noOfDays * 8000

# Home


@app.route('/home', methods=['GET', 'POST'])
def home():
    if not session.get('userName'):
        return redirect('/')
    return render_template('create_patient.html')

# Create Patient Feature


@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if not session.get('userName'):
        redirect('/')
    if request.method == 'POST' and session.get('userName'):
        request_dic = get_data(request)
        # creating patient object
        print(request.form)
        patient = Patient(patientSSN=request_dic['patientSSN'], name=request_dic['name'], age=request_dic['age'], dateOfAdmission=request_dic['dateOfAdmission'],
                          typeOfBed=request_dic['typeOfBed'], address=request_dic['address'], state=request_dic['state'], city=request_dic['city'], status="Active")
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

# View details of particular patient


@app.route('/view_patient', methods=['GET', 'POST'])
def viewPatient():
    if not session.get('userName'):
        return redirect('/')
    if request.method == 'POST':
        patientid = request.form['search']
        if patientid:
            patient_obj = Patient.query.filter_by(id=patientid).first()
            if patient_obj:
                patient_dict = get_data_from_patient_obj(patient_obj)
            else:
                flash("No patient with entered patientId", 'danger')
                return render_template('view.html')
            return render_template('view.html', patientid=patientid,  name=patient_dict['name'], age=patient_dict['age'], dateOfAdmission=patient_dict['dateOfAdmission'], typeOfBed=patient_dict['typeOfBed'], address=patient_dict['address'], state=patient_dict['state'], city=patient_dict['city'])
        else:
            flash("Please enter the patientId", 'danger')
    return render_template('view.html')

# Update Feature


@app.route("/get_patient/<feature>", methods=['GET', 'POST'])
def getPatient(feature):
    if not session.get('userName'):
        return redirect('/')
    if request.method == 'POST':
        patientid = request.form['search']
        # print(feature)
        if patientid:
            patient_obj = Patient.query.filter_by(id=patientid).first()
            if patient_obj:
                patient_dict = get_data_from_patient_obj(patient_obj)
                if(feature == "update"):
                    return render_template('update.html', patientid=patientid,  name=patient_dict['name'], age=patient_dict['age'], dateOfAdmission=patient_dict['dateOfAdmission'], typeOfBed=patient_dict['typeOfBed'], address=patient_dict['address'], state=patient_dict['state'], city=patient_dict['city'], task="update")
                elif(feature == "delete"):
                    return render_template('delete.html', patientid=patientid,  name=patient_dict['name'], age=patient_dict['age'], dateOfAdmission=patient_dict['dateOfAdmission'], typeOfBed=patient_dict['typeOfBed'], address=patient_dict['address'], state=patient_dict['state'], city=patient_dict['city'], task="delete")
            else:
                flash("No Patient is there with entered Id", "danger")
        else:
            flash("Please enter the patientId", 'danger')
    if(feature == "update"):
        return render_template('update.html', task="search")
    elif(feature == "delete"):
        return render_template('delete.html', task="search")


@app.route("/update_patient", methods=['GET', 'POST'])
def updatePatient():
    if not session.get('userName'):
        return redirect('/')
    if request.method == "POST":
        # print(request.form)
        patientid = request.form['search']
        if patientid:
            patient_obj = Patient.query.filter_by(id=patientid).first()
            request_dic = get_data(request)
            try:
                patient_obj.name = request_dic['name']
                patient_obj.age = request_dic['age']
                patient_obj.dateOfAdmission = request_dic['dateOfAdmission']
                patient_obj.typeOfBed = request_dic['typeOfBed']
                patient_obj.address = request_dic['address']
                patient_obj.state = request_dic['state']
                patient_obj.city = request_dic['city']
                db.session.commit()
                flash("Updated successfully :)", "success")
                return render_template('update.html', task="search")
            except:
                flash("Invaild details entered", "danger")
        else:
            flash("Please enter the patientId", 'danger')
    return render_template('update.html', task="search")

# Delete Part


@app.route("/delete_patient", methods=['GET', 'POST'])
def deletePatient():
    if not session.get('userName'):
        return redirect('/')
    if request.method == "POST":
        patientid = request.form['search']
        if patientid:
            try:
                patient_obj = Patient.query.filter_by(id=patientid).first()
                db.session.delete(patient_obj)
                db.session.commit()
                flash("Deletion Initiated Successfully", "success")
                return render_template('delete.html', task='search')
            except:
                flash("Please try to it again", 'danger')
        else:
            flash("Please enter the patientId", "danger")
    return render_template('delete.html', task="search")

# Show All Patients Feature


@app.route("/show_patients")
def show_patients():
    if not session.get('userName'):
        return redirect('/')
    patient = Patient.query.filter_by(status="Active").all()
    return render_template("show_patients.html", patient=patient)

#fetch medicines of patient


@app.route("/fetch/<details>", methods=['GET', 'POST'])
def fetchIssuedMedicine(details):
    if not session.get("userName"):
        return redirect("/")
    if request.method == 'POST':
        patientid = request.form['patientid']
        patient_obj = Patient.query.filter_by(id=patientid).first()
        if patient_obj:
            patient_data = get_data_from_patient_obj(patient_obj)
            #to find the bills belongs to medicine
            if details=='medicine':
                bill = db.session.query(billing).filter(
                    billing.c.patientId == patientid).filter(billing.c.medicineId != None).all()
                med = {}
                for each in bill:
                    medicine = Medicine.query.filter_by(id=each[2]).first()
                    #initialize dictionary for medicines
                    med[each[2]] = {
                        'quantity': each[4],
                        'amount': each[5],
                        'name': medicine.name,
                        'rate': medicine.cost
                    }
                return render_template('issued_medicine.html', patientid=patientid, patient_data=patient_data, medicines=med, details = 'medicine')
            #to find the bills belongs to tests
            elif details == 'test':
                bill = db.session.query(billing).filter(
                    billing.c.patientId == patientid).filter(billing.c.testId != None).all()
                tests = {}
                for each in bill:
                    test = Test.query.filter_by(id=each[3]).first()
                    tests[each[3]] = {
                        'amount': each[5],
                        'name': test.name
                    }
                return render_template('issued_medicine.html', patientid=patientid, patient_data=patient_data, tests=tests, details='test')
            elif details == 'test&&medicine':
                #all test bills
                testBill = db.session.query(billing).filter(billing.c.patientId == patientid).filter(billing.c.testId != None).all()
                #all medicine bills
                medicineBill = db.session.query(billing).filter(
                    billing.c.patientId == patientid).filter(billing.c.medicineId != None).all()
                medicines = {}
                medicineTotal = 0
                tests = {}
                testTotal = 0
                for each in testBill:
                    test = Test.query.filter_by(id=each[3]).first()
                    tests[each[3]] = {
                        'amount': each[5],
                        'name': test.name
                    }
                    testTotal+=each[5]
                for each in medicineBill:
                    medicine = Medicine.query.filter_by(id=each[2]).first()
                    #initialize dictionary for medicines
                    medicines[each[2]] = {
                        'quantity': each[4],
                        'amount': each[5],
                        'name': medicine.name,
                        'rate': medicine.cost
                    }
                    medicineTotal=each[5]
                dateOfDischarged = date.today()
                noOfDays = (dateOfDischarged - patient_data['dateOfAdmission']).days
                roomCharge = calculateRoomCharges(patient_data['typeOfBed'], noOfDays)
                total = roomCharge+medicineTotal+testTotal
                totalDetails = {
                    'noOfDays': noOfDays,
                    'roomCharge': roomCharge,
                    'medicineTotal': medicineTotal,
                    'testTotal': testTotal,
                    'total': total
                }
                return render_template('fetch_bill.html', patientid=patientid, patient_data=patient_data, dateOfDischarged=dateOfDischarged, tests=tests, medicines=medicines, totalDetails=totalDetails)
        else:
            flash("Please enter a valid Patient Id", 'danger')
    return render_template('issued_medicine.html', details=details)


#get medicine
@app.route("/getMedicine/<patientid>", methods=['GET', 'POST'])
def getMedicine(patientid):
    if not session.get("userName"):
        return redirect("/")
    medicines = Medicine.query.all()
    return render_template('add_medicine.html', medicines=medicines, patientid=patientid)

#get tests
@app.route("/getTest/<patientid>", methods=['GET', 'POST'])
def getTest(patientid):
    if not session.get("userName"):
        return redirect("/")
    tests = Test.query.all()
    return render_template('add_diagnostics.html', tests=tests, patientid=patientid)

#Add medicine
@app.route("/addMedicine/<patientid>", methods=['GET', 'POST'])
def addMedicine(patientid):
    #patient = Patient.query.filter_by(id=patientid).first()
    if not session.get("userName"):
        return redirect("/")
    if request.method == "POST":
        medicineId = request.form.get('medicine')
        quantityIssued = int(request.form.get('quantityIssued'))
        if medicineId:
            medicine = Medicine.query.filter_by(id=medicineId).first()
            #avaialablity checkup
            if medicine.available > quantityIssued:
                medicine.available -= quantityIssued
                availability = "Yes"
            else:
                availability = "No"
                flash("Sorry, insufficient medicine", "danger")
                return redirect(url_for('getMedicine', patientid=patientid))
            bill = billing.insert().values(patientId=patientid, medicineId=medicineId,
                                           pieces=quantityIssued, cost=quantityIssued * medicine.cost)
            db.session.execute(bill)
            db.session.commit()
            flash("Medicine Issued", "success")
            return redirect(url_for('getMedicine', patientid=patientid))
    flash("Get request on add medicine", "danger")
    return render_template('add_medicine.html')


# Add tests
@app.route("/addTest/<patientid>", methods=['GET', 'POST'])
def addTest(patientid):
    #patient = Patient.query.filter_by(id=patientid).first()
    if not session.get("userName"):
        return redirect("/")
    if request.method == "POST":
        testId = request.form.get('test')
        if testId:
            test = Test.query.filter_by(id=testId).first()
            bill = billing.insert().values(patientId=patientid, testId=testId,
                                           cost=test.cost)
            db.session.execute(bill)
            db.session.commit()
            flash("test Issued", "success")
            return redirect(url_for('getTest', patientid=patientid))
    flash("Get request on add test", "danger")
    return render_template('add_diagnostics.html')

#Billing 
@app.route('/bill', methods=['GET', 'POST'])
def fetchBill():
    if not session.get("userName"):
        return redirect('/')
    return render_template('fetch_bill.html')

#discharge patient
@app.route('/discharge_patient/<patientid>', methods=['POST'])
def dischargePatient(patientid):
    if request.method == 'POST':
        patient = Patient.query.filter_by(id=patientid).first()
        patient.status = 'Discharged'
        db.session.commit()
        flash('Patient is successfully discharged','success')
        return redirect("/home")
# Login and Logout Feature

@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get("userName"):
        return redirect("/home")
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        # fetch the user object from entered userid
        user = User.query.filter_by(userName=userid).first()
        # comparing if user is their with entered userid then compare its password
        if user and user.password == password:
            role = Role.query.filter_by(id=user.roleId).first().role
            session["userName"] = user.userName
            session['role'] = role
            flash("You are logged in!!", "success")
            return render_template("create_patient.html")
        else:
            flash("You are invalid user!!", "danger")
    return render_template("index.html")


@app.route("/logout")
def logout():
    session['userName'] = False
    session['role'] = False
    return redirect('/')

#######################################################


@app.cli.command('init_db')
def init_db():
    db.drop_all()
    db.create_all()

    #insert roles
    roles = {
        1: "Admin", 2: "Pharmacist", 3: "Diagnostic"
    }
    for x, y in roles.items():
        role = Role(id=x, role=y)
        db.session.add(role)
    db.session.commit()

    #insert users
    user1 = User(userName="RE16153100", password="casestudy@12", roleId=1)
    user2 = User(userName="PS16153100", password="12345", roleId=2)
    user3 = User(userName="DS16153100", password="12345", roleId=3)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

    #insert tests
    tests = [(1, 'BP', 250), (2, 'ECG', 500), (3, 'X-Ray', 150)]
    for x in tests:
        test = Test(id=x[0], name=x[1], cost=x[2])
        db.session.add(test)

    medicines = [(1, 'M1', 250, 2), (2, 'M2', 100, 10), (3, 'M3', 150, 30)]
    for x in medicines:
        medicine = Medicine(id=x[0], name=x[1], available=x[2], cost=x[3])
        db.session.add(medicine)
    db.session.commit()
