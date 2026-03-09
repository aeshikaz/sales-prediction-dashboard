import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Read previous outputs
with open(os.path.join(OUTPUT_DIR, "insights.txt"), "r", encoding="utf-8") as f:
    insights = f.read()

with open(os.path.join(OUTPUT_DIR, "predictions.txt"), "r", encoding="utf-8") as f:
    predictions = f.read()

with open(os.path.join(OUTPUT_DIR, "anomalies.txt"), "r", encoding="utf-8") as f:
    anomalies = f.read()

prompt = f"""
You are a senior business analyst.

Combine the following information into a professional
AI Sales Intelligence Report.

Insights:
{insights}

Forecast:
{predictions}

Anomalies:
{anomalies}

Structure the report into sections:
1. Key Insights
2. Sales Forecast
3. Detected Anomalies
4. Strategic Recommendations
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

report = response.text


REPORT_PATH = os.path.join(OUTPUT_DIR, "ai_sales_report.txt")

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(report)

print("\nAI SALES REPORT:\n")
print(report)