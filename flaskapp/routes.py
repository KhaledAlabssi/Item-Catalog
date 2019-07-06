from flask import render_template
from flaskapp import app


@app.route("/")
@app.route("/catalog/")
def home():
    return render_template('catalog.html')


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