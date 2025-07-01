import pandas as pd


def sort_and_reset(df, col=None):
    """Sort dataframe by given column, if no colname is given. only reset the indexes.

    Args:
        df (DataFrame): Dataframe to sort
        col (str, optional): Column name to sort by. Defaults to None.

    Returns:
        df (DataFrame): Dataframe with sorted values and resetted index.
    """

    # Check if col is sting
    if isinstance(col, str):
        # Sort by col
        df = df.sort_values(by=col)

    # Resest index
    df = df.reset_index()
    return df
