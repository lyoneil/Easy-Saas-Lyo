# _*_ coding: utf-8 _*_

"""
accordion component
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(pathname, search, tag, catalog_list, flush=None, class_name=None):
    """
    layout of component
    """
    # define components
    ad_item_list, active_id = [], None
    for index, (title_first, icon_first, list_second) in enumerate(catalog_list):
        item_id = f"id-{tag}-accordion-{index}"

        # define components
        address_list = []
        for title_second, path in list_second:
            if path == pathname:
                active_id = item_id

            # define components
            if path == pathname:
                _class = "text-decoration-none px-5 py-2 text-primary"
            else:
                _class = "text-decoration-none px-5 py-2 text-black hover-primary"
            address_list.append(html.A(title_second, href=path, className=_class))

        # define components
        div = html.Div(address_list, className="d-flex flex-column py-2")
        ad_item_list.append(dbc.AccordionItem(div, item_id=item_id, title=title_first))

    # return result
    _class = class_name or "border-top-solid border-bottom-solid"
    return dbc.Accordion(ad_item_list, active_item=active_id, flush=flush, class_name=_class)