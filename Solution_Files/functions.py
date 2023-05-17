from fuzzywuzzy import fuzz # fuzzy logic, compare strings
from collections import defaultdict # dictionary with default value
import pandas as pd # data manipulation

def find_similar_columns(df, threshold=90):
    """ Find columns in a dataframe that are similar to each other.

    Args:
        df (pandas.DataFrame): Dataframe to find similar columns of.
        threshold (int): Percentage of similarity below which two columns are considered different.
    
    Returns:
        dict: Dictionary where the keys are lower-case column names and the values are lists of original
        column names that map to the lower-case column name.
    """
    # Create a dictionary where the keys are lower-case column names
    # and the values are lists of original column names that map to the lower-case column name
    column_dict = defaultdict(list)

    cols = list(df.columns)
    while len(cols) > 0:
        col = cols.pop(0) # Get the first column in the list and remove it from the list
        column_dict[col].append(col) # Add the column name to the list of columns that match the lower-case column name
        for other_col in cols:
            # If the two column names are similar enough, remove the other column name from the list
            if fuzz.ratio(col, other_col) >= threshold:
                column_dict[col].append(other_col)
        cols = [x for x in cols if x not in column_dict[col]]

    # Filter out entries in the dictionary where there are not at least two similar column names
    similar_columns = {key: value for key, value in column_dict.items() if len(value) > 1}
    
    return similar_columns

# Function to investigate possible duplicated columns in a dataframe
def investigate_similar_columns(df: pd.DataFrame, first_column: str, second_column: str,
                                common_columns: list):
    """ Function to investigate possible duplicated columns in a dataframe
    
    Args:
        df (pd.DataFrame): Dataframe to investigate
        first_column (str): Name of the first column to compare
        second_column (str): Name of the second column to compare

    Returns:
        None
    """
    # Check if the two columns are equal
    columns_equal = df[first_column].equals(df[second_column])

    # Print the result
    print('Columns are equal: ', columns_equal)

    # Compare the two columns in the previous line
    condition = df[first_column] == df[second_column]

    # Check if non-null values are the same
    non_null_values_same = df[condition][first_column].equals(df[condition][second_column])

    print('Non-null values are the same: ', non_null_values_same)

    # Display different records
    different_records = df[~condition][[first_column, second_column]]

    # Boolean variable that indicates that there is at least one null value in the first column
    first_column_null = df[first_column].isnull().sum() > 0

    # Boolean variable that indicates that there is at least one null value in the second column
    second_column_null = df[second_column].isnull().sum() > 0

    # Create variable to store the column name with the non-null (imputed) values
    non_null_column = ''

    # Check the boolean variables and print if there is a null value in any of the columns or in both
    # If only one column has all non-null values, print the name of the column and a message saying
    # This column has all non-null values. Keeping this column and dropping the other one.
    if first_column_null and second_column_null:
        print('Both columns have null values')
    elif first_column_null and not second_column_null:
        non_null_column = second_column
        print('Column with the non-null (imputed) values: ', second_column)
        print('Column to drop: ', first_column)
    elif second_column_null and not first_column_null:
        non_null_column = first_column
        print('Column with the non-null (imputed) values: ', first_column)
        print('Column to drop: ', second_column)
    else:
        print('Both columns have non-null values')
    
    # Check if non_null_column is inside common_columns and print the result
    if non_null_column in common_columns:
        print('Column {} is in common_columns'.format(non_null_column))
    else:
        print('Column {} is not in common_columns'.format(non_null_column))

# Function to swap two column names in a dataframe
def swap_columns(df: pd.DataFrame, first_column: str, second_column: str):
    """ Function to swap two column names in a dataframe
    
    Args:
        df (pd.DataFrame): Dataframe to swap columns in
        first_column (str): Name of the first column to swap
        second_column (str): Name of the second column to swap

    Returns:
        pd.DataFrame: Dataframe with swapped columns
    """
    # Create a copy of the dataframe
    df_swapped = df.copy()

    # Rename the columns by passing a dictionary to the `rename` method
    df_swapped = df_swapped.rename(columns={first_column: second_column + "_temp",
                                            second_column: first_column})
    
    # Now rename the temporary column to 'column2'
    df_swapped = df_swapped.rename(columns={second_column + "_temp": second_column})

    return df_swapped
