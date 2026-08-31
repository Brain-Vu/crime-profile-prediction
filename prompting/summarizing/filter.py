import pandas as pd

cases = pd.read_csv("checkpoint.csv")

cases[cases["summary"].notna()].to_csv("filtered.csv")