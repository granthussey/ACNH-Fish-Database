import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

# Import external stylesheet from internet
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Initialize app with external stylesheet
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read in dataframe to manipulate
fish = pd.read_pickle("/Users/granthussey/github/ACNL/data/acnl_fish.pkl")
# bugs = pd.read_pickle('/Users/granthussey/github/ACNL/data/acnl_bug.pkl')

# Initialize global variables we'll constantly reuse
available_fish = fish[fish.columns[0]].unique()
available_months = fish.loc[:, "January":"December"].columns.unique().tolist()


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


def filter_backend_table(backend_table):
    """Removes the 'metadata' within the backend table (such as T/F values for months)
    
    Args:
        backend_table (dataframe): Dataframe containing fish/bug data that has T/F columns, 
    
    Returns:
        dataframe: the pretty-fied dataframe
    """

    # Bug doesn't have "Shadow size" column
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

    # Fish does have "Shadow size" column
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


def get_fish_logic(df, selected_fish):

    # if [] or None, return all false
    if not selected_fish:
        print("trigger f")
        return [False] * len(df)

    # if str or list, iterate
    else:

        if isinstance(selected_fish, str):
            print("pd_vec f")
            print((pd_vector))
            print()
            pd_vector = df["Fish"] == selected_fish
            return pd_vector.tolist()  # single logical vector

        elif isinstance(selected_fish, list):
            # "AND" an all-true vector by each T/F column
            selected = pd.Series([True] * len(df))
            for each_fish in selected_fish:
                cur_vector = df["Fish"] == each_fish
                selected = selected & cur_vector

            print("selected f")
            print((selected))
            print()
            return selected.tolist()

        else:
            print("there was an error in get_fish_logic")
            # return all false for compatability
            return [False] * len(df)


def get_month_logic(df, selected_months):

    print(df)

    # if [] or None, return all false
    if not selected_months:
        print("trigger mo")
        return [False] * len(df)

    # if str or list, iterate
    else:

        if isinstance(selected_months, str):
            print(len(df))
            pd_vector = df[selected_months]

            print("pd_vec mo")
            print(pd_vector)
            print(len(pd_vector))
            print(type(pd_vector))
            print()

            test = pd_vector.tolist()

            print("pd_vec  test")
            print(test)
            print(len(test))
            print(type(test))
            print()
            return test  # single logical vector

        elif isinstance(selected_months, list):

            print(len(df))
            # "AND" an all-true vector by each T/F column
            selected = pd.Series([True] * len(df))
            for each_month in selected_months:
                selected = selected & df[each_month]

            print("selected mo")
            print(selected)
            print(len(selected))
            print(type(selected))
            print()

            test = selected.tolist()

            print("selected mo test")
            print(test)
            print(len(test))
            print(type(test))
            print()

            return test

        else:
            print("there was an error in get_month_logic")
            # return all false for compatability
            return [False] * len(df)


# def filter_given_months(backend_table, months):

#     """
#     This needs to take either a list or a str and deal with it properly.
#     """

#     # remove columns from backend_table that we wont want to show
#     presentable_df = filter_backend_table(backend_table)

#     # print('This is the length of presentable_df ' + str(len(presentable_df)))

#     try:

#         # If user inputs a single month
#         if isinstance(months, str):
#             selected = backend_table[months]

#             return presentable_df.loc[selected]

#         # If user inputs more than one month
#         elif isinstance(months, list):

#             # "AND" an all-true vector by each T/F column
#             selected = pd.Series([True] * len(presentable_df))
#             for each_month in months:
#                 selected = selected & backend_table[each_month]

#             return presentable_df.loc[selected]

#         # If empty string (user deleted everything from Dropdown)
#         elif not months:
#             pass

#     except Exception:
#         print("There was an exception in filter_given_months() function")
#         pass

app.layout = html.Div(
    [
        # THIS IS EVERYTHING ABOVE THE DASH TABLE
        html.Div(
            children=[
                # TITLE
                html.H3(
                    id="title",
                    children=html.Div(id="testing", children="The Fish Database"),
                ),
                # DESCRIPTION
                html.Div(
                    children=[
                        """
                        Welcome to the premier fish database.
                        Choose from the drop downs below to filter the table below.
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
                                    options=iteratable_to_dropdown_options(
                                        available_fish
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
                                    options=iteratable_to_dropdown_options(
                                        ["All"] + available_months
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
                                    options=dict_to_dropdown_options(
                                        dict(
                                            zip(
                                                list(
                                                    "Leaving after {}".format(month)
                                                    for month in available_months
                                                ),
                                                available_months,
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
                                "Find fish coming to your island ",
                                dcc.Dropdown(
                                    id="month-arriving-dropdown",
                                    options=dict_to_dropdown_options(
                                        dict(
                                            zip(
                                                list(
                                                    "Arriving in {}".format(month)
                                                    for month in available_months
                                                ),
                                                available_months,
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
        # 1. style_data_conditional
        # 2. style_data
        # 3. style_filter_conditional
        # 4. style_filter
        # 5. style_header_conditional
        # 6. style_header
        # 7. style_cell_conditional
        # 8. style_cell
        # THIS IS THE DASH TABLE
        html.Div(
            children=dash_table.DataTable(
                id="fish-df",
                columns=df_cols_to_dashtable_cols(filter_backend_table(fish)),
                data=filter_backend_table(fish).to_dict("records"),
                # Remove the certical lines
                style_as_list_view=True,
                # Make the columns
                style_header={"textAlign": "left", "fontWeight": "bold"},
                style_data_conditional=[
                    {
                        "if": {"row_index": "odd"},
                        "backgroundColor": "rgb(248, 248, 248)",
                    }
                ],
                style_data={"font": "Arial"},
                sort_action="native",
                # filter_action="native",
                # style_data={"border": "1px solid black"}
                # style_cell_conditional=[
                #     {"if": {"column_id": c}, "textAlign": "left"}
                #     for c in [
                #         "Fish",
                #         "Location",
                #         "Shadow size",
                #         "Active start hours",
                #         "Active end hour",
                #     ]
                # ],
            ),
            style={
                "marginBottom": 50,
                "marginTop": 25,
                "marginRight": 25,
                "marginLeft": 25,
            },
            # style={"margin": "auto"},
        ),
        # Initialize the table for display
        # html.Div(id='my-table', children=generate_table(fish), style={'width':'80%'
        #         }
        #     )
    ]
)


def return_original_fish_table():
    presentable_table = filter_backend_table(fish)
    return (
        presentable_table.to_dict("records"),
        df_cols_to_dashtable_cols(presentable_table),
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

    print()
    print(month_dropdown_value)
    print(fish_dropdown_value)
    print(month_arriving_value)
    print(month_leaving_value)
    print()

    """
    Logical Overview
    1) Check to see if user selected options for "month-arriving-dropdown" or "month-leaving-dropdown"
        a. Use those values to filter fish
    
    2) Otherwise, process "selected" vectors for month-dropdown and fish-dropdown
        a. OR those vectors together!
    """

    if isinstance(month_arriving_value, str):
        raise PreventUpdate  # placeholder

    elif isinstance(month_leaving_value, str):
        raise PreventUpdate  # placeholder

    else:

        # Don't update if [] or None
        if not month_dropdown_value and not fish_dropdown_value:
            raise PreventUpdate

        # Update otherwise
        else:
            # you're going to get a list of str, str, or [] or None for one of the dropdowns,
            # so now I need to handle that.

            # Get months filter if it exists
            log1 = get_month_logic(fish, month_dropdown_value)
            print("month vector")
            print(len(log1))
            print()

            # Get fish filter if that exists
            log2 = get_fish_logic(fish, fish_dropdown_value)
            print("fish vector")
            print((log2))
            print()

            selected = log1 or log2

            print(selected)

            presentable_df = filter_backend_table(fish)

            print("the length of presentable df is " + str(len(presentable_df)))
            return (
                presentable_df.loc[selected].to_dict("records"),
                df_cols_to_dashtable_cols(presentable_df.loc[selected]),
            )


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
def erase_fish_and_month(
    month_arriving_value, month_leaving_value,
):
    """If either inputs are not [] nor None, then erase the value user input into
    month-dropdown and fish-dropdown"""

    # Triggers when someone puts data in these fields
    if isinstance(month_arriving_value, str):
        return (True, True, [], [], False, True)

    elif isinstance(month_leaving_value, str):
        return (True, True, [], [], True, False)

    # Triggers when someone deletes values from these fields
    elif not month_arriving_value and not month_leaving_value:
        return (False, False, [], [], False, False)

    # Don't update if these fields are empty
    else:
        raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
    # app.run_server(debug=True, dev_tools_hot_reload=False)
