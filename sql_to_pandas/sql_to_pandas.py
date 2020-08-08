"""Main module."""

import pandas as pd
import sqlite3
import re
import sqlparse 

from .select import select
from .helpers import helpers
from .where import where

class SQLtoPD:
    def __init__(self, strict=True):
        self.strict = strict

    def _parse_LIMIT(self, df: pd.DataFrame, string: str) -> pd.DataFrame:
        """Parses the LIMIT statement from SQL"""
        return df.head(int(string[1]))
        
    def _parse_ORDER_BY(self, df: pd.DataFrame, string: str) -> pd.DataFrame:
        """Parses SQL ORDER BY <column> ASC/DEC"""
        is_asc = True

        if string[1] != 'by':
            raise SyntaxError('Error: invalid syntax. Try ORDER BY <col> <ASC/DESC>.')

        # Remove 'order', 'by'
        string = string[2:]

        if string[-1] == 'desc':
            is_asc = False
            string = string[:-1]
        else:
            if string[-1] == 'asc':
                string = string[:-1]

        ordered_cols = helpers._clean_listlike(string)

        return df.sort_values(by=ordered_cols, ascending=is_asc)

    def parse(self, df: pd.DataFrame, string: str) -> pd.DataFrame:
        """
        Parses the SQL string into Pandas and returns its results onto the DataFrame

        Parameters:
        ----------
        df: pd.DataFrame
            The DataFrame to make the SQL query on
        string: str
            The SQL query as a string

        Returns:
        ---------
        df: pd.DataFrame
            The DataFrame after the SQL query has been made

        Example:
        >>> import sqltopandas
        >>> spd = sqltopandas.SQLtoPD()
        >>> df = pd.DataFrame(np.array([[1, 1, 3], [5, 5, 6], [7, 8, 9]]),columns=['a', 'b', 'c'])
        >>> df
        a  b  c
        0  1  1  3
        1  5  5  6
        2  7  8  9
        >>> spd.parse(df, 'SELECT a, b, c FROM df')
        a  b
        0  1  1
        1  5  5
        2  7  8

        >>> spd.parse(df, \"\"\"SELECT a, b, c 
                           FROM df
        ...                WHERE a!=1\"\"\")
        a  b
        1  5  5
        2  7  8
        """

        # SQL statements are categorized into four different types of statements, which are

        # DML (DATA MANIPULATION LANGUAGE)
        # DDL (DATA DEFINITION LANGUAGE)
        # DCL (DATA CONTROL LANGUAGE)
        # TCL (TRANSACTION CONTROL LANGUAGE)

        # All currently handled SQL methods
        DML_mapping = {
            'select' : select._parse_SELECT,
            # Handled in parse_SELECT
            # 'where' : where._parse_WHERE,
            'order' : self._parse_ORDER_BY,
            'limit' : self._parse_LIMIT,
        }

        DDL_mapping = {
            
        }

        # Turn the string to lowercase and split into an array for processing
        string_split = sqlparse.split(string.lower())
        
        # Remove all empty strings (newlines processed etc)
        string_split = list(filter(None, string_split))

        # Remove ; from end of each statement
        string_split = [word[:-1] if word[-1] == ';' else word for word in string_split]

        # First word of each SQL statement so we can know how to process it 
        first_words = [word.split(' ')[0] for word in string_split]
        
        # call each function with its corresponding SQL statement   
        for idx, w in enumerate(first_words):
            df = DML_mapping[w](df=df, string=string_split[idx].split())
        
        return df
