import pandas as pd

df = pd.read_csv("./samples.csv")

print(df.columns.tolist())
print(df["plain_text"].notna().sum())

df.head()

print("Rows:", len(df))
print("Columns:", len(df.columns))
print(df.columns.tolist())
