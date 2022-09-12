from wtforms import StringField, TextAreaField, PasswordField, SubmitField, validators, Form
from flask_wtf.file import FileRequired, FileAllowed, FileField


class CustomerRegisterForm(Form):
    name= StringField('Name')
    username= StringField('Username')
    email= StringField('Email', [validators.Email(), validators.DataRequired()])
    password= PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Both password must match.')])
    confirm= PasswordField('Repeat Password:', [validators.DataRequired()])
    country= StringField('Country', [validators.DataRequired()])
    state= StringField('State', [validators.DataRequired()])
    city= StringField('City', [validators.DataRequired()])
    contact= StringField('Contact', [validators.DataRequired()])
    address= StringField('Address', [validators.DataRequired()])
    zipcode= StringField('Zipcode', [validators.DataRequired()])

    profile= FileField('Profile', validators=[FileAllowed(['jpg','png','jpeg','gif'],'Image only, PLEASE!')])
    submit= SubmitField('Register')