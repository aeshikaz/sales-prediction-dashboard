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
You are a business intelligence analyst.

Dataset summary:
{summary}

Generate concise business insights.

Constraints:
- Maximum 5 insights
- Each insight must be 1 sentence
- Focus on actionable business meaning
- Avoid long explanations

Format:
1.
2.
3.
4.
5.
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