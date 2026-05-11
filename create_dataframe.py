import pandas as pd
import numpy as np


def create_random_dataframe(rows=5, cols=3, column_names=None):
    """
    Create a pandas dataframe with random data.

    Parameters:
    -----------
    rows : int, default=5
        Number of rows in the dataframe
    cols : int, default=3
        Number of columns in the dataframe
    column_names : list, optional
        List of column names. If None, generates default names

    Returns:
    --------
    pd.DataFrame
        DataFrame with random float values (0-1 range)
    """
    if column_names is None:
        column_names = [f'Column_{chr(65 + i)}' for i in range(cols)]

    df = pd.DataFrame(
        np.random.rand(rows, cols),
        columns=column_names
    )

    return df


if __name__ == "__main__":
    # Create and display a dataframe with default parameters (5 rows, 3 columns)
    df = create_random_dataframe()
    print("Default DataFrame (5 rows, 3 columns):")
    print(df)

    # Example with custom parameters
    print("\n\nCustom DataFrame (3 rows, 4 columns):")
    df_custom = create_random_dataframe(
        rows=3,
        cols=4,
        column_names=['Feature_1', 'Feature_2', 'Feature_3', 'Feature_4']
    )
    print(df_custom)
