# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
import flask_login
from dash import html

from components import cbrand
from utility.paths import PATH_LOGIN

TAG = "analysis1"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    user = flask_login.current_user

    # define components
    class_link = "fs-6 text-white px-0 hover-success"
    navlink_list = [
        dbc.NavLink("Intros", id=f"id-{TAG}-intros", href="#", class_name=class_link),
        dbc.NavLink("Products", id=f"id-{TAG}-products", href="#", class_name=class_link),
        dbc.NavLink("Prices", id=f"id-{TAG}-prices", href="#", class_name=class_link),
        dbc.NavLink("Contacts", id=f"id-{TAG}-contacts", href="#", class_name=class_link),

        dbc.NavItem("HOME", className="small text-white-50 mt-4 mb-1"),
        dbc.NavLink("Overview", id=f"id-{TAG}-*", href="#", class_name=class_link),
        dbc.NavLink("Updates", id=f"id-{TAG}-*", href="#", class_name=class_link),
        dbc.NavLink("Reports", id=f"id-{TAG}-*", href="#", class_name=class_link),

        dbc.NavItem("DASHBOARD", className="small text-white-50 mt-4 mb-1"),
        dbc.NavLink("Overview", id=f"id-{TAG}-*", href="#", class_name=class_link),
        dbc.NavLink("Weekly", id=f"id-{TAG}-*", href="#", class_name=class_link),
        dbc.NavLink("Monthly", id=f"id-{TAG}-*", href="#", class_name=class_link),
        dbc.NavLink("Annually", id=f"id-{TAG}-*", href="#", class_name=class_link),
    ]

    # define components
    navitem_bottom = dbc.NavItem(children=[
        dbc.DropdownMenu(children=[
            dbc.DropdownMenuItem("Basic Profile", href="#"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Logout", href=PATH_LOGIN)
        ], label=user.email.split("@")[0], class_name="me-1"),
        dbc.Badge(5, color="danger", href="#", class_name="text-decoration-none"),
    ], class_name="d-flex align-items-center")

    # return result
    return dbc.Row(children=[
        # define components
        dbc.Col(children=[
            cbrand.layout(class_name=None),
            html.Hr(className="text-white my-2"),
            dbc.Nav(navlink_list, vertical=True, class_name="mb-auto"),
            html.Hr(className="text-white my-2"),
            dbc.Nav(navitem_bottom, vertical=True, class_name=None),
        ], width=12, md=2, class_name="d-flex flex-column bg-primary px-4 py-2 h-100-scroll"),

        # define components
        dbc.Col("analysis page", width=12, md=10, class_name="d-flex flex-row bg-light px-4 py-2 h-100-scroll"),
    ], align="start", justify="center", class_name="mx-0 vh-100 overflow-auto")
