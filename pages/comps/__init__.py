# _*_ coding: utf-8 _*_

"""
components module
"""

from dash import html

from config import CONFIG_APP_NAME
from utility.paths import PATH_ROOT


def get_component_logo(size):
    """
    layout of component
    """
    return html.A(CONFIG_APP_NAME, href=PATH_ROOT, style={
        "color": "#000000",
        "font-weight": "900",
        "font-size": f"{size}px",
        "font-family": "Raleway-Bold",
        "text-decoration": "none",
    })
