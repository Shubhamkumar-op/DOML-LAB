from flask import Flask, request, jsonify
import joblib
from sklearn.datasets import load_iris

app = Flask(__name__)

model = joblib.load("model.joblib")
iris = load_iris()


@app.route("/")
def home():
    return "ML Model is deployed successfully!"


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "features" not in data:
        return jsonify({"error": "Please provide features"}), 400

    features = data["features"]

    if len(features) != 4:
        return jsonify({"error": "Exactly 4 features are required"}), 400

    prediction = model.predict([features])[0]

    return jsonify({
        "prediction": iris.target_names[int(prediction)]
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)