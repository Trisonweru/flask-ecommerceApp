from flask import render_template, url_for, session, request, redirect, flash

from shop import app, db, bcrypt

from .forms import CustomerRegistration, Login
from .models import Customer

import os
#register a customer route
@app.route("/registercustomer", methods=["POST", "GET"])
def registercustomer():
    form=CustomerRegistration(request.form) # we instaciate the CustomerRegistration class from our forms.py file
    if request.method == 'POST' and form.validate(): # if the reuest method is post 
        hashedpass=bcrypt.generate_password_hash(form.password.data)#encrypt the password
        #create a customer
        customer = Customer(name=form.name.data, username=form.username.data, email=form.email.data, password=hashedpass,
        country=form.country.data, city=form.city.data, contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data )
        db.session.add(customer) #save the customer to the database
        db.session.commit() #commit the process for the actual save.
        flash(f'Welcome {form.username.data}. Thank you for registering.', 'success')
        return redirect(url_for("customerlogin"))
    return render_template("customer/customer.html", form=form)
#responsible for customer login
@app.route("/customerlogin", methods=["POST", "GET"])
def customerlogin():
    form=Login(request.form) # create an instace of the login form
    if request.method == 'POST' and form.validate(): #if the method is post and the form validates
        customer=Customer.query.filter_by(email=form.email.data).first()#find the customer in the database
        if customer and bcrypt.check_password_hash(customer.password, form.password.data): #if the cutomer exists and the password hash matches the hash fro entered password
            session['email']=form.email.data #add the user to seesion
            flash(f'Welcome {form.email.data}. You are now logged in.', 'success')
            return redirect(request.args.get('next') or url_for('cart'))
        else:
            flash(f'Wrong password/email. Please try again.', 'danger')
    return render_template("customer/login.html", form=form, title="Login page")


