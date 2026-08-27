from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_and_save_model():
    os.makedirs("app", exist_ok=True)

    iris = load_iris()
    X, y = iris.data, iris.target

    model = RandomForestClassifier()
    model.fit(X, y)

    joblib.dump(model, "app/model.pkl")

    print("Model trained and saved to app/model.pkl")


if __name__ == "__main__":
    train_and_save_model()