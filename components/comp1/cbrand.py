# _*_ coding: utf-8 _*_

"""
brand component
"""

import dash
import dash_bootstrap_components as dbc
from dash import html

from config import config_app_name
from paths import PATH_ROOT


def layout(pathname, search, href=PATH_ROOT, class_name=None):
    """
    layout of component
    """
    return dbc.NavbarBrand(children=[
        html.Img(src=dash.get_asset_url("favicon.svg"), style={"width": "1.2rem"}),
        html.Span(config_app_name, className="fs-5 align-middle ms-1"),
    ], href=href, class_name=class_name)
