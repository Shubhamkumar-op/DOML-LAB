import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("bugs.csv")

# Select features and target
X = df[
    [
        "lines_of_code",
        "cyclomatic_complexity",
        "developer_experience"
    ]
]

y = df["bug_severity"]

# Convert labels into numbers
le = LabelEncoder()
y = le.fit_transform(y)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save model and label encoder
joblib.dump(model, "bug_model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("Bug severity model trained successfully!")
print("Model saved as bug_model.pkl")
print("Label encoder saved as label_encoder.pkl")