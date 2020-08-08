import pandas as pd
import re
import sqlparse

from ..where import where
from ..helpers import helpers

def _SELECT_COUNT(df: pd.DataFrame) -> pd.DataFrame:
    return df.shape[0]

def _SELECT_AVG(df: pd.DataFrame) -> pd.DataFrame:
    return df.mean()

def _SELECT_SUM(df: pd.DataFrame) -> pd.DataFrame:
    return df.sum()

def _SELECT_MAX(df: pd.DataFrame) -> pd.DataFrame:
    return df.max()

def _SELECT_MIN(df: pd.DataFrame) -> pd.DataFrame:
    return df.min()

def _SELECT_STDEV(df: pd.DataFrame) -> pd.DataFrame:
    return df.std()

def _parse_SELECT(df: pd.DataFrame, string: str):
    """Parses which columns to use from the DataFrame. Runs in place of SELECT <cols> FROM <df>"""

    option_map = {
        'count' : _SELECT_COUNT,
        'avg' : _SELECT_AVG,
        'sum' : _SELECT_SUM,
        'max' : _SELECT_MAX, 
        'min' : _SELECT_MIN,
        'stdev' : _SELECT_STDEV,
    }
    
    # Obtain the possible optional function -- will always be "SELECT <FUNCTION>(col) FROM df"
    checkstring = string[1].replace('(', ' ').replace(')', ' ').split()

    df = where._parse_WHERE(df, string)

    # Get optional keyword and column it will work on if it exists
    if checkstring[0] in option_map.keys():
        if len(checkstring[1:]) > 1:
            raise ValueError('Error: aggregate functions can only be applied to a single column.')

        return option_map[checkstring[0]](df[[checkstring[1]]])
    else:
        cols = []
        if string[1] == '*':
            cols = df.columns.to_list()
        else:
            string = string[string.index('select') + 1: string.index('from')]
            cols = helpers._clean_listlike(string)
    
        df = df[cols]

    return df
