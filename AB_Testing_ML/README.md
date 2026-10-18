# A/B Testing of Machine Learning Models Using Flask

## 1. Introduction

This project demonstrates A/B testing of two Machine Learning models using a Flask web application. The main objective is to compare two models by sending prediction requests to them through a REST API.

The project uses the Iris dataset and two classification algorithms: Decision Tree Classifier and Random Forest Classifier. Each incoming prediction request is randomly assigned to one of the two models, and the selected model returns its prediction.

## 2. How Does the Project Work?

The project follows these steps:

1. **Load the Dataset:** The Iris dataset is loaded from Scikit-learn. It contains flower measurements used to classify flowers into three species.
2. **Split the Data:** The dataset is divided into training data (80%) and testing data (20%).
3. **Train Model A:** A Decision Tree Classifier is trained using the training dataset.
4. **Train Model B:** A Random Forest Classifier is trained using the same training dataset.
5. **Evaluate Both Models:** Accuracy is calculated on the test dataset, and the results are printed in the terminal.
6. **Start the Flask API:** The Flask application provides a `/predict` endpoint that accepts prediction requests in JSON format.
7. **Randomly Assign Requests:** For each request, the application randomly selects Model A or Model B.
8. **Generate the Prediction:** The selected model predicts the Iris flower species and returns the model name and prediction as a JSON response.
9. **Test the API:** The test script sends 10 requests and counts how many requests were handled by each model.

## 3. Project Architecture

```text
          Iris Dataset
                |
                v
        Split the Dataset
         /            \
        v              v
   Model A          Model B
 Decision Tree    Random Forest
         \            /
          v          v
       Flask REST API
          /predict
              |
              v
     Random Model Selection
          /          \
         v            v
     Model A        Model B
         \            /
          v          v
       Prediction Result
              |
              v
       JSON API Response
              |
              v
     Test Script Sends Requests
              |
              v
      Count Requests for A and B
```

## 4. Technologies Used

- Python
- Flask
- Scikit-learn
- Iris Dataset
- REST API
- Requests library

## 5. Project Structure

```text
AB_Testing_ML/
├── app.py
├── test_api.py
└── README.md
```

**app.py:** Loads the dataset, trains both models, calculates their accuracy, starts the Flask API, randomly routes requests, and returns predictions.

**test_api.py:** Sends 10 HTTP POST requests to the prediction API, displays each response, and counts the requests handled by each model.

## 6. Installation

Install the required libraries:

```bash
pip install flask scikit-learn requests
```

## 7. How to Run the Project

### Step 1: Start the Flask Application

Open a terminal inside the `AB_Testing_ML` folder and run:

```bash
python app.py
```

Both models are trained when the application starts. Their accuracy scores are printed in the terminal, and the Flask server starts at:

`http://127.0.0.1:5000`

### Step 2: Test the Prediction API

Open a second terminal in the same project folder and run:

```bash
python test_api.py
```

The script sends 10 requests to the `/predict` endpoint and displays the response from each request.

## 8. API Request Example

The test script sends flower measurements in JSON format:

```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

The four values represent sepal length, sepal width, petal length, and petal width.

## 9. Example API Response

A response may look like this:

```json
{
  "model": "A",
  "prediction": "setosa"
}
```

The selected model can be either `A` (Decision Tree) or `B` (Random Forest). The predicted flower species is returned in the `prediction` field.

## 10. A/B Testing Results

The test script counts how many requests are assigned to each model. For example:

```text
A/B Testing Results
Model A Requests: 5
Model B Requests: 5
```

The counts may vary between runs because requests are assigned randomly. Equal distribution is not guaranteed.

The application also prints the test accuracy of both models when it starts. These accuracy values provide a basic comparison of their classification performance.

## 11. Limitations

- Random routing demonstrates request allocation but does not guarantee an equal number of requests for each model.
- The current test script counts request assignments; it does not compare latency, user outcomes, or statistical significance.
- A more complete A/B experiment would collect sufficient evaluation data and compare suitable performance metrics.

## 12. Conclusion

The project demonstrates how two Machine Learning models can be deployed behind a Flask REST API and randomly assigned incoming prediction requests. It also shows how request counts and model accuracy can be observed to support a basic A/B testing experiment.
