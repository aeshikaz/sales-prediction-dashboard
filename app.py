import os
import sys
import subprocess
import threading
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import pandas as pd

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales_data.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
LLM_DIR = os.path.join(BASE_DIR, "llm_analysis")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

pipeline_status = {"running": False, "log": [], "done": False}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "Empty question"}), 400
    try:
        df = pd.read_csv(DATA_PATH, encoding="latin1")
        data_summary = f"""
Total rows: {len(df)}
Total Sales: {df['Sales'].sum():,.2f}
Total Profit: {df['Profit'].sum():,.2f}
Sales by Region:
{df.groupby('Region')['Sales'].sum().to_string()}
Sales by Category:
{df.groupby('Category')['Sales'].sum().to_string()}
Top 5 Products by Sales:
{df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5).to_string()}
Average Discount: {df['Discount'].mean():.2f}
"""
        prompt = f"""You are a business data analyst.
Here is a summary of a retail sales dataset:
{data_summary}
Answer the user's question using this information.
Rules:
- Answer in 2-4 sentences
- Be concise and clear
- Focus on business insights
User Question: {question}"""
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/outputs/<filename>")
def get_output(filename):
    allowed = ["insights.txt", "predictions.txt", "anomalies.txt", "ai_sales_report.txt"]
    if filename not in allowed:
        return jsonify({"error": "Not found"}), 404
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"content": None, "message": "File not generated yet. Run the pipeline first."})
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return jsonify({"content": content})


@app.route("/api/pipeline/run", methods=["POST"])
def run_pipeline():
    global pipeline_status
    if pipeline_status["running"]:
        return jsonify({"error": "Pipeline already running"}), 400
    pipeline_status = {"running": True, "log": [], "done": False}

    def run():
        scripts = [
            ("Generating Insights", os.path.join(LLM_DIR, "generate_insights.py")),
            ("Running Forecast Engine", os.path.join(LLM_DIR, "forecast_engine.py")),
            ("Detecting Anomalies", os.path.join(LLM_DIR, "anomaly_detection.py")),
            ("Generating Report", os.path.join(LLM_DIR, "report_generator.py")),
        ]
        for label, script in scripts:
            pipeline_status["log"].append(f"▶ {label}...")
            try:
                result = subprocess.run(
                    [sys.executable, script],
                    capture_output=True, text=True, timeout=120
                )
                if result.returncode == 0:
                    pipeline_status["log"].append(f"✓ {label} complete")
                else:
                    pipeline_status["log"].append(f"✗ {label} failed: {result.stderr[:200]}")
            except Exception as e:
                pipeline_status["log"].append(f"✗ {label} error: {str(e)}")
        pipeline_status["running"] = False
        pipeline_status["done"] = True
        pipeline_status["log"].append("Pipeline complete.")

    threading.Thread(target=run, daemon=True).start()
    return jsonify({"status": "started"})


@app.route("/api/pipeline/status")
def pipeline_status_endpoint():
    return jsonify(pipeline_status)


@app.route("/api/stats")
def stats():
    try:
        df = pd.read_csv(DATA_PATH, encoding="latin1")
        return jsonify({
            "total_sales": round(df["Sales"].sum(), 2),
            "total_profit": round(df["Profit"].sum(), 2),
            "total_orders": len(df),
            "avg_discount": round(df["Discount"].mean() * 100, 1),
            "top_region": df.groupby("Region")["Sales"].sum().idxmax(),
            "top_category": df.groupby("Category")["Sales"].sum().idxmax(),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    app.run(debug=True, port=5000)