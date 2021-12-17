from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators, IntegerField, TextAreaField
from wtforms.fields.html5 import EmailField

from wtforms.validators import InputRequired, Email, Length, ValidationError, Optional
from ContactsSafe.database import * #imports ALL data from database.py (including all tables)

class LoginForm(FlaskForm):

  #custom validator to check if user indeed exists in database
  def validate_username(form, field): 
    validated=True 
    x = User.query.filter_by(username=form.name.data).first() 

    if x is None:
      form.username.errors.append["No such user! Check your username and try again!"]
      validated=False

  #Inputs required in the form below, along with validators
  name = StringField("Username", validators=[InputRequired()],  render_kw={"placeholder": "Username"})
  email = EmailField("Email", validators = [Email(), InputRequired()],  render_kw={"placeholder": "Email-Address"})
  remember_me = BooleanField('Remember Me')
  password = PasswordField("Password", validators = [InputRequired()],  render_kw={"placeholder": "Password"}, id="pw")

#create
class RegistrationForm(FlaskForm):

  #custom validator to ensure that user logs in with a unique username
  def validate_username(form, field):
    validated = True 
    x = User.query.filter_by(username = form.name.data).first()

    if x:
      form.username.errors.append("Already a user using this username! Try again")
      validated = False

    return validated
    
  #custom validator to ensure that user registers with a unique email
  def validate_email(form, field):
    validated = True
    x = User.query.filter_by(email = form.email.data).first()
    
    if x:
      form.email.errors.append("That email is already in use! Try again")
      validated = False
    
    return validated

  name = StringField("Username", validators=[InputRequired()], render_kw={"placeholder": "Username"})	
  email = EmailField("Email", validators = [Email(), InputRequired()], render_kw={"placeholder": "Email-Address"})
  password = PasswordField("New password", validators = [
  validators.DataRequired(),
  validators.EqualTo('confirm', message='Passwords must match'), InputRequired()], render_kw={"placeholder": "Password"}, id="pw")
  confirm = PasswordField('Repeat Password', validators=[InputRequired()], render_kw={"placeholder": "Confirm Password"}, id="pw")
  accept_toc = BooleanField('I accept the Terms of Conditions', [validators.DataRequired()])

class Add_contacts(FlaskForm):
	name = StringField('Contact Name', validators=[InputRequired()], render_kw={"placeholder": "Name *"})

	nickname = StringField('Nickname', render_kw={"placeholder": "Nickname"})

	homephone = StringField('Home phone number', validators = [Optional(), Length(min=8, max=14, message='Standard phone numbers have a length ranging from 8 to 14 characters. Your phone number length does not fall withing that range. Please try again.')], render_kw={"placeholder": "Home Phone"})

	#length is validated as such because phone numbers worldwide range from 8 to 14 characters
	personal = StringField('Personal phone number', validators = [InputRequired(), Length(min=8, max=14, message='Standard personal phone numbers have a length ranging from 8 to 14 characters. Your phone number length does not fall withing that range. Please try again.')], render_kw={"placeholder": "Personal Phone Number *"})

	work = StringField('Work phone number', validators = [Optional(), Length(min=8, max=14, message='Standard work phone numbers have a length ranging from 8 to 14 characters. Your phone number length does not fall withing that range. Please try again.')], render_kw={"placeholder": "Work Phone"})

	email = EmailField('Email', validators = [Optional(), Email()], render_kw={"placeholder": "Email-Address"})

	address = StringField('Address', render_kw={"placeholder": "Home Address"})

	work_info = TextAreaField('Work information', render_kw={"placeholder": "Work Information"})

	relationship = StringField('Relationship', render_kw={"placeholder": "Relationship"})

	additional_notes = TextAreaField('Additional Notes', render_kw={"placeholder": "Additional notes"})
  
  
  
