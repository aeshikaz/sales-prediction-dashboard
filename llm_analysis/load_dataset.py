import pandas as pd

# Load the dataset
df = pd.read_csv("../data/sales_data.csv", encoding="latin1")

print("Dataset loaded successfully!\n")

# Show first 5 rows
print("First 5 rows:\n")
print(df.head())

print("\n----------------------\n")

# Show dataset information
print("Dataset Info:\n")
print(df.info())

print("\n----------------------\n")

# Show statistical summary
print("Dataset Statistics:\n")
print(df.describe())