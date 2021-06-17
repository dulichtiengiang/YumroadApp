
from itertools import product
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import validates
from yumroad.extensions import db
from flask_login import UserMixin

##########! PRODUCT MODEL ##############################
    # db.Index('idex_name_and_desc', 'name', 'description')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    price_cents = db.Column(db.Integer)
    picture_url = db.Column(db.Text)

    creator = db.relationship('User', uselist=False, back_populates='products')
    store = db.relationship('Store', uselist=False, back_populates='products')

    @validates('name')
    def validate_name(self, key, name):
        if len(name.strip()) <= 3:
            #! Error
            raise ValueError("Needs to have a real name")
        return name

##########! USER MODEL ##############################
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    store = db.relationship('Store', uselist=False, back_populates='user')
    products = db.relationship('Product', back_populates='creator') #! can say back_populates 'creator' by creator

    @classmethod #method of this class
    def create(cls, email, password):
        #method_create: User.create('test@gmail.com', 'examplepassword')
        #create hashed_password
        hashed_password = generate_password_hash(password)
        return User(email=email.lower().strip(), password=hashed_password)

##########! STORE MODEL ##############################
class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', uselist=False, back_populates='store')
    products = db.relationship('Product', back_populates='store')

    @validates('name')
    def validate_name(self, key, name):
        if len(name.strip()) <= 3:
            raise ValueError("Needs to have a real name")
        return name

