import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

# Set stylesheet and initialize app
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read in fish and bugs csv
# df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

fish = pd.read_pickle("/Users/granthussey/github/ACNL/data/acnl_fish.pkl")
# bugs = pd.read_pickle('/Users/granthussey/github/ACNL/data/acnl_bug.pkl')

available_fish = fish[fish.columns[0]].unique()
# available_bugs =
available_months = fish.loc[:, "All":"December"].columns.unique()


def generate_table(dataframe, max_rows=100):
    return html.Table(
        children=[
            html.Thead(html.Tr([html.Th(col) for col in dataframe.columns])),
            html.Tbody(
                [
                    html.Tr(
                        [html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]
                    )
                    for i in range(min(len(dataframe), max_rows))
                ]
            ),
        ]
    )


def filter_backend_table(backend_table):

    if backend_table.columns[0] == "Bug":
        df = backend_table.filter(
            items=[
                backend_table.columns[0],
                "Location",
                "Price",
                "Active start hours",
                "Active end hour",
            ]
        )

    elif backend_table.columns[0] == "Fish":
        df = backend_table.filter(
            items=[
                backend_table.columns[0],
                "Location",
                "Shadow size",
                "Price",
                "Active start hours",
                "Active end hour",
            ]
        )

    return df


def filter_given_months(backend_table, months):

    """
    This needs to take either a list or a str and deal with it properly.
    """

    # remove columns from backend_table that we wont want to show
    presentable_df = filter_backend_table(backend_table)

    # print('This is the length of presentable_df ' + str(len(presentable_df)))

    try:

        # If user inputs a single month
        if isinstance(months, str):
            selected = backend_table[months]
            # print('This is the length of filtered df is  ' + str(len(presentable_df.loc[selected])))
            # print()
            # print()
            # print()

            # Return proper df
            return generate_table(presentable_df.loc[selected])

        # If user inputs more than one month
        elif isinstance(months, list):
            # initialize an all-true vector to use later
            selected = pd.Series([True] * len(presentable_df))
            for each_month in months:
                selected = selected & backend_table[each_month]

            # print('This is the length of filtered df is  ' + str(len(presentable_df.loc[selected])))
            # print()
            # print()
            # print()
            # Return proper df
            return generate_table(presentable_df.loc[selected])

        # If empty string (user deleted everything from Dropdown)
        elif not months:
            pass

    except Exception:
        print("There was an exception in filter_given_months() function")
        pass


app.layout = html.Div(
    [
        # Initialize the filters top two columns
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="fish",
                            options=[{"label": i, "value": i} for i in available_fish],
                            placeholder="Select a fish, or filter by month",
                            multi=True,
                        )
                    ],
                    style={"width": "49%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="month",
                            options=[
                                {"label": i, "value": i} for i in available_months
                            ],
                            value="March",
                            multi=True,
                        ),
                    ],
                    style={"width": "49%", "float": "right", "display": "inline-block"},
                ),
            ],
            style={
                "borderBottom": "thin lightgrey solid",
                "backgroundColor": "rgb(250, 250, 250)",
                "padding": "10px 5px",
            },
        ),
        # Initialize the table for display
        html.Div(id="my-table", children=generate_table(fish), style={"width": "80%"}),
    ]
)

#
@app.callback(Output("my-table", "children"), [Input("month", "value")])
def update_table(months_to_filter):
    # print(months_to_filter)
    return filter_given_months(fish, months_to_filter)


if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_hot_reload=False)
