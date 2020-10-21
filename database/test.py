import DataBase
import pandas as pd
import sqlite3

conn = sqlite3.connect("gastrotommy.db")
df = pd.read_sql_query("SELECT * FROM restaurant;", conn)

print(df)

df.to_csv("testdata.csv")