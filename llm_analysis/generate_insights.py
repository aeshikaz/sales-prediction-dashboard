import os
import pandas as pd
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Load dataset
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales_data.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

OUTPUT_PATH = os.path.join(OUTPUT_DIR, "insights.txt")

df = pd.read_csv(DATA_PATH, encoding="latin1")

# Create summary statistics for the LLM
summary = df.describe().to_string()

# Create prompt for Gemini
prompt = f"""
You are a business analyst.

Here is a statistical summary of a sales dataset:

{summary}

Based on this data:
1. Identify important business insights
2. Detect possible trends
3. Suggest recommendations for improving sales
4. Mention any anomalies or unusual patterns

Explain clearly in bullet points.
"""

# Send to Gemini
response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents=prompt
)

insights = response.text

# Save insights
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(insights)

print("\nAI Insights Generated:\n")
print(insights)