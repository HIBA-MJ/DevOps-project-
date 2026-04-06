import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import os

# Paths
input_path = "data/input/googleplaystore.csv"
output_path = "data/output/"

os.makedirs(output_path, exist_ok=True)

# Load dataset
df = pd.read_csv(input_path)

print("Initial shape:", df.shape)

# --- PREPROCESSING ---
df = df.drop_duplicates()

df['Rating'] = df['Rating'].fillna(df['Rating'].mean())

df['Installs'] = df['Installs'].str.replace('[+,]', '', regex=True)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

df['Price'] = df['Price'].str.replace('$', '', regex=False)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

df = df.dropna(subset=['Installs', 'Price'])

print("After cleaning:", df.shape)

# --- BASIC METRICS (REQUIRED) ---
num_rows = len(df)
avg_rating = df['Rating'].mean()

# --- ML ---
X = df[['Installs']]
y = df['Rating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)

preds = model.predict(X_test)

mse = mean_squared_error(y_test, preds)

# --- SAVE OUTPUT ---
df.to_csv(output_path + "cleaned_data.csv", index=False)

with open(output_path + "metrics.txt", "w") as f:
    f.write(f"MSE: {mse}\n")
    f.write(f"Rows after cleaning: {num_rows}\n")
    f.write(f"Average rating: {avg_rating}\n")

print("Done!")

