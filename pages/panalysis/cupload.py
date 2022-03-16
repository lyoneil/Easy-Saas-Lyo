# _*_ coding: utf-8 _*_

"""
upload component
"""

import base64

import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, dcc, html

from app import app, app_db
from config import config_dir_store
from ..paths import PATH_ANALYSIS, PATH_LOGIN

TAG = "analysis-upload"


def layout(pathname, search, class_name=None):
    """
    layout of component
    """
    # define components
    button = dbc.Button("Upload Data", class_name="w-75")
    args_up = {"accept": ".csv", "max_size": 1024 * 1024 * 10}

    # return result
    return html.Div(children=[
        html.A(id={"type": "id-address", "index": TAG}),
        dcc.Upload(button, id=f"id-{TAG}-upload", **args_up, className="text-center"),
    ], className=class_name)


@app.callback(
    Output({"type": "id-address", "index": TAG}, "href"),
    Input(f"id-{TAG}-upload", "contents"),
    State(f"id-{TAG}-upload", "filename"),
    prevent_initial_call=True,
)
def _button_click(contents, filename):
    # check user
    user = flask_login.current_user
    if not user.is_authenticated:
        return PATH_LOGIN

    # store data
    content_type, content_string = contents.split(",")
    with open(f"{config_dir_store}/{user.id}-{filename}", "wb") as file_out:
        file_out.write(base64.b64decode(content_string))

        # update user
        user.filename = filename

        # commit user
        app_db.session.merge(user)
        app_db.session.commit()

    # return result
    return f"{PATH_ANALYSIS}-table"
