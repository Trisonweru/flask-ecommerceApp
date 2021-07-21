from flask import render_template, url_for, session, request, redirect, flash

from shop import app, db, bcrypt
from shop.products.models import AddProduct

from .forms import ResellerRegistration, Login
from .models import Reseller

import os

#responsible for the reseller routing
@app.route("/reseller", methods=['GET', 'POST'])
def reseller():
    if 'email' not in session: #checknif user is logged in, if not we redirect them to ressler login
        flash(f'Please login to access this route.', 'info')
        return redirect(url_for('resellerlogin'))
    products=AddProduct.query.filter(AddProduct.stock > 0) #else get the products if the the products stock is greater tha 0
    return render_template('reseller/reseller.html', products=products) #pass the products to the resseller.html template for displaying

#register a reseller route
@app.route("/registerreseller", methods=["POST", "GET"])
def registerreseller():
    form=ResellerRegistration(request.form) #instatiate the form class 
    if request.method == 'POST' and form.validate(): #if the request method is get and form validate without any errors
        hashedpass=bcrypt.generate_password_hash(form.password.data) #hash the password
        reseller = Reseller(name=form.name.data, username=form.username.data, email=form.email.data, password=hashedpass,
        country=form.country.data, city=form.city.data, contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data )
        db.session.add(reseller) #add the user reseller details to the database
        db.session.commit() # and commit the changes
        flash(f'Welcome {form.username.data}. Thank you for registering.', 'success')
        return redirect(url_for("resellerlogin"))
    return render_template("reseller/register.html", form=form, title="Registration page")

@app.route("/resellerlogin", methods=["POST", "GET"])
def resellerlogin():
    form=Login(request.form) #instatiate the Login from class
    if request.method == 'POST' and form.validate(): #if request is Post and form validates without any errors
        reseller=Reseller.query.filter_by(email=form.email.data).first() #get the resseler with the email from form input
        if reseller and bcrypt.check_password_hash(reseller.password, form.password.data): #if the resseler with the email is available in the database, check if the hashed password and entered password matches
            session['email']=form.email.data #if true, add the resseler email to session
            flash(f'Welcome {form.email.data}. You are now logged in.', 'success')
            return redirect(request.args.get('next') or url_for('reseller'))
        else:
            flash(f'Wrong password/email. Please try again.', 'danger')
    return render_template("reseller/login.html", form=form, title="Login page")
