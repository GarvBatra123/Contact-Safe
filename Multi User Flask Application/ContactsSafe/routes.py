from ContactsSafe import app
from ContactsSafe import db
from flask import render_template, request, flash, redirect, url_for
from ContactsSafe.forms import LoginForm, RegistrationForm, Add_contacts
from ContactsSafe.database import User, UserAddContacts
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
import datetime, calendar, json, os

# THIS FUNCTION ALLOWS US TO USE PYTHON MODULES IN WEBPAGES THROUGH JINJA2 TEMPLATING
@app.context_processor
def handle_context():
	return dict(os=os)


@app.errorhandler(404)
def error404(e):
	return render_template("error_404.html")


@app.route('/aboutUs')
def aboutUs():
	return render_template("aboutUs.html")


@app.route('/')
def landingpage():
	return render_template("landingPage.html")

#following route leads to addcontacts.html which contains a form, which enables user to add a contact to his savedcontacts
@app.route('/addcontacts', methods=['GET', 'POST'])
@login_required #ensures user is logged in before he can access this route
def addcontacts():
  form = Add_contacts()
  if request.method == 'POST':
    if form.validate_on_submit():
      contact = UserAddContacts(name = form.name.data, nickname = form.nickname.data, homephone = form.homephone.data, personal = form.personal.data, work = form.work.data, email = form.email.data, address = form.address.data, work_info = form.work_info.data, relationship = form.relationship.data, additional_notes = form.additional_notes.data, owner_id=current_user.id) #uses data taken from form to create row
      db.session.add(contact) #adds row to db file
      db.session.commit()
      flash('User added', category = "success")
      return redirect(url_for('index'))
    else:
      flash(format(form.errors))
  return render_template("addcontacts.html", form=form,  errors = form.errors)


@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      user = User.query.filter_by(username=form.name.data).first() 
      if user is None:
        flash("No such user", category="danger")
        return redirect(url_for('login')) 

      elif user.check_password(form.password.data):
        flash("Wrong password", category="danger")
        return redirect(url_for('login')) 
      
      else:
        login_user(user, remember=form.remember_me.data)
        nextpage = request.args.get("next")
        if not nextpage or url_parse(nextpage).netloc != "":
          nextpage = url_for('index') 

        return redirect(nextpage)

  return render_template("login.html", form=form) 


@app.route("/profilePage")
@login_required
def ProfilePage():
  return render_template("ProfilePage.html")


@app.route("/logout")
@login_required
def logout():
	logout_user() #in-built function from Flask-Login alowing user to logout
	flash("You are logged out!", category="success") 
	return redirect(url_for("login"))


@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm(request.form) #form used on register page called 'RegistrationForm'

  if request.method == 'POST': #if person using POST request method (i.e. trying to submit the form)

    if form.validate_on_submit(): #if all validators defined in forms (in forms.py) are satisfied

      user = User(username=form.name.data, email=form.email.data, password=form.password.data) #create row called user with data from form submitted by user
      db.session.add(user) #add this row to db
      print("user", user)
      db.session.commit() 
      flash('Thanks for registering')
      return redirect(url_for('login'))
    else:
      flash(format(form.errors)) #returns a dictionary of the errors
  return render_template('register.html', form=form, errors = form.errors)

@app.route('/savedcontacts')
@login_required
def index():
  Contacts = UserAddContacts.query.filter_by(owner_id=current_user.id).order_by(UserAddContacts.name).all()
  return render_template('savedcontacts.html', Contacts=Contacts)


@app.route("/PrivacyPolicy")
def PrivacyPolicy():
	return render_template("privacypolicy.html")

@app.route("/delete/<int:contact_id>")
def delete(contact_id):
  tobedeleted = UserAddContacts.query.filter_by(owner_id=current_user.id, id = contact_id).first() #returns rows of contact data that belong to current user
  if tobedeleted: 
    db.session.delete(tobedeleted) #delete that particular row of contact data
    db.session.commit()
    flash("Contact deleted successfully", category="success")
  else:
    flash("No such task", category="danger")
  return redirect(url_for('index'))

@app.route("/update/<int:contact_id>", methods=['GET', 'POST'])
@login_required
def updatetask(contact_id):
  form = Add_contacts()
  if request.method == 'GET':
    if contact_id:
      contact = UserAddContacts.query.filter_by(owner_id=current_user.id, id = contact_id).first()
      form.name.data = contact.name
      form.nickname.data = contact.nickname 
      form.homephone.data = contact.homephone
      form.personal.data = contact.personal
      form.work.data = contact.work
      form.email.data = contact.email
      form.address.data = contact.address
      form.work_info.data = contact.work_info
      form.relationship.data = contact.relationship
      form.additional_notes.data = contact.additional_notes
    else:
      flash('No such record')
  else:
    if form.validate_on_submit():
      contact = UserAddContacts.query.filter_by(owner_id=current_user.id, id = contact_id).first()
      contact.name = form.name.data  
      contact.nickname = form.nickname.data   
      contact.homephone = form.homephone.data  
      contact.personal = form.personal.data  
      contact.email = form.email.data
      contact.address = form.address.data  
      contact.work_info=form.work_info.data  
      contact.relationship = form.relationship.data  
      contact.additional_notes = form.additional_notes.data 
      db.session.commit()
      flash("Contact updated successfully", category="success")
      return redirect(url_for("index"))
    else:
      flash("Failure to submit form {}".format(form.errors))
  return render_template('addcontacts.html', form=form)

