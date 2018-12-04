import os

from flask import Flask, session, json, current_app, redirect, url_for
from flask_assets import Environment
from flask_compress import Compress
from flask_login import LoginManager
from flask_mail import Mail
from flask_rq import RQ
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect
from flask_moment import Moment
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_babel import Babel, lazy_gettext as _l
# from oauth2client.contrib.flask_util import UserOAuth2


# from app.assets import app_css, app_js, vendor_css, vendor_js
from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()
csrf = CsrfProtect()
compress = Compress()
moment = Moment()
babel = Babel()
# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    app.config['OAUTH_CREDENTIALS'] = {
        'google': {
            'id': '767868202462-3v28oqcun0fnd0vc89uh7in4mbi7fg4o.apps.googleusercontent.com',
            'secret': 'KfvqdFDqYYn9hXDFeC3BmImD'
        },
        'facebook': {
            'id': '340669703151082',
            'secret': '9d1b868c34d034b780e9da3af9213653'
        },
        'twitter': {
            'id': 'NzD4SB1S9Ulod1k1cqZGH5g6J ',
            'secret': 'CLXzCpbe0NxY8mOzgBtgRNWJjltJth2urwR7EkBzr365EUNEWO'
        }
    }

    config[config_name].init_app(app)

    # Set up extensions
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    compress.init_app(app)
    moment.init_app(app)
    RQ(app)

    babel.init_app(app)

    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    patch_request_class(app)

    # Register Jinja template functions
    from .utils import register_template_utils
    register_template_utils(app)

    # Set up asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/styles', 'assets/scripts']
    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))
    assets_env.url_expire = True

    # assets_env.register('app_css', app_css)
    # assets_env.register('app_js', app_js)
    # assets_env.register('vendor_css', vendor_css)
    # assets_env.register('vendor_js', vendor_js)
    # assets_env.register('skye_css', vendor_css)
    # assets_env.register('skye_js', vendor_js)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        SSLify(app)

    # # Create app blueprints

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # customer blue_print

    from .customer import customer as customer_blueprint
    app.register_blueprint(customer_blueprint, url_prefix='/customer')

    # home blue_print

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    # publisher blue_print

    from .publisher import publisher as publisher_blueprint
    app.register_blueprint(publisher_blueprint, url_prefix='/publisher')

    # home blue_print

    from .auth import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .social import social as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/social_login')

    # csrf.exempt(api_blueprint)

    return app
