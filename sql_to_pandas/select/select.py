import pandas as pd
import re
import sqlparse

def _clean_listlike(string: str) -> list:
    """Removes commas and semicolons from SQL list-like things. i,e id, number --> ['id', 'number'] """
    cols = []
    for item in string:
        # Check if item is in list, or if user adds ; to the end of the query
        if item[-1] == ',' or item[-1] == ';' or item[-1] == '\n':
            cols.append(item[:-1])
        else:
            cols.append(item)

    return cols

def _parse_SELECT(df: pd.DataFrame, string: str):
    """Parses which columns to use from the DataFrame. Runs in place of SELECT <cols> FROM <df>"""
    cols = []
    if string[1] == '*':
        cols = df.columns.to_list()
    else:
        string = string[string.index('select') + 1: string.index('from')]
        cols = _clean_listlike(string)
    
    return df[cols]

# def _SELECT_COUNT(self, df: pd.DataFrame) -> pd.DataFrame:
#     pass

# def _SELECT_AVG(self, df: pd.DataFrame) -> pd.DataFrame:
#     pass

# def _SELECT_SUM(self, df: pd.DataFrame) -> pd.DataFrame:
#     pass

if __name__ == "__main__":
    string = 'SELECT COUNT(id) FROM df;'
    string = string.split()
    print(string)
