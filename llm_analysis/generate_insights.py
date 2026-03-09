import pandas as pd

# Load dataset
df = pd.read_csv("../data/sales_data.csv", encoding="latin1")

# Basic business metrics
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()

top_region = df.groupby("Region")["Sales"].sum().idxmax()
top_category = df.groupby("Category")["Sales"].sum().idxmax()

summary = f"""
Sales Summary:

Total Sales: {total_sales}
Total Profit: {total_profit}

Top Performing Region: {top_region}
Top Performing Category: {top_category}
"""

print(summary)

# Save insights to file
with open("../outputs/insights.txt", "w") as f:
    f.write(summary)

print("Insights saved to outputs/insights.txt")