# _*_ coding: utf-8 _*_

"""
Change Password
"""

import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from werkzeug import security

from app import app, app_db
from utility.consts import RE_PWD

from ...paths import PATH_LOGOUT

TAG = "user-password"


def layout(pathname, search):
    """
    layout of card
    """
    # define components
    c_pwd = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-pwd", type="password"),
        dbc.Label("Current Password:", html_for=f"id-{TAG}-pwd"),
    ])
    c_pwd1 = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-pwd1", type="password"),
        dbc.Label("New Password:", html_for=f"id-{TAG}-pwd1"),
    ])
    c_pwd2 = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-pwd2", type="password"),
        dbc.Label("Confirm Password:", html_for=f"id-{TAG}-pwd2"),
    ])

    # define components
    c_fb = html.Div(id=f"id-{TAG}-fb", className="text-danger text-center")
    c_button = dbc.Button("Update Password", id=f"id-{TAG}-button", class_name="w-100")

    # return result
    return dbc.Card(children=[
        html.Div("Change Password:", className="border-bottom p-4"),
        dbc.Row(children=[
            dbc.Col(c_pwd, width=12, md=4, class_name=None),
            dbc.Col(c_pwd1, width=12, md=4, class_name="mt-2 mt-md-0"),
            dbc.Col(c_pwd2, width=12, md=4, class_name="mt-2 mt-md-0"),
            # change line
            dbc.Col(c_fb, width=12, md={"size": 4, "order": "last"}, class_name="mt-0 mt-md-4"),
            dbc.Col(c_button, width=12, md=4, class_name="mt-4 mt-md-4"),
        ], align="center", class_name="p-4"),
        dbc.Modal(children=[
            dbc.ModalHeader(dbc.ModalTitle("Update Success"), close_button=False),
            dbc.ModalBody("The password was updated successfully"),
            dbc.ModalFooter(dbc.Button("Go back to re-login", href=PATH_LOGOUT, class_name="ms-auto")),
        ], id=f"id-{TAG}-modal", backdrop="static", is_open=False),
    ], class_name="mb-4")


@app.callback([
    Output(f"id-{TAG}-fb", "children"),
    Output(f"id-{TAG}-modal", "is_open"),
], [
    Input(f"id-{TAG}-button", "n_clicks"),
    State(f"id-{TAG}-pwd", "value"),
    State(f"id-{TAG}-pwd1", "value"),
    State(f"id-{TAG}-pwd2", "value"),
], prevent_initial_call=True)
def _button_click(n_clicks, pwd, pwd1, pwd2):
    user = flask_login.current_user

    # check data
    if not security.check_password_hash(user.pwd, pwd or ""):
        return "Current password is wrong", False

    # check data
    if (not pwd1) or (len(pwd1) < 6):
        return "Password is too short", None
    if not RE_PWD.match(pwd1):
        return "Must contain numbers and letters", None
    if (not pwd2) or (pwd2 != pwd1):
        return "Passwords are inconsistent", None

    # update data
    user.pwd = security.generate_password_hash(pwd1)

    # commit data
    app_db.session.merge(user)
    app_db.session.commit()

    # return result
    return None, True