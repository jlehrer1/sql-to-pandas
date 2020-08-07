import pandas as pd
import re
import sqlparse

from ..where import where
from ..helpers import helpers

def _SELECT_COUNT(df: pd.DataFrame) -> pd.DataFrame:
    pass

def _SELECT_AVG(df: pd.DataFrame) -> pd.DataFrame:
    pass

def _SELECT_SUM(df: pd.DataFrame) -> pd.DataFrame:
    pass

def _parse_SELECT(df: pd.DataFrame, string: str):
    """Parses which columns to use from the DataFrame. Runs in place of SELECT <cols> FROM <df>"""

    print('SELECT STRING IS: ', string)
    option_map = {
        'count' : _SELECT_COUNT,
        'avg' : _SELECT_AVG,
        'sum' : _SELECT_SUM,
    }
    
    # Get optional keyword if it exists
    checkstring = string[1].split('(')[0]

    if checkstring in option_map.keys():
        df = where._parse_WHERE(df, string)
        # df = option_map[checkstring](df)
    else:
        cols = []
        if string[1] == '*':
            cols = df.columns.to_list()
        else:
            string = string[string.index('select') + 1: string.index('from')]
            cols = helpers._clean_listlike(string)
    
        df = df[cols]

    return df
