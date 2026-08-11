import time
import requests
import pandas as pd
import os

from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("COURT_LISTENER_API_KEY")

# ----------------------------
# CONFIGURATION
# ----------------------------

RANDOM_SEED = 67

BASE_URL = "https://www.courtlistener.com/api/rest/v4/search/"


headers = {
    "Authorization": f"Token {API_TOKEN}"
}

# ----------------------------
# DOWNLOAD CASES
# ----------------------------

cases = []
counter = 1
url = BASE_URL
params = {
    "q": 'dateFiled:[2025-08-10 TO 2026-08-09]',
    "type": "o"
}

print("Downloading cases...")

while url:

    response = requests.get(
        url,
        params=params,
        headers=headers
    )

    if response.status_code != 200:
        print("Error:", response.status_code)
        print(response.text)
        break

    data = response.json()

    # printing total number of cases
    if url == BASE_URL:
        print(f"{data['count']} total cases found")

    # each response holds 20 different cases
    for curr_case in data["results"]:

        # skip cases that are missing opinions
        if not curr_case["opinions"]:
            continue

        # multiple opinions can exist, we choose the first one
        opinion = curr_case["opinions"][0] 

        cases.append({
            "case_id": counter, 
            "caseName": curr_case.get("caseName"),
            "opinion_id": opinion.get("id"),
            "date_filed": curr_case.get("dateFiled"),
            "court": curr_case.get("court"),
            "absolute_url": curr_case.get("absolute_url"),
            "next_url": data["next"] # to track progress
        })
        
        counter += 1

    print(f"Collected {len(cases)} total cases")

    # periodically saving progress
    if len(cases) % 100 < 20:
        pd.DataFrame(cases).to_csv(
            "courtlistener_sample.csv",
            index=False
        )

    url = data.get("next")
    params = None

    if url:
        time.sleep(3.5)

# final save
df = pd.DataFrame(cases)
df.to_csv("courtlistener_sample.csv", index=False)

print(f"\nTotal cases downloaded: {len(cases)}")