# Automated ML Pipeline Using Apache Airflow

## 1. Introduction

This project demonstrates how to automate and manage a Machine Learning workflow using Apache Airflow. Apache Airflow is an open-source workflow orchestration platform that allows users to define, execute, and monitor tasks in a specific order.

The project creates a simple pipeline containing three tasks: loading sample data, processing the data, and evaluating the result. These tasks are defined in an Airflow DAG and executed through the Airflow web interface.

## 2. How Does the Project Work?

The pipeline works in the following sequence:

1. **Load Data:** The `load_data` task creates a sample dataset containing five values: `[10, 20, 30, 40, 50]`.
2. **Pass Data to the Next Task:** Airflow passes the returned dataset to the next task using its task dependency mechanism.
3. **Process Data:** The `train_model` task calculates the average of all the values in the dataset.
4. **Calculate the Result:** The average is calculated as `(10 + 20 + 30 + 40 + 50) / 5 = 30.0`.
5. **Evaluate the Result:** The `evaluate_model` task prints the completion message and the calculated average.
6. **Monitor Execution:** The Airflow web interface displays the DAG and the status of each task. Successful tasks appear as completed in the Grid view.

## 3. Project Architecture

```text
          Start Airflow
                |
                v
       simple_ml_pipeline DAG
                |
                v
           load_data
                |
                v
          Sample Dataset
     [10, 20, 30, 40, 50]
                |
                v
          train_model
                |
                v
        Calculate Average
             30.0
                |
                v
        evaluate_model
                |
                v
       Workflow Completed
```

## 4. Technologies Used

- Python
- Apache Airflow 3.1.0
- Docker Desktop
- Docker container runtime
- Airflow Web Interface

## 5. Project Structure

```text
Airflow_Lab/
├── dags/
│   └── ml_pipeline.py
├── docker-compose.yaml
└── README.md
```

**`dags/ml_pipeline.py`:** Contains the DAG definition and the three Python tasks.

**`docker-compose.yaml`:** Contains the multi-service configuration