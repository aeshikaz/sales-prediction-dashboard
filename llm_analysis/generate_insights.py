import os
import time
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()
print("API KEY:", os.getenv("GEMINI_API_KEY"))

# Initialize Gemini client (force v1)
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(api_version="v1")
)

# Load dataset
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales_data.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "insights.txt")

df = pd.read_csv(DATA_PATH, encoding="latin1")

# Create summary
summary = df.describe().to_string()

# Prompt
prompt = f"""
You are a business intelligence analyst.

Dataset summary:
{summary}

Generate executive-level business insights suitable for senior management.
Focus on strategic implications, risks, and opportunities.

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

# ✅ Retry + fallback models
models = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite"
]

insights = ""
used_model = None

for m in models:
    try:
        print(f"Trying model: {m}")

        response = client.models.generate_content(
            model=m,
            contents=prompt
        )

        insights = response.text if hasattr(response, "text") else str(response)
        used_model=m
        print(f"Success with {m}")
        break

    except Exception as e:
        print(f"{m} failed:", e)
        time.sleep(2)

# If all models fail
if not insights:
    used_model = "fallback"
    insights = f"""
1. Sales show an average value of {df['Sales'].mean():.2f}, indicating consistent revenue generation.
2. High-value transactions contribute significantly to total revenue.
3. Discounts may be impacting profit margins.
4. Sales variability suggests inconsistent performance.
5. Increasing order size can improve revenue.
"""

if used_model == "fallback":
    insights = "[Fallback Mode]\n\n" + insights
else:
    insights = f"[AI Model: {used_model}]\n\n" + insights

# Save output
os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(insights)

print("\nAI Insights Generated:\n")
print(insights)