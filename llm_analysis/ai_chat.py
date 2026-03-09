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

    if question.lower() == "exit":
        break

    # Prepare dataset summary
    data_summary = df.head(50).to_string()

    prompt = f"""
You are a business data analyst.

Below is a sample of the sales dataset.

{data_summary}

Use this data to answer the user's question.

User Question:
{question}

Provide a clear business explanation.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("\nAI Response:\n")
    print(response.text)
    print("\n----------------------\n")