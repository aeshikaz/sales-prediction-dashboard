import os
import pandas as pd
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Load dataset
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales_data.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

OUTPUT_PATH = os.path.join(OUTPUT_DIR, "anomalies.txt")

df = pd.read_csv(DATA_PATH, encoding="latin1")

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

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(analysis)

print("\nAI Anomaly Analysis:\n")
print(analysis)