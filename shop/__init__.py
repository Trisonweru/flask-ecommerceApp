from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os

basedir=os.path.abspath(os.path.dirname(__file__)) #gets the base direcotry to our app.
app = Flask(__name__) #creates a flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db' #configure myshop database
app.config['SECRET_KEY']='thisissupposedtobemysecret' #configure a secret key
app.config['UPLOADED_PHOTOS_DEST']=os.path.join(basedir, "static/images") #configures the destitanation for uploaded image files
#requrement configugurations for whenever you would like to upload images 
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app) 

db = SQLAlchemy(app)# creates a database
bcrypt=Bcrypt(app)# instatiate the bcrypt to help in hashing of passwords

from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes
from shop.reseller import routes