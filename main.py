from flask import Flask, request, render_template, redirect, url_for


app=Flask("__name__")


@app.route('/home',methods=['GET','POST'])
def log1():	

	return render_template('crte_patient.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('log1'))
    return render_template('index.html', error=error)
app.run(debug=True)    
