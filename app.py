# _*_ coding: utf-8 _*_

"""
Dash
"""

import logging

import dash
import dash_bootstrap_components as dbc
from flask_login import LoginManager
from flask_mail import Mail
from flask_redis import FlaskRedis

from config import *
from model import User, app_db

# logging config
logging.basicConfig(format=config_log_format, level=logging.WARNING)

# create app
app = dash.Dash(
    __name__,
    server=True,
    title="Dash",
    compress=True,
    serve_locally=True,
    show_undo_redo=False,
    url_base_pathname="/",
    assets_folder="assets",
    update_title="Updating...",
    prevent_initial_callbacks=False,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        "default.css",
        dbc.icons.BOOTSTRAP,
        dbc.themes.BOOTSTRAP,
    ],
    meta_tags=[{
        "charset": "utf-8",
    }, {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1",
    }],
)

# create server
server = app.server
server.config.update(
    SECRET_KEY=config_app_secret_key,

    SQLALCHEMY_DATABASE_URI=config_database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,

    REDIS_URL=config_redis_uri,

    MAIL_SERVER=config_mail_server,
    MAIL_PORT=config_mail_port,
    MAIL_USERNAME=config_mail_username,
    MAIL_PASSWORD=config_mail_password,
    MAIL_DEFAULT_SENDER=config_mail_sender,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
)

# initial db
app_db.init_app(server)

# initial mail
app_mail = Mail(server)

# initial redis
app_redis = FlaskRedis(server)

# initial login_manager
login_manager = LoginManager(server)


# overwirte user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
