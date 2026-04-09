import os
import time
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

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

INSIGHTS_PATH = os.path.join(OUTPUT_DIR, "insights.txt")
PREDICTIONS_PATH = os.path.join(OUTPUT_DIR, "predictions.txt")
ANOMALIES_PATH = os.path.join(OUTPUT_DIR, "anomalies.txt")

REPORT_PATH = os.path.join(OUTPUT_DIR, "final_report.txt")

# Read files safely
def read_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "No data available."


insights = read_file(INSIGHTS_PATH)
forecast = read_file(PREDICTIONS_PATH)
anomalies = read_file(ANOMALIES_PATH)

# Prompt
prompt = f"""
You are a senior business analyst.

Combine the following into a professional business report:

--- Insights ---
{insights}

--- Forecast ---
{forecast}

--- Anomaly Analysis ---
{anomalies}

Format:
- Title
- Executive Summary
- Key Insights
- Forecast Analysis
- Risk & Anomaly Analysis
- Recommendations
- Conclusion

Requirements:
- Create a structured report
- Include headings
- Keep it concise and professional
- Add a short conclusion
"""

# Retry + fallback models
models = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite"
]

final_report = ""
used_model=None

for m in models:
    try:
        print(f"Trying model: {m}")

        response = client.models.generate_content(
            model=m,
            contents=prompt
        )

        final_report = response.text if hasattr(response, "text") else str(response)
        used_model=m
        print(f"Success with {m}")
        break

    except Exception as e:
        print(f"{m} failed:", e)
        time.sleep(2)

# ✅ Fallback report (VERY IMPORTANT)
if not final_report:
    used_model = "fallback"
    final_report = f"""
SALES ANALYSIS REPORT

--- INSIGHTS ---
{insights}

--- FORECAST ---
{forecast}

--- ANOMALY ANALYSIS ---
{anomalies}

--- CONCLUSION ---
The business shows variable performance with opportunities for optimization.
"""

if used_model == "fallback":
    final_report = "[Fallback Mode]\n\n" + final_report
else:
    final_report = f"[AI Model: {used_model}]\n\n" + final_report

# Save report
os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(final_report)

print("\nFINAL REPORT GENERATED:\n")
print(final_report)