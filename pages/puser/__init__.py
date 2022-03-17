# _*_ coding: utf-8 _*_

"""
user page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app
from . import paccount, pbilling
from ..components import ccatalog, cfooter, cnavbar, csmallnav
from ..paths import PATH_LOGOUT, PATH_USER

TAG = "user"
CATALOG_LIST = [
    ["ACCOUNT", None, [
        ("General", f"{PATH_USER}-ac-general"),
        ("Security", f"{PATH_USER}-ac-security"),
        ("Notifications", f"{PATH_USER}-ac-notify"),
    ]],
    ["BILLING", None, [
        ("Plan", f"{PATH_USER}-bl-plan"),
        ("Payments", f"{PATH_USER}-bl-payments"),
    ]],
]


def layout(pathname, search):
    """
    layout of page
    """
    # define pathname
    pathname = f"{PATH_USER}-ac-general" if pathname == PATH_USER else pathname

    # define components
    if pathname.startswith(f"{PATH_USER}-bl-"):
        title = "BILLING"
        content = pbilling.layout(pathname, search)
    else:
        title = "ACCOUNT"
        content = paccount.layout(pathname, search)

    # define components
    catalog = dbc.Collapse(dbc.Card(children=[
        ccatalog.layout(pathname, search, CATALOG_LIST, class_name=None),
        dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-75 mx-auto my-4"),
    ]), id=f"id-{TAG}-collapse", class_name="d-md-block")

    # return result
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=None, class_navbar=None),
        csmallnav.layout(pathname, search, f"id-{TAG}-toggler", title, fluid=None),
        dbc.Container(dbc.Row(children=[
            dbc.Col(catalog, width=12, md=2, class_name="mt-0 mt-md-4"),
            dbc.Col(content, width=12, md=8, class_name="mt-4 mt-md-4"),
        ], align="start", justify="center"), fluid=None),
        cfooter.layout(pathname, search, fluid=None, class_footer=None),
    ], className="d-flex flex-column vh-100")


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
