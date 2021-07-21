from shop import db
from datetime import datetime
import json

#creating a user model to the database, this will create a table with 
#the following columns, which can be used to store corresponding data.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)

#This function returns a printable representation of the User model object.
    def __repr__(self):
        return '<User %r>' % self.username



db.create_all() #used to create user model in the database.
    

