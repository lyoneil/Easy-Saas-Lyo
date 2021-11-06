# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc

from ..comps import cfooter, cnavbar
from ..palert import *
from ..paths import *


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    if pathname == PATH_ANALYSIS:
        children = "analysis"
    else:
        return layout_404(pathname, search, PATH_ANALYSIS)

    # define components
    fluid = None
    content = dbc.Container(children, fluid=fluid)

    # define components
    navbar = cnavbar.layout(pathname, search, fluid=fluid)
    footer = cfooter.layout(pathname, search, fluid=fluid)

    # return result
    return [navbar, content, footer]
