# SQLtoPandas: 

Use SQL queries on Pandas DataFrames.

Are you comfortable with SQL but not Pandas? Or maybe you're comfortable with Pandas but not SQL? Well, this library allows querying of Pandas DataFrames using SQL syntax. Hopefully it will let you learn SQL if you already understand Pandas, or learn how Pandas DataFrames behave if you already know SQL. 

## Requirements and Information: 
Install all required packages through `pip` when it's released, or generate the `conda` dev environment with `conda create --file environment.yml`, and activate with `conda active sqltopandas`. This *does* require Python 3.8 because getting variable literal names with f-string debugging is a critical part of the code infrastructure. I don't think there is a nice way to make that backwards compatible, sadly. 

## Usage:
Example usage:
```python3
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

>>> spd.parse(df, """SELECT a, b, c FROM df
...                  WHERE a!=1
...               """)
   a  b
1  5  5
2  7  8

```

## Obvious edge cases 
DataFrame column names, as well as DataFrame names, cannot be SQL keywords. For example, a column name with "SELECT" or "select" will throw an error.

## Contributing:
If you have read this far I hope you've found this tool useful. I am always looking to learn more and develop as a programmer, so if you have any ideas or contributions, feel free to write a feature or pull request. 
