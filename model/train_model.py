import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Load the dataset
dataset_path = os.path.join(os.path.dirname(__file__), 'dataset.csv')
df = pd.read_csv(dataset_path)

# Separate features and target
X = df.drop('label', axis=1)
y = df['label']

# Split into training and test data (optional)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train RandomForest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
model_path = os.path.join(os.path.dirname(__file__), 'cybersecurity_ai_model.pkl')
joblib.dump(model, model_path)

print("✅ Model trained and saved at:", model_path)
