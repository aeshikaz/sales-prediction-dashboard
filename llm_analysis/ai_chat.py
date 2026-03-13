import os
import pandas as pd
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Setup Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Dataset path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales_data.csv")

# Load dataset
df = pd.read_csv(DATA_PATH, encoding="latin1")

print("\nAI Sales Data Assistant")
print("Type 'exit' to quit.\n")

while True:
    question = input("Ask a question about the sales data: ")

    if question.lower() in ["exit", "quit"]:
        print("Exiting AI assistant.")
        break

    if question.strip() == "":
        print("Please enter a valid question.\n")
        continue

    # Prepare dataset summary
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

    prompt = f"""
You are a business data analyst.

Here is a summary of a retail sales dataset:

{data_summary}

Answer the user's question using this information.

Rules:
- Answer in 1–2 sentences
- Be concise and clear
- Focus on business insights

User Question:
{question}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        print("\nAI Response:\n")
        print(response.text)
        print("\n----------------------\n")

    except Exception as e:
        print("Error generating AI response:", e)