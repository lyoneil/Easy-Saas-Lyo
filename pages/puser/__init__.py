# _*_ coding: utf-8 _*_

"""
user page
"""

import dash
import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, html

from app import app
from components import cfooter, cnavbar, csmallnav, ccatalog
from utility import PATH_LOGOUT, get_trigger_property
from . import padmin, pinfosec, pplanpay

TAG = "user"
CATALOG_LIST = [
    ["Admin", f"id-{TAG}-admin", "#admin"],
    ["ACCOUNT", None, [
        ("Info&Security", f"id-{TAG}-infosec", "#infosec"),
        ("Plan&Payments", f"id-{TAG}-planpay", "#planpay"),
    ]],
]


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    catalog = dbc.Collapse(dbc.Card(children=[
        ccatalog.layout(CATALOG_LIST, class_name=None),
        dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-75 mx-auto my-2"),
    ], class_name="py-2"), id=f"id-{TAG}-collapse", class_name="d-md-block")

    # define components
    ctid = f"id-{TAG}-content"
    content = dbc.Row(children=[
        dbc.Col(catalog, width=12, md=2, class_name="mt-0 mt-md-4"),
        dbc.Col(id=ctid, width=12, md=8, class_name="mt-4 mt-md-4"),
    ], align="start", justify="center", class_name=None)

    # return result
    tgid = f"id-{TAG}-toggler"
    return html.Div(children=[
        cnavbar.layout(fluid=False, class_name=None),
        csmallnav.layout(tgid, "User", fluid=False, class_name=None),
        dbc.Container(content, fluid=False, class_name=None),
        cfooter.layout(fluid=False, class_name=None),
        # define components
        html.A(id={"type": "id-address", "index": TAG}),
    ], className="d-flex flex-column vh-100")


@app.callback(output=[
    dict(
        cadmin=Output(f"id-{TAG}-admin", "className"),
        cinfosec=Output(f"id-{TAG}-infosec", "className"),
        cplanpay=Output(f"id-{TAG}-planpay", "className"),
    ),
    dict(
        is_open=Output(f"id-{TAG}-collapse", "is_open"),
        content=Output(f"id-{TAG}-content", "children"),
        href=Output({"type": "id-address", "index": TAG}, "href"),
    ),
], inputs=dict(
    n_clicks_temp=dict(
        n_clicks0=Input(f"id-{TAG}-admin", "n_clicks"),
        n_clicks1=Input(f"id-{TAG}-infosec", "n_clicks"),
        n_clicks2=Input(f"id-{TAG}-planpay", "n_clicks"),
    ),
    togger=dict(
        n_clicks=Input(f"id-{TAG}-toggler", "n_clicks"),
        is_open=State(f"id-{TAG}-collapse", "is_open"),
    ),
), prevent_initial_call=False)
def _init_page(n_clicks_temp, togger):
    # define class
    class_curr, class_none = "text-primary", "text-black hover-primary"

    # define output
    output0 = dict(cadmin=class_none, cinfosec=class_none, cplanpay=class_none)
    outpute = dict(is_open=dash.no_update, content=None, href=dash.no_update)

    # check user
    if not flask_login.current_user.is_authenticated:
        outpute.update(dict(href=PATH_LOGOUT))
        return [output0, outpute]

    # define variables
    triggered = dash.callback_context.triggered
    curr_id, _, _, value = get_trigger_property(triggered)

    # define is_open
    if curr_id == f"id-{TAG}-toggler" and togger["n_clicks"]:
        outpute.update(dict(is_open=(not togger["is_open"])))

    # define content
    curr_id = curr_id or f"id-{TAG}-infosec"
    if curr_id == f"id-{TAG}-admin":
        output0.update(dict(cadmin=class_curr))
        outpute.update(dict(
            is_open=False,
            content=padmin.layout(None, None),
        ))
    elif curr_id == f"id-{TAG}-infosec":
        output0.update(dict(cinfosec=class_curr))
        outpute.update(dict(
            is_open=False,
            content=pinfosec.layout(None, None),
        ))
    elif curr_id == f"id-{TAG}-planpay":
        output0.update(dict(cplanpay=class_curr))
        outpute.update(dict(
            is_open=False,
            content=pplanpay.layout(None, None),
        ))

    # return result
    return [output0, outpute]
