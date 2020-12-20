from yumroad.extensions import db
from sqlalchemy.orm import validates


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(120), nullable=True)

    @validates('name')
    def validate_name(self, key, name):
        print(len(name.strip()))
        if (len(name.strip()) <= 3):

            raise ValueError("Needs to have a real name")

        return name
