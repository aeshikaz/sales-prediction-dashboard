import os
import time
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()
print("API KEY:", os.getenv("GEMINI_API_KEY"))

# ✅ Force API v1 (VERY IMPORTANT)
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(api_version="v1")
)

# Load dataset
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales_data.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "predictions.txt")

df = pd.read_csv(DATA_PATH, encoding="latin1")

# Convert date
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Monthly aggregation
monthly_sales = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()

# Growth rate
growth_rate = monthly_sales.pct_change().mean()

# Prediction
last_month_sales = monthly_sales.iloc[-1]
predicted_sales = last_month_sales * (1 + growth_rate)

trend_summary = f"""
Last Month Sales: {last_month_sales:.2f}
Average Growth Rate: {growth_rate:.4f}
Predicted Next Month Sales: {predicted_sales:.2f}
"""

# Prompt
prompt = f"""
You are a business analyst.

Here is sales trend data:

{trend_summary}

Tasks:
1. Explain the future sales trend
2. Identify risks or opportunities
3. Suggest 2–3 business recommendations

Keep it concise and actionable.
"""

# ✅ Retry + fallback models (same as insights)
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
        used_model = m
        print(f"Success with {m}")
        break

    except Exception as e:
        print(f"{m} failed:", e)
        time.sleep(2)

# If all models fail
if not analysis:
    used_model = "fallback"
    analysis = f"""
Sales are expected to reach approximately {predicted_sales:.2f} next month.
The average growth rate indicates a stable trend.
Businesses should focus on improving margins and targeting high-value customers.
"""

if used_model == "fallback":
    analysis = "[Fallback Mode]\n\n" + analysis
else:
    analysis = f"[AI Model: {used_model}]\n\n" + analysis

# Save output
os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(analysis)

print("\nSales Forecast Analysis:\n")
print(analysis)