# _*_ coding: utf-8 _*_

"""
echarts page
"""

import random

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import Input, Output, ClientsideFunction, dcc, html

TAG_BASE = "analysis"
TAG = "analysis-echarts"

# style of page
STYLE_PAGE = ""


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define data
    data_chart = dict(
        id_div=f"id-{TAG}-div-chart",  # div to show chart
        id_storage=f"id-{TAG}-storage-chart",  # storage of chart click data
        x_data=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        y_data=[random.randint(50, 100) for _ in range(10)],
    )

    # return result
    style = {"height": "500px"}
    return html.Div(children=[
        html.Div(id=f"id-{TAG}-div-chart", style=style),  # div to show chart
        fuc.FefferySessionStorage(id=f"id-{TAG}-storage-chart"),  # storage of chart click data
        dcc.Store(id=f"id-{TAG}-data-chart", data=data_chart),  # data to trigger clientside callback
        # define style
        html.Div(id=f"id-{TAG}-message"),
        fuc.FefferyStyle(rawStyle=STYLE_PAGE),
    ], className=None)


# client side callback
dash.clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="render_chart",
    ),
    Output(f"id-{TAG}-div-chart", "children"),
    Input(f"id-{TAG}-data-chart", "data"),
    prevent_initial_call=False,
)


@dash.callback(
    Output(f"id-{TAG}-message", "children"),
    Input(f"id-{TAG}-storage-chart", "data"),
    prevent_initial_call=True,
)
def _update_page(storage_chart):
    content = f"click: {storage_chart}"
    return fac.AntdMessage(content=content, top=50)
