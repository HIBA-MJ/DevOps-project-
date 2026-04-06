import pandas as pd
import os
import requests
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# -------- PATHS --------
input_path = "data/input/googleplaystore.csv"
output_path = "data/output/"

os.makedirs(output_path, exist_ok=True)

# -------- LOAD DATA --------
df = pd.read_csv(input_path)
print("Initial shape:", df.shape)

# -------- PREPROCESSING --------
df = df.drop_duplicates()

df['Rating'] = df['Rating'].fillna(df['Rating'].mean())

df['Installs'] = df['Installs'].str.replace('[+,]', '', regex=True)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

df['Price'] = df['Price'].str.replace('$', '', regex=False)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

df = df.dropna(subset=['Installs', 'Price'])

print("After cleaning:", df.shape)

# -------- BASIC METRICS --------
num_rows = len(df)
avg_rating = df['Rating'].mean()

# -------- ML --------
X = df[['Installs']]
y = df['Rating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)

preds = model.predict(X_test)

mse = mean_squared_error(y_test, preds)

# -------- SAVE OUTPUT --------
cleaned_file = output_path + "cleaned_data.csv"
metrics_file = output_path + "metrics.txt"

df.to_csv(cleaned_file, index=False)

with open(metrics_file, "w") as f:
    f.write(f"MSE: {mse}\n")
    f.write(f"Rows after cleaning: {num_rows}\n")
    f.write(f"Average rating: {avg_rating}\n")

print("Files created successfully")

# -------- UPLOAD TO AZURE --------
def upload_to_azure(file_path, sas_url):
    with open(file_path, "rb") as f:
        headers = {"x-ms-blob-type": "BlockBlob"}
        response = requests.put(sas_url, data=f, headers=headers)
        print(f"Upload {file_path} status:", response.status_code)

# 🔥 PUT YOUR REAL SAS URLs HERE
upload_to_azure(cleaned_file, "https://finalprojectstorage.blob.core.windows.net/data/output/cleaned_data.csv?sp=rcw&st=2026-04-06T08:47:08Z&se=2050-04-06T17:02:08Z&sv=2024-11-04&sr=b&sig=g2e60nFm1OOG3BLptiZktFS8my5drvUN%2BJUEIP9B8tM%3D")
upload_to_azure(metrics_file, "https://finalprojectstorage.blob.core.windows.net/data/output/metrics.txt?sp=rcw&st=2026-04-06T08:48:38Z&se=2050-04-06T17:03:38Z&sv=2024-11-04&sr=b&sig=%2F5BF4%2F9BLqXzjJUquYaCx64P2rsIGq9YExhJ4zUauIY%3D")

print("Done!")
print("trigger test")
