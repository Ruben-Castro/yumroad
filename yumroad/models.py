from yumroad.extensions import db
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash
from flask_login import UserMixin


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)

    creator = db.relationship("User", uselist=False, back_populates="products")
    store = db.relationship("Store", uselist=False, back_populates="products")

    @validates('name')
    def validate_name(self, key, name):
        print(len(name.strip()))
        if (len(name.strip()) <= 3):
            raise ValueError("Needs to have a real name")

        return name


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    products = db.relationship("Product", back_populates="creator")
    store = db.relationship("Store", uselist=False, back_populates="user")

    @classmethod
    def create(cls, email, password):
        hashed_password = generate_password_hash(password)
        return User(email=email.lower().strip(), password=hashed_password)


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship("User", uselist=False, back_populates="store")
    products = db.relationship("Product", back_populates="store")

    @validates('name')
    def validate_name(self, key, name):
        print(len(name.strip()))
        if (len(name.strip()) <= 3):
            raise ValueError("Needs to have a real name")

        return name
