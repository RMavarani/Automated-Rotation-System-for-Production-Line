import pandas as pd
from rapidfuzz import process, fuzz

def find_closest_match(df: pd.DataFrame, search_string: str, column_name: str):
    """
    Find the closest match to the search_string in the specified column of the DataFrame.

    Parameters:
    df (pd.DataFrame): Input dataframe.
    search_string (str): The string to search for.
    column_name (str): The column in the dataframe to search within.

    Returns:
    tuple: Closest match and its similarity score.
    """
    # Extract the column values
    column_values = df[column_name].tolist()

    # Use process.extractOne to find the best match
    closest_match, score, idx = process.extractOne(search_string, column_values, scorer=fuzz.ratio)

    return closest_match, score

df=pd.read_excel('app\\functions\\Book1.xlsx')
find_closest_match(df,'string_test','name input')