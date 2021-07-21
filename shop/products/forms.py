from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField

#creates the form using wtforms to collect the datails about th product with the following fields
class AddProducts(Form):
    name=StringField("Name", [validators.DataRequired()])
    price=DecimalField("Price",[validators.DataRequired()] )
    discount=IntegerField("Discount", default=0 )
    stock=IntegerField("Stock",[validators.DataRequired()] )
    location=StringField("Location", [validators.DataRequired()])
    description=TextAreaField("Description",  [validators.DataRequired()])
    colors=TextAreaField('Colors', [validators.DataRequired()])

    image_1=FileField("Image 1", validators=[FileRequired(), FileAllowed(['jpg', 'gif', 'jpeg', 'png', 'image only please'])])
    image_2=FileField("Image 2", validators=[FileRequired(), FileAllowed(['jpg', 'gif', 'jpeg', 'png', 'image only please'])])
    image_3=FileField("Image 3", validators=[FileRequired(), FileAllowed(['jpg', 'gif', 'jpeg', 'png',  'image only please'])])