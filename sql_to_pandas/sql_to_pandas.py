"""Main module."""

import pandas as pd
import sqlite3 

class SQLtoPD:
    def __init__(self, strict=True):
        self.strict = strict

    def parse(df: pd.DataFrame, string: str) -> pd.DataFrame:
        """Parses the SQL string into pandas and returns its results onto the DataFrame"""
        
        _is_valid_sql(string)


    def _is_valid_sql(string):
        """Checks if the given SQL query is valid SQL."""

        pass
