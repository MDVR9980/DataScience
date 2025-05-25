import pandas as pd

try:
    df = pd.read_csv('flights.csv')
    print("Columns:", df.columns.tolist())
    print("Head of data:\n", df.head())
except Exception as e:
    print("Error reading CSV:", e)
