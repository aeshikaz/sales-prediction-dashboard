import os
import pandas as pd
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Load dataset
df = pd.read_csv("../data/sales_data.csv", encoding="latin1")

# Convert order date to datetime
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Monthly sales aggregation
monthly_sales = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()

# Calculate growth rate
growth_rate = monthly_sales.pct_change().mean()

# Predict next month sales
last_month_sales = monthly_sales.iloc[-1]
predicted_sales = last_month_sales * (1 + growth_rate)

trend_summary = f"""
Last Month Sales: {last_month_sales:.2f}
Average Growth Rate: {growth_rate:.4f}

Predicted Next Month Sales: {predicted_sales:.2f}
"""

prompt = f"""
You are a business analyst.

Here is sales trend data:

{trend_summary}

Explain the future sales trend and provide business recommendations.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

analysis = response.text

# Save prediction
with open("../outputs/predictions.txt", "w", encoding="utf-8") as f:
    f.write(analysis)

print("\nSales Forecast Analysis:\n")
print(analysis)