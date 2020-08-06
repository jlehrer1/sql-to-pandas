# SQLtoPandas: 

Use SQL queries on Pandas DataFrames.

Are you comfortable with SQL but not Pandas? Or maybe you're comfortable with Pandas but not SQL? Well, this library allows querying of Pandas DataFrames using SQL syntax. Hopefully it will let you learn SQL if you already understand Pandas, or learn how Pandas DataFrames behave if you already know SQL. 

## Usage:
Example usage:
```python3
>>> import sqltopandas
>>> spd = sqltopandas.SQLtoPD()
>>> df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                   columns=['a', 'b', 'c'])
>>> df
   a  b  c
0  1  2  3
1  4  5  6
2  7  8  9

>>> spd.query(df, 'SELECT a from df')
   a
0  1
1  4
2  7

```

## Contributing:
If you have read this far I hope you've found this tool useful. I am always looking to learn more and develop as a programmer, so if you have any ideas or contributions, feel free to write a feature or pull request. 
