import pandas as pd

cases = pd.read_csv("./summarized_cases.csv")

# cases[cases["summary"].notna()].to_csv("filtered.csv")
cases[cases["summary"].notna()][["case_id", "summary"]].to_csv("simplified.csv")

# df = pd.read_csv("cleaned_cases.csv")
# df = df.loc[:, ~df.columns.str.contains(r"^Unnamed")]

# df = df.head()

# # df.drop(columns="summary", inplace=True)

# df.to_csv("cleaned_cases_shorter.csv", index=False)