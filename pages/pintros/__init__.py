# _*_ coding: utf-8 _*_

"""
intros page
"""

import dash_bootstrap_components as dbc
from dash import html

from utility.paths import PATH_ANALYSIS, PATH_INTROS
from components import cfooter, cnavbar
from . import ccontact, cheader, cintros, cplans

NAV_LINKS = [
    ["Intros", "id-navbar-intros", PATH_INTROS, "border-bottom border-primary"],
    ["Analysis", "id-navbar-analysis", PATH_ANALYSIS, "border-bottom"],
]


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return html.Div(children=[
        cnavbar.layout(NAV_LINKS, fluid=False, class_name=None),
        dbc.Container(children=[
            cheader.layout(class_name=None),
            cintros.layout(class_name="mt-5"),
            cplans.layout(class_name="mt-5"),
            ccontact.layout(class_name="mt-5"),
        ], fluid=False, class_name="my-5"),
        cfooter.layout(fluid=False, class_name=None),
    ], className="d-flex flex-column vh-100")
