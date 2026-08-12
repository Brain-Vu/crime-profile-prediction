import random
import pandas as pd

# ----------------------------
# CONFIGURATION
# ----------------------------

RANDOM_SEED = 67
SAMPLE_SIZE = 165

file = input("Please input the name of the csv: ")
casesDF = pd.read_csv(f"./data/{file}")

# ----------------------------
# RANDOM SAMPLE
# ----------------------------

sampleDF = casesDF.sample(n=SAMPLE_SIZE, random_state=RANDOM_SEED)
print(sampleDF)

# ----------------------------
# SAVE FILES
# ----------------------------

# df.to_csv("courtlistener_sample.csv", index=False)

# print(f"\nSaved {sample_size} randomly selected cases.")