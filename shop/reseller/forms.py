from wtforms import Form, PasswordField, validators, SubmitField, StringField

#customer model to create a table for customers with the following columns
class ResellerRegistration(Form):
    name=StringField("Name:")
    username=StringField("Username:", [validators.DataRequired()])
    email = StringField('Email Address:', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password:', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password:')

    country=StringField("Country:", [validators.DataRequired()])
    city=StringField("City:", [validators.DataRequired()])
    contact=StringField("Contact:", [validators.DataRequired()])
    address=StringField("Address:", [validators.DataRequired()])
    zipcode=StringField("Zip code:", [validators.DataRequired()])

    submit=SubmitField("Register")
#login for customers
class Login(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Your Password', [validators.DataRequired()])

