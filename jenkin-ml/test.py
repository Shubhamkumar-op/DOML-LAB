from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

if not os.path.exists("model.joblib"):
    raise FileNotFoundError("Run train_model.py first!")

iris = load_iris()

X_train, X_test, y_train, y_test = train_test_split(
    iris.data,
    iris.target,
    test_size=0.2,
    random_state=42
)

model = joblib.load("model.joblib")

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)
print("Testing completed successfully!")

if accuracy < 0.80:
    raise SystemExit("Model test failed!")

print("Model test passed!")