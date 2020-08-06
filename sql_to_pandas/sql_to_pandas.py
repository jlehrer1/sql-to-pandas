"""Main module."""

import pandas as pd
import sqlite3
import re 

from .keywords import _get_sql_keywords

class SQLtoPD:
    def __init__(self, strict=True):
        self.strict = strict
    
    def _issqlkeyword(self, string: str) -> bool:
        # Get list of SQL reserved keywords
        keywords = _get_sql_keywords()
        return string in keywords

    def _is_valid_sql(self, df: pd.DataFrame, string: str):
        """Checks if the given SQL query is valid SQL syntactically."""
        # Split the string so each word can be parsed
        string = string.split()

        # Extract the not sql keywords (computationally expensive!)
        not_sql_words = [word for word in string if not self._issqlkeyword(word.upper())]

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
        
    def _parse_columns(self, df: pd.DataFrame, string: str) -> pd.DataFrame:
        """Parses which columns to use from the DataFrame. Runs in place of SELECT <cols> FROM <df>"""
        if string[0] == 'select':
            if string[1] == '*':
                pass 
            else:
                cols = []
                i = 1

                # Iterate through all columns being requested
                while string[i] != '\n':
                    cols.append(string[i])
                    i += 1

                # Clean commas from column list styling in SQL
                for idx, item in enumerate(cols):
                    if item[-1] == ',':
                        cols[idx] = item[:-1]
                
                df = df[cols]
        return df

    def _parse_rows(self, df: pd.DataFrame, string: str) -> pd.DataFrame:
        """Parses which rows to use from the DataFrame. Runs in place of WHERE <condition>"""
        # If there is no row select condition return out and continue
        if 'where' not in string:
            return df

        start_parse_location = string.index('where') + 1
        i = start_parse_location

        # Make sure we're still parsing
        conditions = []
        while string[i] != '\n' or i != len(string) - 1:
            conditions.append(i)

        return df

    def parse(self, df: pd.DataFrame, string: str) -> pd.DataFrame:
        """Parses the SQL string into pandas and returns its results onto the DataFrame"""
        self._is_valid_sql(df=df, string=string)

        # Turn the string to lowercase and split into an array for processing
        string_split = re.findall(r'\S+|\n', string.lower())
        
        # Parse columns
        df = self._parse_columns(df, string_split)

        # Parse rows
        df = self._parse_rows(df, string_split)

        return df

