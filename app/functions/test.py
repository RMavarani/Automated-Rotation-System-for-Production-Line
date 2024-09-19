import pandas as pd

def levenshtein_distance(str1, str2):
    """
    Compute the Levenshtein distance between two strings.
    
    Parameters:
    str1 (str): First string.
    str2 (str): Second string.
    
    Returns:
    int: Levenshtein distance between str1 and str2.
    """
    # Create a matrix to store distances
    dp = [[0 for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]

    # Initialize the matrix
    for i in range(len(str1) + 1):
        for j in range(len(str2) + 1):
            if i == 0:
                dp[i][j] = j  # If first string is empty, insert all chars of second string
            elif j == 0:
                dp[i][j] = i  # If second string is empty, remove all chars of first string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # If characters are the same, no operation needed
            else:
                dp[i][j] = 1 + min(dp[i-1][j],      # Remove
                                   dp[i][j-1],      # Insert
                                   dp[i-1][j-1])    # Replace

    return dp[len(str1)][len(str2)]

def find_closest_match(df: pd.DataFrame, search_string: str, column_name: str):
    """
    Find the closest match to the search_string in the specified column of the DataFrame
    based on the smallest Levenshtein distance.
    
    Parameters:
    df (pd.DataFrame): Input dataframe.
    search_string (str): The string to search for.
    column_name (str): The column in the dataframe to search within.
    
    Returns:
    tuple: Closest match and its Levenshtein distance.
    """
    # Initialize variables to track the closest match
    closest_match = None
    smallest_distance = float('inf')
    
    # Iterate through the values in the specified column
    for value in df[column_name]:
        # Compute Levenshtein distance between the search string and the current value
        distance = levenshtein_distance(search_string, value)
        
        # If the distance is smaller than the current smallest distance, update the closest match
        if distance < smallest_distance:
            smallest_distance = distance
            closest_match = value
            
    return closest_match, smallest_distance

df=pd.read_excel('app\\functions\\Book1.xlsx')
find_closest_match(df,'string_test','name input')