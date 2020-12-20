from flask_wtf import FlaskForm
from wtforms.fields import StringField

from wtforms.validators import Length

class ProductForm(FlaskForm):
    name = StringField('Name', [Length(min=4, max=60)])
    description = StringField('Description')
    
    

