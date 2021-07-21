from shop import db

#customer model to create a table for reseller with the following columns
class Reseller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    country = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), unique=False, nullable=False)
    contact = db.Column(db.String(30), unique=True, nullable=False)
    address = db.Column(db.String(30), unique=False, nullable=False)
    city = db.Column(db.String(30), unique=False, nullable=False)
    zipcode = db.Column(db.String(30), unique=False, nullable=False)

#This function returns a printable representation of the Reseller model object.
    def __repr__(self):
        return '<Reseller %r>' % self.username



db.create_all()  #craates the table on the database.
