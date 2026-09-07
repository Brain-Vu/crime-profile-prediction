from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="""
You are creating a crime profile.

Based on this crime summary, predict the characteristics of the primary suspect.

Crime summary:
A person entered a home at night through a window and stole several electronic devices.
"""
)

print(response.text)