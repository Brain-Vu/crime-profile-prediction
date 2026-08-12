import time
import requests
import pandas as pd
import os

from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("COURT_LISTENER_API_KEY")
BASE_URL = "https://www.courtlistener.com/api/rest/v4/opinions"

# ----------------------------
# CONFIGURATION
# ----------------------------

RANDOM_SEED = 67
SAMPLE_SIZE = 165

file = input("Please input the name of the csv: ")
cases_DF = pd.read_csv(f"./data/{file}")

headers = {
    "Authorization": f"Token {API_TOKEN}"
}

# ----------------------------
# RANDOM SAMPLE
# ----------------------------

sample_DF = cases_DF.sample(n=SAMPLE_SIZE, random_state=RANDOM_SEED)
print(sample_DF)

# ----------------------------
# GETTING PLAIN TEXT DESCRIPTIONS
# ----------------------------

for case in sample_DF.itertuples(index=True):
  id = case.case_id
  index = case.Index

  response = requests.get(
    f"{BASE_URL}/{id}",
    headers=headers
  )

  # error handling
  if response.status_code != 200:
      print("Error:", response.status_code)
      break

  opinion_data = response.json()
  sample_DF.loc[index, "plain_text"] = opinion_data["plain_text"]

  time.sleep(3.4)

# ----------------------------
# SAVE FILES
# ----------------------------

sample_DF.to_csv("samples.csv", index=False)
print(f"\nSaved {SAMPLE_SIZE} randomly selected cases.")