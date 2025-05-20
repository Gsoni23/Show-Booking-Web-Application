from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User 
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login', methods= ['GET','POST'])
def Login():
    
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged In",category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("User don\'t exist", category='error')

    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('auth.Login'))

@auth.route('/signup', methods = ['get','post'])
def Signup():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user:
            flash("Email already exists", category='error')
        elif len(email) < 4:
            flash("Email length error", category= 'error')
        elif len(password) < 5:
            flash("Password is too short", category='error')
        else:
            new_user = User(email = email, name = name, password = generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account successfully created", category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home')) 


    return render_template("signup.html", user = current_user)    