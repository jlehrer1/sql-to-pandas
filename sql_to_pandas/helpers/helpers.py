"""Module containing helper functions that are used in various submodules. Any reusable misc. function can be placed here"""

import pandas as pd 
from .keywords import KEYWORDS

def _get_sql_keywords():
    """Returns a list containing all SQL keywords"""
    return KEYWORDS

def _issqlkeyword(string: str) -> bool:
    """Returns if a given string (word) is a SQL keyword"""
    return string in KEYWORDS

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
