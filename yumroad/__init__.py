from flask import Flask
from yumroad.config import configurations
from yumroad.extensions import db, csrf, login_manager
from yumroad.blueprints.products import products
from yumroad.blueprints.users import user_bp
import yumroad.models

def create_app(environment_name="dev"):
    app = Flask(__name__)

    app.config.from_object(configurations[environment_name])
    db.init_app(app)
    csrf.init_app(app)
    
    login_manager.init_app(app)

    app.register_blueprint(products, url_prefix='/product')
    app.register_blueprint(user_bp)
    return app
