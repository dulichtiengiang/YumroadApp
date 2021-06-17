from flask import Flask
from flask.helpers import url_for
from werkzeug.utils import redirect

from yumroad.blueprints.products import bp_products
from yumroad.blueprints.users import bp_user
from yumroad.blueprints.stores import bp_store

from yumroad.config import configuration
from yumroad.extensions import (db, csrf, login_manager, migrate, mail)

def create_app(environment_name='dev'):
    app = Flask(__name__)

    app.config.from_object(configuration[environment_name])
    db .init_app(app=app)
    csrf.init_app(app=app)
    login_manager.init_app(app=app)
    migrate.init_app(app=app, db=db, render_as_batch=True)
    mail.init_app(app=app)

    app.register_blueprint(bp_products, url_prefix='/product')
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_store, url_prefix='/store')

    @app.route('/')
    def home():
        return redirect(url_for('store.index'))

    return app