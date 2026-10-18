
import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "features": [5.1, 3.5, 1.4, 0.2]
}

count = {"A": 0, "B": 0}

for i in range(10):
    response = requests.post(url, json=data)
    result = response.json()

    version = result["model"]
    count[version] += 1

    print("Request", i + 1, result)

print("\nA/B Testing Results")
print("Model A Requests:", count["A"])
print("Model B Requests:", count["B"])
