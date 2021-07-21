from shop import db
from datetime import datetime
import json

#creates a table to store brands names in the db
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)


#creates a table to store categories names in the db
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

#creates a table to store the actual products details in the db
class AddProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price=db.Column(db.Numeric(10,2), nullable=False)
    discount=db.Column(db.Integer, default=0)
    stock=db.Column(db.Integer, nullable=False)
    location=db.Column(db.String(60), nullable=False)
    colors=db.Column(db.Text, nullable=False)
    description=db.Column(db.Text, nullable=False)
    pub_date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    brand_id=db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand=db.relationship('Brand', backref=db.backref('brands'))#, lazy='True'
   

    category_id=db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category=db.relationship('Category', backref=db.backref('categories'))#, lazy='True'
   
    image_1=db.Column(db.String(150), nullable=False, default="image.jpg")
    image_2=db.Column(db.String(150), nullable=False, default="image.jpg")
    image_3=db.Column(db.String(150), nullable=False, default="image.jpg")

    def __repr__(self):
        return '<AddProducts %r>' % self.name

#create a class to help save our orders as json object in the database
class JsonEncoderDict(db.TypeDecorator):
    impl = db.String()
    def process_bind_param(self, value, dialect):
        return json.dumps(value)
    def process_result_value(self, value, dialect):
        return json.loads(value)


#creating an order table to store customer orders with the following fields
class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(20), default="Pending", nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    orders=db.Column(JsonEncoderDict(128))

#This function returns a printable representation of the Order model object.
    def __repr__(self):
        return '<Order %r>' % self.invoice


db.create_all() #creates all the tables in the database