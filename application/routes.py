from flask import Flask, render_template, flash, session, redirect, request
from application import app
from application.forms import LoginForm
from application.models import userStore


@app.route('/home',methods=['GET','POST'])
def home():	
    if not session.get('userName'):
        return redirect('/')
    return render_template('create_patient.html')


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
            return render_template("create_patient.html", login= True)
        else:
            flash("You are invalid user!!", "danger")
    return render_template("index.html")
 
@app.route("/logout")
def logout():
    session['userName'] = False
    return redirect('/')