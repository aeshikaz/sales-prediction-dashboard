# AI Sales Intelligence Dashboard

An AI-powered sales analytics platform that combines Python data analysis, Google Gemini LLM, and Tableau visualization to generate automated business insights, sales forecasts, anomaly detection, and natural language query responses from sales data.

---

## Project Overview

This project demonstrates how Large Language Models (LLMs) can be integrated with data analytics pipelines to provide intelligent business insights.

The system analyzes historical sales data and automatically generates:

- Business insights
- Sales trend predictions
- Anomaly detection explanations
- Strategic recommendations
- Natural language answers to business questions

The results are visualized in an interactive Tableau dashboard.

---

## System Architecture

Sales Dataset (CSV)
↓
Python Data Processing (Pandas)
↓
Analytics Layer
• Statistical Analysis
• Trend Calculation
• Anomaly Detection

↓

Gemini AI Intelligence Layer
• Business Insight Generation
• Forecast Explanation
• Query Assistant

↓

Output Files
• insights.txt
• predictions.txt
• anomalies.txt
• ai_sales_report.txt

↓

Tableau Dashboard


---

## Features

### 1️⃣ AI Business Insight Generation
Automatically analyzes sales data and generates key insights such as:

- Top-performing regions
- Category profitability
- Discount impact
- Sales trends

---

### 2️⃣ Sales Forecast Prediction

Python calculates growth trends and Gemini explains the future forecast with business recommendations.

Example output:

---

## Features

### 1️⃣ AI Business Insight Generation
Automatically analyzes sales data and generates key insights such as:

- Top-performing regions
- Category profitability
- Discount impact
- Sales trends

---

### 2️⃣ Sales Forecast Prediction

Python calculates growth trends and Gemini explains the future forecast with business recommendations.

Example output:
Sales are expected to increase by 8–10% next month due to strong growth in the Technology category.


---

### 3️⃣ AI Anomaly Detection

The system automatically detects unusual patterns such as:

- extreme sales spikes
- negative profit margins
- excessive discounts

Gemini explains potential business causes.

---

### 4️⃣ Natural Language Query Assistant

Users can ask questions about the data:

Example:

---

### 3️⃣ AI Anomaly Detection

The system automatically detects unusual patterns such as:

- extreme sales spikes
- negative profit margins
- excessive discounts

Gemini explains potential business causes.

---

### 4️⃣ Natural Language Query Assistant

Users can ask questions about the data:

Example:
Which region generates the highest revenue?


The AI analyzes the dataset and provides a business explanation.

---

### 5️⃣ AI Business Report Generator

The system combines insights, forecasts, and anomaly analysis into a professional AI-generated business report.

---

## Technologies Used

Python  
Pandas  
Google Gemini LLM  
Tableau  
GitHub  

---

## Project Structure

sales-prediction-dashboard
│
├── data
│ └── sales_data.csv
│
├── llm_analysis
│ ├── generate_insights.py
│ ├── query_ai.py
│ ├── forecast_engine.py
│ ├── anomaly_detection.py
│ └── report_generator.py
│
├── outputs
│ ├── insights.txt
│ ├── predictions.txt
│ ├── anomalies.txt
│ └── ai_sales_report.txt
│
├── tableau
│ └── dashboard.twbx
│
├── requirements.txt
└── README.md

