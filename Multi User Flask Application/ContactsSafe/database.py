from ContactsSafe import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from ContactsSafe import login

#creates table User 
class User(db.Model, UserMixin):
  #columns in the table
  id = db.Column(db.Integer, primary_key = True, autoincrement=True)
  username = db.Column(db.String(50), unique = True)
  password = db.Column(db.String(256))
  email = db.Column(db.String(120), index=True, unique=True)
  date_created = db.Column(db.DateTime, default=datetime.now())
  contacts = db.relationship('UserAddContacts', backref='contact_owner', lazy = "joined", uselist=False) #links User table to UserAddContacts table

  def __repr__(self):
    return "<User {}>".format(self.username)

  #ensures that passwords are hashed and not visible to website owners
  def set_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)

#creates table UserAddContacts
class UserAddContacts(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20))
  nickname = db.Column(db.String(20))
  homephone = db.Column(db.Integer)
  personal = db.Column(db.Integer)
  work = db.Column(db.Integer)
  email = db.Column(db.String(120))
  address = db.Column(db.String(500))
  work_info = db.Column(db.String(700))
  relationship = db.Column(db.String(60))
  additional_notes = db.Column(db.String(800))
  owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

if __name__ == '__main__':
  db.create_all()
  

@login.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

