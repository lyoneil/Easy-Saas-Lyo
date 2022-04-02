# _*_ coding: utf-8 _*_

"""
accordion component
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(catalog_list, curr_path=None, flush=None, class_name=None):
    """
    layout of component
    """
    # define class
    class_none = "text-decoration-none px-5 py-2 text-black hover-primary"
    class_curr = "text-decoration-none px-5 py-2 text-primary"

    # define components
    ad_item_list, active_id = [], None
    for title_first, id_first, list_second in catalog_list:
        address_list = []
        for title, _id, path in list_second:
            if path == curr_path:
                active_id = id_first
            _class = class_curr if path == curr_path else class_none
            address_list.append(html.A(title, id=_id, href=path, className=_class))

        # define components
        div = html.Div(address_list, className="d-flex flex-column py-2")
        ad_item_list.append(dbc.AccordionItem(div, title=title_first, item_id=id_first))

    # return result
    class_name = class_name or "border-top-solid border-bottom-solid"
    return dbc.Accordion(ad_item_list, active_item=active_id, flush=flush, class_name=class_name)
