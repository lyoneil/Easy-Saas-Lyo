# _*_ coding: utf-8 _*_

"""
template page
"""

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from config import config_app_name

from ..paths import *


def layout(pathname, search, tag, params):
    """
    layout of page
    """
    args_button = {"size": "lg", "class_name": "w-100 mt-4"}
    return html.Div(children=[
        dcc.Store(id=f"id-{tag}-pathname", data=pathname),
        html.A(id={"type": "id-address", "index": tag}, className="_class_address_dummpy"),

        html.A(children=[
            html.Img(src=dash.get_asset_url("favicon.svg"), style={"width": "1.25rem"}),
            html.Span(config_app_name, className="fs-5 text-primary align-middle"),
        ], href=PATH_INTROS, className="text-decoration-none position-absolute top-0 start-0"),

        dbc.Row(children=[
            dbc.Col(children=[
                html.Img(src=dash.get_asset_url(params["image_src"]), className="img-fluid"),
            ], width=10, md=4, class_name="mt-auto mt-md-0"),
            dbc.Col(children=[
                html.Div(params["text_hd"], className="text-center fs-1"),
                html.Div(params["text_sub"], className="text-center text-muted"),

                dbc.Form(params["form_children"], class_name="mt-4"),
                html.Div(id=f"id-{tag}-fb", className="text-danger text-center"),

                dbc.Button(params["text_button"], id=f"id-{tag}-button", **args_button),
                html.Div(params["other_list"], className="d-flex justify-content-between"),
            ], width=10, md={"size": 3, "offset": 1}, class_name="mb-auto mb-md-0"),
        ], align="center", justify="center", class_name="vh-100 w-100 mx-auto"),
    ])
