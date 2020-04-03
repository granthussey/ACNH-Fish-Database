import pandas as pd
import numpy as np


def filter_backend_table(backend_df):
    """Removes the 'metadata' within the backend table (such as T/F values for months)
    
    Args:
        backend_df (dataframe): Dataframe containing fish/bug data that has T/F columns, 
    
    Returns:
        dataframe: the pretty-fied dataframe
    """

    # Bug doesn't have "Shadow size" column
    if backend_df.columns[0] == "Bug":
        return backend_df.filter(
            items=[
                backend_df.columns[0],
                "Location",
                "Price",
                "Active start hours",
                "Active end hour",
            ]
        )

    # Fish does have "Shadow size" column
    elif backend_df.columns[0] == "Fish":
        return backend_df.filter(
            items=[
                backend_df.columns[0],
                "Location",
                "Shadow size",
                "Price",
                "Active start hours",
                "Active end hour",
            ]
        )


def get_fish_logic(backend_df, selected_fish):
    """Returns a logical vector of shape (1xlen(backend_df)) to select
    rows and columns for the user
    
    Args:
        backend_df (dataframe)
        selected_fish (str or list): str if one selected, list if multiple, [] if deleted selections
    
    Returns:
        [type]: [description]
    """

    # if [] or None, return all false
    if not selected_fish:
        return [False] * len(backend_df)

    else:

        # if str, return only the one fish
        if isinstance(selected_fish, str):
            selected = (
                backend_df["Fish"] == selected_fish
            )  # type pd.Series, logical vector
            return selected.tolist()

        # if list, return all rows for selected fish
        elif isinstance(selected_fish, list):
            selected = backend_df["Fish"].isin(
                selected_fish
            )  # type pd.Series, logical vector
            return selected.tolist()

        else:
            print("there was an error in get_fish_logic")
            # return all false for compatability
            return [False] * len(backend_df)


def get_month_logic(backend_df, selected_months):
    """backend_df contains columns "January":"December" 
    that are pre-determined boolean vectors"""

    # if [] or None, return all false
    if not selected_months:
        return [False] * len(backend_df)

    else:

        # if str, return fish available in that single month
        if isinstance(selected_months, str):
            selected = backend_df[selected_months]  # type pd.Series, logical vector
            return selected.tolist()

        # if list, return an intersection of all months
        elif isinstance(selected_months, list):

            # Begin with an all-true pd.Series object
            selected = [True] * len(backend_df)

            # Recursively multiply it by each month's logical vectors
            for each_month in selected_months:
                selected = (
                    selected & backend_df[each_month]
                )  # type pd.Series, logical vector

            return selected.tolist()

        else:
            print("there was an error in get_month_logic")
            # return all false for compatability
            return [False] * len(backend_df)


# This will need to be changed before deployment
# to read in from a public Google Sheet
def get_backend_fish_df():
    return pd.read_pickle("/Users/granthussey/github/ACNL/data/acnl_fish.pkl")
