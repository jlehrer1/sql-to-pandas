"""Main module."""

import pandas as pd
import sqlite3
import re
import sqlparse 

from .keywords import _get_sql_keywords

class SQLtoPD:
    def __init__(self, strict=True):
        self.strict = strict

    def _issqlkeyword(self, string: str) -> bool:
        # Get list of SQL reserved keywords
        keywords = _get_sql_keywords()
        return string in keywords

    def _clean_listlike(self, string: str) -> list:
        """Removes commas and semicolons from SQL list-like things. i,e id, number --> ['id', 'number'] """
        cols = []
        for item in string:
            # Check if item is in list, or if user adds ; to the end of the query
            if item[-1] == ',' or item[-1] == ';' or item[-1] == '\n':
                cols.append(item[:-1])
            else:
                cols.append(item)

        return cols

    def _parse_LIMIT(self, df: pd.DataFrame, string: str) -> pd.DataFrame:
        """Parses the LIMIT statement from SQL"""
        return df.head(int(string[1]))
        

    def _parse_ORDER_BY(self, df: pd.DataFrame, string: str) -> pd.DataFrame:
        """Parses SQL ORDER BY <column> ASC/DEC"""
        # Remove 'order', 'by'
        is_asc = True
        string = string[2:]

        if string[-1] == 'desc':
            is_asc = False
            string = string[:-1]
        else:
            if string[-1] == 'asc':
                string = string[:-1]

        ordered_cols = self._clean_listlike(string)

        return df.sort_values(by=ordered_cols, ascending=is_asc)


    def _parse_SELECT(self, df: pd.DataFrame, string: str) -> pd.DataFrame:
        """Parses which columns to use from the DataFrame. Runs in place of SELECT <cols> FROM <df>"""
        cols = []
        if string[1] == '*':
            cols = df.columns.to_list()
        else:
            string = string[string.index('select') + 1: string.index('from')]
            cols = self._clean_listlike(string)
        
        return df[cols]

    def _parse_WHERE(self, df: pd.DataFrame, string: str) -> pd.DataFrame:
        """Parses which rows to use from the DataFrame. Runs in place of WHERE <condition>"""
        # string = string.split()

        # If there is no row select condition return out and continue
        if 'where' not in string:
            return df

        # Get the columns and literal name for building up the string to eval()
        df_cols = df.columns.to_list()
        df_literal_name = f'{df=}'.split('=')[0]

        and_or_ops = {
            'and': '&',
            'or': '|'
        }

        numerical_logical_ops = {
            '!=': '!=',
            '<=': '<=',
            '>=': '>=',
            '>': '>',
            '<': '<',
            '=': '=='
        }

        i = string.index('where') + 1
        conditions = []

        while i != len(string):
            conditions.append(string[i])
            i += 1

        split_conditions = []
        # Go through each word
        for word_idx, word in enumerate(conditions):
            # Then go through each operator and select the first one that is found. The break statement is so that things like != and = are not both recognized -- it should just be !=
            for op in numerical_logical_ops.keys():
                if op in word:
                    word_split_by_op = word.split(sep=op)
                    for spl in word_split_by_op:
                        split_conditions.append(spl)
                    split_conditions.append(op)
                    if word_idx != len(conditions) - 1:
                        split_conditions.append(conditions[word_idx + 1])
                    break
        
        # And remove all newlines from end of the list

        num_and_or_ops_in_splt = sum(
            [split_conditions.count(item) for item in and_or_ops])
        num_cols_in_splt = sum([split_conditions.count(item)
                                for item in df_cols])

        if num_cols_in_splt - num_and_or_ops_in_splt < 1:
            raise RuntimeError(
                'Error: incorrect number of logical operators (AND/OR) in WHERE statement.')

        if num_cols_in_splt - num_and_or_ops_in_splt > 1:
            raise RuntimeError(
                'Error: incorrect number of columns when filtering in WHERE statement.')

        operator_str = ''
        idx = 0

        while idx < len(split_conditions) - 1:
            # df[(df[col]cond cond_val) op (...)]

            # column to filter
            col = ''

            # Pandas equivalent of AND / OR (& / |)
            op = ''

            # The filter operator, like ==, <=, > etc
            cond = ''

            # The filter value
            cond_val = ''

            if split_conditions[idx] in df_cols:
                col = split_conditions[idx]
                cond_val = split_conditions[idx + 1]
                cond = numerical_logical_ops[split_conditions[idx + 2]]

                try:
                    op = and_or_ops[split_conditions[idx + 3]]
                except IndexError:
                    op = ''

            # Make sure column name is in the list of selected columns
            if col not in df.columns:
                raise KeyError('Error: column \'{}\' not found in selected columns'.format(
                    split_conditions[idx]))

            # Make sure there are the correct number of logical operators in relation to the number of conditions

            # Build up df selection using logical operators
            if idx == 0:
                operator_str += '{}.loc[({}[\'{}\']{}{}) {}'.format(
                    df_literal_name, df_literal_name, col, cond, cond_val, op)
            else:
                operator_str += ' ({}[\'{}\']{}{}) {}'.format(
                    df_literal_name, col, cond, cond_val, op)

            idx += 4

        operator_str += ', :]'

        # Then parse it as a Python statement and return the result
        return eval(operator_str)

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
            'select' : self._parse_SELECT,
            'where' : self._parse_WHERE,
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
        string_split = [word[:-1] for word in string_split]

        # First word of each SQL statement so we can know how to process it 
        first_words = [word.split(' ')[0] for word in string_split]
        
        # call each function with its corresponding SQL statement   
        for idx, w in enumerate(first_words):
            df = DML_mapping[w](df=df, string=string_split[idx].split())
        
        return df
