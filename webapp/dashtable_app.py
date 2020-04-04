import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

import personal_dash_tools as tls
import ac_df_tools as ac_tls

#
# REMINDERS
# This is the order of style for dash_table
# 1. style_data_conditional
# 2. style_data
# 3. style_filter_conditional
# 4. style_filter
# 5. style_header_conditional
# 6. style_header
# 7. style_cell_conditional
# 8. style_cell
#

# Import external stylesheet from internet
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Initialize app with external stylesheet
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#
# CONSTANTS
BACKEND_FISH_DF = ac_tls.get_backend_fish_df()
ENDUSER_FISH_DF = ac_tls.filter_backend_table(BACKEND_FISH_DF)
AVAIL_FISH = BACKEND_FISH_DF[BACKEND_FISH_DF.columns[0]].unique()
AVAIL_MONTHS = BACKEND_FISH_DF.loc[:, "January":"December"].columns.unique().tolist()
#

app.layout = html.Div(
    [
        # THIS IS EVERYTHING ABOVE THE DASH TABLE
        html.Div(
            children=[
                # TITLE
                html.H3(id="title", children="The Fish Database",),
                # DESCRIPTION
                html.Div(
                    children=[
                        """
                        Welcome to the internet's premier fish database.
                        Choose from the dropdowns below to explore.
                        """
                    ],
                    style={"padding": "10px 5px"},
                ),
                # CONTAINER FOR fish-dropdown AND month-dropdown
                html.Div(
                    children=[
                        # DROPDOWN FISH NAME
                        html.Div(
                            children=[
                                "Filter by fish name",
                                dcc.Dropdown(
                                    id="fish-dropdown",
                                    options=tls.iteratable_to_dropdown_options(
                                        AVAIL_FISH
                                    ),
                                    placeholder="Choose fish...",
                                    multi=True,
                                ),
                            ],
                            style={"width": "49%", "display": "inline-block"},
                        ),
                        # DROPDOWN ACTIVE MONTH
                        html.Div(
                            children=[
                                "Filter by month fish is active",
                                dcc.Dropdown(
                                    id="month-dropdown",
                                    options=tls.iteratable_to_dropdown_options(
                                        ["All"] + AVAIL_MONTHS  # Make 'all' an option!
                                    ),
                                    placeholder="Choose month(s)...",
                                    multi=True,
                                ),
                            ],
                            style={
                                "width": "49%",
                                "float": "right",
                                "display": "inline-block",
                            },
                        ),
                    ]
                ),
                # CONTAINER FOR month-leaving-dropdown AND month-arriving-dropdown
                html.Div(
                    children=[
                        # DROPDOWN LEAVING FISH
                        html.Div(
                            children=[
                                "Find fish leaving your island",
                                dcc.Dropdown(
                                    id="month-leaving-dropdown",
                                    options=tls.dict_to_dropdown_options(
                                        dict(
                                            zip(
                                                list(
                                                    "Leaving after {}".format(month)
                                                    for month in AVAIL_MONTHS
                                                ),
                                                AVAIL_MONTHS,
                                            )
                                        )
                                    ),
                                    placeholder="Choose month...",
                                    multi=False,
                                    disabled=False,
                                ),
                            ],
                            style={"width": "49%", "display": "inline-block"},
                        ),
                        # DROPDOWN ARRIVING FISH
                        html.Div(
                            children=[
                                "Find fish coming to your island",
                                dcc.Dropdown(
                                    id="month-arriving-dropdown",
                                    options=tls.dict_to_dropdown_options(
                                        dict(
                                            zip(
                                                list(
                                                    "Arriving in {}".format(month)
                                                    for month in AVAIL_MONTHS
                                                ),
                                                AVAIL_MONTHS,
                                            )
                                        )
                                    ),
                                    placeholder="Choose month...",
                                    multi=False,
                                    disabled=False,
                                ),
                            ],
                            style={
                                "width": "49%",
                                "float": "right",
                                "display": "inline-block",
                            },
                        ),
                    ],
                    style={"padding": "10px 0px"},
                ),
            ],
            style={
                "borderBottom": "thin lightgrey solid",
                "backgroundColor": "rgb(250, 250, 250)",
                "padding": "10px 5px",
            },
        ),
        # THIS IS THE DASH TABLE
        html.Div(
            children=dash_table.DataTable(
                id="fish-df",
                columns=tls.df_cols_to_dashtable_cols(ENDUSER_FISH_DF),
                data=ENDUSER_FISH_DF.to_dict("records"),
                style_as_list_view=True,  # Remove vertical lines
                style_header={"textAlign": "left", "fontWeight": "bold"},
                style_data_conditional=[  # Make striped rows for easy viewing
                    {
                        "if": {"row_index": "odd"},
                        "backgroundColor": "rgb(248, 248, 248)",
                    }
                ],
                style_data={"font": "Arial"},  # Love me some Arial
                sort_action="native",  # Allow user to sort
            ),
            style={
                "marginBottom": 50,
                "marginTop": 25,
                "marginRight": 25,
                "marginLeft": 25,
            },
        ),
        # THIS IS A FOOTER
        html.Div(
            children=html.Footer(
                id="footer",
                children=[
                    "Come see this project on ",
                    html.A("GitHub", href="https://www.github.com/granthussey"),
                    ". Code by Grant Hussey. Visit my website: ",
                    html.A("www.granthussey.com", href="https://www.granthussey.com"),
                    html.Br(),
                    "Original dataset taken from ",
                    html.A(
                        "this Google Sheet.",
                        href="https://docs.google.com/spreadsheets/d/1ooePgv7AmENQsoxPuvChIa3S4CnZlUgwMLHXTjKXf-4/htmlview",
                    ),
                ],
                style={
                    "justify": "center",
                    "background-color": "#D3D3D3",
                    "padding": "5px",
                },
            ),
            style={"text-align": "center"},
        ),
    ]
)


@app.callback(
    [Output("fish-df", "data"), Output("fish-df", "columns")],
    [
        Input("month-dropdown", "value"),
        Input("fish-dropdown", "value"),
        Input("month-arriving-dropdown", "value"),
        Input("month-leaving-dropdown", "value"),
    ],
)
def update_table(
    month_dropdown_value, fish_dropdown_value, month_arriving_value, month_leaving_value
):

    # print()
    # print(month_dropdown_value)
    # print(fish_dropdown_value)
    # print(month_arriving_value)
    # print(month_leaving_value)
    # print()

    """
    Logical Overview
    1) Check to see if user selected options for "month-arriving-dropdown" or "month-leaving-dropdown"
        a. Use those values to filter fish
    
    2) Otherwise, process "selected" vectors for month-dropdown and fish-dropdown
        a. OR those vectors together!
    """

    # need to rethink loop lol
    # but let's build these two fxns first
    # then apply them, should be relatively easy.

    if isinstance(month_arriving_value, str):
        selected = ac_tls.get_species_arriving_logic(
            month_arriving_value, AVAIL_MONTHS, BACKEND_FISH_DF
        )
        return (
            ENDUSER_FISH_DF.loc[selected].to_dict("records"),
            tls.df_cols_to_dashtable_cols(ENDUSER_FISH_DF.loc[selected]),
        )

    elif isinstance(month_leaving_value, str):
        selected = ac_tls.get_species_leaving_logic(
            month_leaving_value, AVAIL_MONTHS, BACKEND_FISH_DF
        )
        return (
            ENDUSER_FISH_DF.loc[selected].to_dict("records"),
            tls.df_cols_to_dashtable_cols(ENDUSER_FISH_DF.loc[selected]),
        )

    else:

        # Don't update if [] or None
        if not month_dropdown_value and not fish_dropdown_value:
            raise PreventUpdate

        # Update otherwise
        else:

            # Get months filter if it exists
            log1 = ac_tls.get_month_logic(BACKEND_FISH_DF, month_dropdown_value)

            # Get fish filter if that exists
            log2 = ac_tls.get_fish_logic(BACKEND_FISH_DF, fish_dropdown_value)

            # or is not element-wise for lists, so use np
            selected = np.logical_or(log1, log2)

            return (
                ENDUSER_FISH_DF.loc[selected].to_dict("records"),
                tls.df_cols_to_dashtable_cols(ENDUSER_FISH_DF.loc[selected]),
            )


# Disable certain dropdowns when others are filled
@app.callback(
    [
        Output("month-dropdown", "disabled"),
        Output("fish-dropdown", "disabled"),
        Output("month-dropdown", "value"),
        Output("fish-dropdown", "value"),
        Output("month-arriving-dropdown", "disabled"),
        Output("month-leaving-dropdown", "disabled"),
    ],
    [
        Input("month-arriving-dropdown", "value"),
        Input("month-leaving-dropdown", "value"),
    ],
)
def input_controls(
    month_arriving_value, month_leaving_value,
):
    """If either inputs are not [] nor None, then erase the value user input into
    month-dropdown and fish-dropdown"""

    #
    # Triggers when someone puts data in these fields
    if isinstance(month_arriving_value, str):
        return (True, True, [], [], False, True)

    elif isinstance(month_leaving_value, str):
        return (True, True, [], [], True, False)
    #

    # Triggers when someone deletes values from these fields
    elif not month_arriving_value and not month_leaving_value:
        return (False, False, [], [], False, False)

    # Don't update if these fields are empty
    else:
        raise PreventUpdate


if __name__ == "__main__":
    # app.run_server(debug=True)
    server = app.server
    # app.run_server(debug=True, dev_tools_hot_reload=False)
