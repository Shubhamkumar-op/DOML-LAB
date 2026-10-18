
from datetime import datetime
from airflow.sdk import dag, task


@dag(
    dag_id="simple_ml_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
)
def simple_ml_pipeline():

    @task
    def load_data():
        print("Step 1: Loading ML dataset")
        return [10, 20, 30, 40, 50]

    @task
    def train_model(data):
        print("Step 2: Training ML model")
        average = sum(data) / len(data)
        print("Average:", average)
        return average

    @task
    def evaluate_model(average):
        print("Step 3: Evaluating ML model")
        print("Model evaluation completed")
        print("Average value:", average)

    data = load_data()
    result = train_model(data)
    evaluate_model(result)


simple_ml_pipeline()
