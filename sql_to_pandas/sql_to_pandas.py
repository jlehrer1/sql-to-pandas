"""Main module."""

import pandas as pd
import sqlite3

from . import keywords as k

class SQLtoPD:
    def __init__(self, strict=True):
        self.strict = strict
    
    def _is_valid_sql(self, df: pd.DataFrame, string: str):
        """Checks if the given SQL query is valid SQL syntactically."""
        # Get list of SQL reserved keywords
        keywords = k._get_sql_keywords()

        # Split the string so each word can be parsed
        string = string.split()

        # Extract the not sql keywords (computationally expensive!)
        not_sql_words = [word for word in string if word.upper() not in keywords]
        
        # Then use set differencing to get the keywords
        sql_words = list(set(string).difference(set(not_sql_words)))
        sql_words = [word.lower() for word in sql_words]

        # Check if dataframe name is in the word list (DEBUG THIS FIRST)
        df_literal_name = f'{df=}'.split('=')[0]
        if df_literal_name not in not_sql_words:
            raise ValueError('Error: The DataFrame name is incorrect. Please use the literal variable name in referencing it, or see the documentation for more help')
        
        # Make sure "WHERE <condition>" is matching in the dataframe columns
        if 'where' in sql_words:
            possible_col = sql_words[sql_words.index('where') + 1]
            if possible_col not in df.columns.to_list():
                raise ValueError('Error: {} column not found'.format(possible_col))
        





    def parse(self, df: pd.DataFrame, string: str) -> pd.DataFrame:
        """Parses the SQL string into pandas and returns its results onto the DataFrame"""
        
        self._is_valid_sql(df, string)

