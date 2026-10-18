
from flask import Flask, request, jsonify
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import random

app = Flask(__name__)

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

model_a = DecisionTreeClassifier(random_state=42)
model_b = RandomForestClassifier(random_state=42)

model_a.fit(X_train, y_train)
model_b.fit(X_train, y_train)

print("Model A Accuracy:", accuracy_score(y_test, model_a.predict(X_test)))
print("Model B Accuracy:", accuracy_score(y_test, model_b.predict(X_test)))

@app.route("/")
def home():
    return "A/B Testing of ML Models is Running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = data["features"]

    version = random.choice(["A", "B"])

    if version == "A":
        model = model_a
    else:
        model = model_b

    prediction = int(model.predict([features])[0])

    return jsonify({
        "model": version,
        "prediction": iris.target_names[prediction]
    })

if __name__ == "__main__":
    app.run(debug=True)
