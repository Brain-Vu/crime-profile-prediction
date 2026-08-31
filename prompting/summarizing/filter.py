import pandas as pd

cases = pd.read_csv("./results/summarized_cases.csv")

cases[cases["summary"].notna()].to_csv("filtered.csv")
cases[cases["summary"].notna()][["case_id", "summary"]].to_csv("simplified.csv")