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

    def _clean_listlike(self, string: str) -> list:
        """Removes commas from SQL list-like things, used in parsing SELECT statements. i,e id, number --> ['id', 'number'] """
        cols = []
        i = 1

        # Iterate through all columns being requested
        while string[i] != '\n' and string[i + 1] != 'from':
            cols.append(string[i])
            i += 1

        # Clean commas from column list styling in SQL
        for idx, item in enumerate(cols):
            if item[-1] == ',':
                cols[idx] = item[:-1]

        return cols

    def _is_valid_sql(self, df: pd.DataFrame, string: str):
        """Checks if the given SQL query is valid SQL syntactically."""

        # Extract the not sql keywords (computationally expensive!)
        not_sql_words = [
            word for word in string if not self._issqlkeyword(word.upper())]

        # Then use set differencing to get the keywords
        sql_words = list(set(string).difference(set(not_sql_words)))
        sql_words = [word.lower() for word in sql_words]

        # Check if dataframe name is in the word list (DEBUG THIS FIRST)
        df_literal_name = f'{df=}'.split('=')[0]
        if df_literal_name not in not_sql_words:
            raise ValueError(
                'Error: The DataFrame name is incorrect. Please use the literal variable name in referencing it, or see the documentation for more help')

        # Make sure "WHERE <condition>" is matching in the dataframe columns
        if 'where' in sql_words:
            # String one after "WHERE"
            possible_col_idx = string.index('where') + 1
            ok_logical_ops = ['and', 'or']
            not_logical_sql_keywords = list(
                set(sql_words).difference(set(ok_logical_ops)))

            # while string[i]

            # if possible_col not in df.columns.to_list():
            #     raise ValueError('Error: {} column not found'.format(possible_col))

    def _parse_SELECT(self, df: pd.DataFrame, string: str) -> pd.DataFrame:
        """Parses which columns to use from the DataFrame. Runs in place of SELECT <cols> FROM <df>"""
        if string[1] == '*':
            pass
        else:
            cols = self._clean_listlike(string)
            df = df[cols]
        return df

    def _parse_WHERE(self, df: pd.DataFrame, string: str) -> pd.DataFrame:
        """Parses which rows to use from the DataFrame. Runs in place of WHERE <condition>"""
        # If there is no row select condition return out and continue
        if 'where' not in string:
            return df

        ok_logical_ops = {
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

        df_cols = df.columns.to_list()
        df_literal_name = f'{df=}'.split('=')[0]

        operator_str = ''
        idx = 0

        while idx < len(split_conditions) - 1:
            col = ''
            op = ''
            cond = ''
            cond_val = ''

            if split_conditions[idx] in df_cols:
                col = split_conditions[idx]
                cond_val = split_conditions[idx + 1]
                cond = numerical_logical_ops[split_conditions[idx + 2]]
                try:
                    op = ok_logical_ops[split_conditions[idx + 3]]
                except IndexError:
                    op = ''

            # Build up df selection using logical operators
            if idx == 0:
                operator_str += '{}.loc[({}[\'{}\']{}{}) {}'.format(
                    df_literal_name, df_literal_name, col, cond, cond_val, op)
            else:
                operator_str += ' ({}[\'{}\']{}{}) {}'.format(
                    df_literal_name, col, cond, cond_val, op)

            idx += 4

        operator_str += ']'

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

        >>> spd.parse(df, 'SELECT a, b, c FROM df
        ...                WHERE a!=1')
        a  b
        1  5  5
        2  7  8
        """

        # Turn the string to lowercase and split into an array for processing
        string_split = re.findall(r'\S+|\n', string.lower())

        # Make sure SQL is valid
        self._is_valid_sql(df=df, string=string_split)

        # Parse columns
        df = self._parse_SELECT(df=df, string=string_split)

        # Parse rows
        df = self._parse_WHERE(df=df, string=string_split)

        return df
