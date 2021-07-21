from wtforms import Form, BooleanField, StringField, PasswordField, validators

#creating the registration form logic using wtforms for admin
class RegistrationForm(Form):
    usertype = StringField('Register as Customer/Reseller', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()]) #validators.Email() should raise an error if the email input is not an email.
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

#creating the login form logic using wtforms for admin 
class Login(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Your Password', [validators.DataRequired()])
