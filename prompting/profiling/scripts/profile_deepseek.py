import os
import json
import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# =========================
# DEEPSEEK CLIENT
# =========================

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# =========================
# INPUTS
# =========================

PROMPT = "profiling_prompt.txt"
CSV_FILE = "test.csv"
TEXT_COLUMN = "summary"
OUTPUT_FILE = "deepseek.csv"

# =========================
# LOAD PROMPT
# =========================

with open(PROMPT, "r", encoding="utf-8") as file:
    prompt = file.read()

# =========================
# JSON SCHEMA
# =========================

SCHEMA = {
    "type": "object",
    "properties": {
        "suspect-information": {
            "type": "object",
            "properties": {
                "age": {
                    "type": "string",
                    "enum": [
                        "0-18y",
                        "19-24y",
                        "25-29y",
                        "30-39y",
                        "40-49y",
                        "50+y"
                    ]
                },
                "sex": {
                    "type": "string",
                    "enum": [
                        "Male",
                        "Female"
                    ]
                },
                "economic-status": {
                    "type": "string",
                    "enum": [
                        "Lower",
                        "Middle",
                        "Upper"
                    ]
                },
                "educational-level": {
                    "type": "string",
                    "enum": [
                        "High school",
                        "Bachelor's",
                        "Above Bachelor's"
                    ]
                },
                "reasoning": {
                    "type": "string",
                    "description": (
                        "A brief justification of why you made your choices."
                    )
                }
            },
            "required": [
                "age",
                "sex",
                "economic-status",
                "educational-level",
                "reasoning"
            ],
            "additionalProperties": False
        }
    },
    "required": ["suspect-information"],
    "additionalProperties": False
}


# =========================
# RUN DEEPSEEK
# =========================

def run_deepseek(csv_file, text_column, output_file):

    # -------------------------
    # Resume from existing file
    # -------------------------

    if os.path.exists(output_file):
        df = pd.read_csv(output_file)
        print(f"Resuming from existing file: {output_file}")

        # Make sure output column exists
        if "deepseek_profile" not in df.columns:
            df["deepseek_profile"] = None

    else:
        df = pd.read_csv(csv_file)
        df["deepseek_profile"] = None

    total = len(df)

    # -------------------------
    # Process cases
    # -------------------------

    for i in range(total):

        # Skip already completed cases
        if pd.notna(df.at[i, "deepseek_profile"]):
            continue

        print(f"\nProcessing {i + 1}/{total}")

        text = df.at[i, text_column]

        try:

            response = client.responses.create(
                model="deepseek-v4-flash",

                input=f"""
                    {prompt}

                    Crime summary:
                    {text}
                    """,

                text={
                    "format": {
                        "type": "json_schema",
                        "name": "suspect_profile",
                        "schema": SCHEMA
                    }
                }
            )

            # -------------------------
            # Get model output
            # -------------------------

            result = json.loads(response.output_text)

            # -------------------------
            # Save result
            # -------------------------

            df.at[i, "deepseek_profile"] = json.dumps(result)

            # Save immediately
            df.to_csv(output_file, index=False)

            print(f"✓ Saved case {i + 1}/{total}")

        except Exception as e:

            print(f"✗ Case {i + 1} failed: {e}")

            # Save progress even after failure
            df.to_csv(output_file, index=False)

            print("Progress saved. Moving to next case.")

    print("\nFinished!")
    print(f"Results saved to: {output_file}")


# =========================
# START
# =========================

run_deepseek(
    csv_file=CSV_FILE,
    text_column=TEXT_COLUMN,
    output_file=OUTPUT_FILE
)