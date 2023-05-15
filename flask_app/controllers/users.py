from flask import render_template, request, flash, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app import bcrypt


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods =['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/')
    data ={ 
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/trees')


@app.route('/login', methods = ['POST'])
def login():
    user = User.get_email(request.form)
    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/trees')

@app.route('/login/success')
def login_success():
    user = User.validate(request.form)
    if not user:
        return redirect('/login')

    session['user_id'] = user.id
    return redirect('/trees')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

