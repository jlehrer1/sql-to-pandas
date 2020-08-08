import pandas as pd
from ..helpers import helpers

def _parse_WHERE(df: pd.DataFrame, string: str) -> pd.DataFrame:
    """Parses which rows to use from the DataFrame. Runs in place of WHERE <condition>"""
    # print('INPUT STR TO WHERE IS: ', string)

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
    try:
        i = string.index('where') + 1
    except ValueError:
        return df
        
    conditions = []

    # Build up conditions until end of statement
    while i != len(string) and not helpers._is_nonlogical_sql_keyword(string[i]):
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
    # print('OPERATOR STRING: ', operator_str)

    # Then parse it as a Python statement and return the result
    return eval(operator_str)