import os
import pandas as pd
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Load dataset
df = pd.read_csv("../data/sales_data.csv", encoding="latin1")

# Detect anomalies using simple statistical method
sales_mean = df["Sales"].mean()
sales_std = df["Sales"].std()

threshold_high = sales_mean + 2 * sales_std
threshold_low = sales_mean - 2 * sales_std

anomalies = df[(df["Sales"] > threshold_high) | (df["Sales"] < threshold_low)]

anomaly_summary = anomalies.describe().to_string()

prompt = f"""
You are a business analyst.

The following statistics represent unusual sales values detected in a dataset.

{anomaly_summary}

Explain possible business reasons for these anomalies
and suggest what the company should investigate.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

analysis = response.text

with open("../outputs/anomalies.txt", "w", encoding="utf-8") as f:
    f.write(analysis)

print("\nAI Anomaly Analysis:\n")
print(analysis)