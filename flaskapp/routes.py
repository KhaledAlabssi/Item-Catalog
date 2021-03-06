import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, NewCompanyForm
from flaskapp.models import User, Company, Auto
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/catalog/")
def home():
    company = Company.query.all()
    return render_template('catalog.html', company=company)


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
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/company/new/", methods=['Get', 'Post'])
@login_required
def newCompany():
    form = NewCompanyForm()
    if form.validate_on_submit():
        company = Company(name=form.name.data, user=current_user)
        db.session.add(company)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('newCompany.html', form=form)


@app.route("/company/<int:company_id>/edit/", methods=["GET", "POST"])
@login_required
def editCompany(company_id):
    company = Company.query.get_or_404(company_id)
    if company.user != current_user:
        abort(403)
    form = NewCompanyForm()
    if form.validate_on_submit():
        company.name = form.name.data
    
        db.session.commit()
        flash('Your Brand has been updated!', 'success')
        return redirect(url_for('home'))
    return render_template("editCompany.html", form=form, company_id=company_id, company=company)


@app.route("/company/<int:company_id>/delete/", methods=["GET", "POST"])
@login_required
def deleteCompany(company_id):
    company = Company.query.get_or_404(company_id)
    if company.user != current_user:
        abort(403)
    db.session.delete(company)
    db.session.commit()
    flash('Your Brand has been deleted!', 'success')
    return redirect(url_for('home'))




@app.route("/company/<int:company_id>", methods=["GET", "POST"])
@login_required
# @app.route("/company/<int:company_id>/autos>")
def showAutos(company_id):
    return render_template("publicAutos.html", company_id=company_id)


@app.route("/company/<int:company_id>/autos/new/", methods=["GET", "POST"])
@login_required
def newAutos(company_id):
    return render_template("newAuto.html", company_id=company_id)


@app.route("/company/<int:company_id>/autos/<int:car_id>/edit/", methods=["GET", "POST"])
@login_required
def editAuto(company_id, car_id):
    return render_template("editAutos.html", company_id=company_id, car_id=car_id)


@app.route("/company/<int:company_id>/autos/<int:car_id>/delete/", methods=["GET", "POST"])
@login_required
def deleteAuto(company_id, car_id):
    return render_template("deleteAuto.html", company_id=company_id, car_id=car_id)