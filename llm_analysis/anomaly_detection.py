import os
import time
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()
print("API KEY:", os.getenv("GEMINI_API_KEY"))

# ✅ Force API v1
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(api_version="v1")
)

# Load dataset
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales_data.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "anomalies.txt")

df = pd.read_csv(DATA_PATH, encoding="latin1")

# 🔍 Simple anomaly detection using IQR
Q1 = df["Sales"].quantile(0.25)
Q3 = df["Sales"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

anomalies = df[(df["Sales"] < lower_bound) | (df["Sales"] > upper_bound)]

# Create summary
summary = f"""
Total Records: {len(df)}
Anomalies Found: {len(anomalies)}
Lower Bound: {lower_bound:.2f}
Upper Bound: {upper_bound:.2f}
"""

# Prompt
prompt = f"""
You are a data analyst.

Here is anomaly detection summary:

{summary}

Tasks:
1. Explain what these anomalies indicate
2. Identify possible causes
3. Suggest actions to reduce risk

Keep it concise and business-focused.
"""

# ✅ Retry + fallback models
models = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite"
]

analysis = ""
used_model = None

for m in models:
    try:
        print(f"Trying model: {m}")

        response = client.models.generate_content(
           model=m,
            contents=prompt
        )

        analysis = response.text if hasattr(response, "text") else str(response)
        used_model=m
        print(f"Success with {m}")
        break

    except Exception as e:
        print(f"{m} failed:", e)
        time.sleep(2)

# If all fail
if not analysis:
    used_model = "fallback"
    analysis = f"""
1. {len(anomalies)} anomalies detected indicating irregular sales patterns.
2. High values may indicate bulk purchases or seasonal spikes.
3. Low values may indicate discounts or weak demand.
4. High variability suggests inconsistent performance.
5. Monitoring anomalies can improve business decision-making.
"""

if used_model == "fallback":
    analysis = "[Fallback Mode]\n\n" + analysis
else:
    analysis = f"[AI Model: {used_model}]\n\n" + analysis

# Save output
os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(analysis)

print("\nAnomaly Analysis:\n")
print(analysis)