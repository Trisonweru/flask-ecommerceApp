#From here we will create different routes to the administration pages
from flask import render_template, url_for, session, request, redirect, flash

from shop import app, db, bcrypt

from .forms import RegistrationForm, Login #importing the registration and login classes from the forms file.
from .models import User # we will also use User model from models to query for data
from shop.products.models import AddProduct #we again import AddProduct model because we will query the db and display products for admin
from shop.products.models import CustomerOrder #we again us the custome model to query for customers 

import os

#route for the admins page
@app.route("/admin")
def admin():
    #if the user is not in session we dont display the this route
    if 'email' not in session:
        flash(f'Please login to access this route.', 'danger')
        return redirect(url_for('login'))
    #otherwise query all the products and pass it to our index.html template for display
    products=AddProduct.query.all()
    return render_template("admin/index.html", title="Admin Page", products=products)

#route to register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form) # we instatiate our registration form class which we pass to our template register.html for display
    if request.method == 'POST' and form.validate(): #check if request is post thn we save the data to the database
        #encrypt the user entered password using bcrypt
        hashedpass=bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashedpass)
        db.session.add(user)
        #commit the user to the database
        db.session.commit()
        flash(f'Welcome {form.username.data}. Thank you for registering.', 'success')
        return redirect(url_for('home'))
    return render_template('admin/register.html', form=form, title="Registration page")

#route to login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form=Login(request.form) #creating an instace of login class and pass it to our login.html template for display
    if request.method == 'POST' and form.validate(): #check if method is post and no validation errors then autheticate the user
        user=User.query.filter_by(email=form.email.data).first() # we fetch the user with the input email
        #check the hashed password against the user entered password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #create a session for the user if the password is correct
            session['email']=form.email.data
            flash(f'Welcome {form.email.data}. You are now logged in.', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash(f'Wrong password/email. Please try again.', 'danger') #if login is not succesful
    return render_template("admin/login.html", form=form, title="Login page")

#a function to display orders
@app.route('/getorders', methods=["POST", "GET"])
def getorders():
    #checks the user if in session, while true we get all orders from th database for display
    if 'email' not in session:
        flash(f'Please login to access this route.', 'danger')
    orders=CustomerOrder.query.all() #query the orders and pass them to orders.html component
    #print(type(orders))        
    return render_template("admin/orders.html", orders=orders, title="Orders")


