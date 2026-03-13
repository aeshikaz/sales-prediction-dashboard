import os
import pandas as pd
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Load dataset
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales_data.csv")

df = pd.read_csv(DATA_PATH, encoding="latin1")

# Convert dataset summary to text
data_summary = df.describe().to_string()

print("\nAsk a question about the sales data.")
user_question = input("Question: ")

prompt = f"""
You are a data analyst.

Here is a statistical summary of a sales dataset:

{data_summary}

Answer this user question clearly and concisely:

{user_question}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print("\nAI Answer:\n")
print(response.text)