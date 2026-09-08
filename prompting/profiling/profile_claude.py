import os
import json
import pandas as pd

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# =========================
# CLAUDE CLIENT
# =========================

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# =========================
# INPUTS
# =========================

PROMPT = "profiling_prompt.txt"
CSV_FILE = "test.csv"
TEXT_COLUMN = "summary"
OUTPUT_FILE = "claude.csv"

MODEL = "claude-sonnet-5"

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
                        "A brief justification of why these predictions "
                        "were made based on the crime summary and "
                        "reasonable statistical or contextual associations."
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

    "required": [
        "suspect-information"
    ],

    "additionalProperties": False
}

# =========================
# RUN CLAUDE
# =========================

def run_claude(csv_file, text_column, output_file):

    # Resume if output already exists
    if os.path.exists(output_file):
        df = pd.read_csv(output_file)
        print(f"Resuming from existing file: {output_file}")

        if "claude_profile" not in df.columns:
            df["claude_profile"] = ""

    else:
        df = pd.read_csv(csv_file)
        df["claude_profile"] = ""

    total = len(df)

    for i in range(total):

        # Skip already processed rows
        if pd.notna(df.at[i, "claude_profile"]) and df.at[i, "claude_profile"] != "":
            continue

        print(f"\nProcessing {i + 1}/{total}")

        text = df.at[i, text_column]

        try:

            response = client.messages.create(
                model=MODEL,
                max_tokens=2000,

                system=prompt,

                messages=[
                    {
                        "role": "user",
                        "content": f"""
Crime summary:

{text}
"""
                    }
                ],

                output_config={
                    "format": {
                        "type": "json_schema",
                        "schema": SCHEMA
                    }
                }
            )

            # Extract Claude's text response
            result_text = ""

            for block in response.content:
                if block.type == "text":
                    result_text += block.text

            # Parse JSON
            result = json.loads(result_text)

            # Save result
            df.at[i, "claude_profile"] = json.dumps(result)

            # Save progress immediately
            df.to_csv(output_file, index=False)

            print(f"✓ Saved case {i + 1}/{total}")

        except Exception as e:

            print(f"✗ Case {i + 1} failed: {e}")

            # Save progress even if request fails
            df.to_csv(output_file, index=False)

            print("Progress saved. Moving to next case.")

    print("\nFinished!")
    print(f"Results saved to: {output_file}")


# =========================
# START
# =========================

run_claude(
    csv_file=CSV_FILE,
    text_column=TEXT_COLUMN,
    output_file=OUTPUT_FILE
)