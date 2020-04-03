import pandas as pd
import numpy as np
import dash_html_components as html


def df_cols_to_dashtable_cols(df):
    """Formats dataframe columns in format that dash_tables can accept"""

    return [{"name": i, "id": i} for i in df.columns]


def iteratable_to_dropdown_options(iterable):
    """Formats an iteratable (such as a list) 
    in a format that dcc.dropdown can accept for  'option' parameter"""

    return [{"label": each, "value": each} for each in iterable]


def dict_to_dropdown_options(dic):
    """Formats a dictionary (such as a list) 
    in a format that dcc.dropdown can accept for  'option' parameter.
    
    This is very important if you want the label different from the value.

    dic's KEY will become the LABEL (what you see in dropdown)
    dic's VALUE will become the VALUE (what gets propogated thru callbacks)
    """

    return [{"label": key, "value": dic[key]} for key in dic]


def generate_table(df, max_rows=100):

    """Creates an html table for Html.table component
    
    Args:
        df (dataframe)
        max_rows (int, optional): The size of the table that will be displayed. 
        Defaults to 100.
    
    Returns:
        Html.table format
    """

    return html.Table(
        children=[
            html.Thead(html.Tr([html.Th(col) for col in df.columns])),
            html.Tbody(
                [
                    html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
                    for i in range(min(len(df), max_rows))
                ]
            ),
        ]
    )
