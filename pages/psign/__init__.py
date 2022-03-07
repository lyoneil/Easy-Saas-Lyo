# _*_ coding: utf-8 _*_

"""
sign page
"""

import flask

from .. import palert
from ..paths import *
from . import pemail, plogin, ppwd


def layout(pathname, search):
    """
    layout of page
    """
    if pathname == PATH_LOGIN or pathname == PATH_LOGOUT:
        return plogin.layout(pathname, search)

    if pathname == PATH_REGISTERE or pathname == PATH_RESETPWDE:
        return pemail.layout(pathname, search)
    if pathname == f"{PATH_REGISTERE}/result" or pathname == f"{PATH_RESETPWDE}/result":
        text_sub = f"An email has sent to {flask.session.get('email')}."
        return palert.layout_simple("Sending success", text_sub, "Back to home", PATH_INTROS)

    if pathname == f"{PATH_REGISTERE}-pwd" or pathname == f"{PATH_RESETPWDE}-pwd":
        return ppwd.layout(pathname, search)
    if pathname == f"{PATH_REGISTERE}-pwd/result" or pathname == f"{PATH_RESETPWDE}-pwd/result":
        text_sub = "The password was set successfully."
        return palert.layout_simple("Setting success", text_sub, "Go to login", PATH_LOGIN)

    # return result
    return palert.layout_404(pathname, search, return_href=PATH_INTROS)
