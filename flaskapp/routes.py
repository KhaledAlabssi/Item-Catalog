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


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/register")
def register():
    return render_template('register.html')


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