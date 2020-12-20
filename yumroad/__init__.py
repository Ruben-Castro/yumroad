from flask import Flask
from yumroad.config import configurations
from yumroad.extensions import db, csrf
from yumroad.blueprints.products import products


def create_app(environment_name="dev"):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])
    db.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(products, url_prefix='/product')
    return app
