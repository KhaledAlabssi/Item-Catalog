import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm
from flaskapp.models import User, Company, Auto
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/catalog/")
def home():
    return render_template('catalog.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, emai=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/company/new/")
def newCompany():
    return render_template('newCompany.html')


@app.route("/company/<int:company_id>/edit/")
def editCompany(company_id):
    return render_template("editCompany.html", company_id=company_id)


@app.route("/company/<int:company_id>/delete/")
def deleteCompany(company_id):
    return render_template("deleteCompany.html", company_id=company_id)


@app.route("/company/<int:company_id>")
# @app.route("/company/<int:company_id>/autos>")
def showAutos(company_id):
    return render_template("publicAutos.html", company_id=company_id)


@app.route("/company/<int:company_id>/autos/new/")
def newAutos(company_id):
    return render_template("newAutos.html", company_id=company_id)


@app.route("/company/<int:company_id>/autos/<int:car_id>/edit/")
def editAuto(company_id, car_id):
    return render_template("editAutos.html", company_id=company_id, car_id=car_id)


@app.route("/company/<int:company_id>/autos/<int:car_id>/delete/")
def deleteAuto(company_id, car_id):
    return render_template("deleteAuto.html", company_id=company_id, car_id=car_id)