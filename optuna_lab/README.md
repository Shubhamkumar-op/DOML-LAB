## Procedure: Hyperparameter Tuning with Optuna and MLflow

**Step 1: Create a Project Folder**

Open Visual Studio Code and open the terminal. Create a project folder named `optuna_lab` and navigate into it.

```powershell
cd D:\DOML-LAB
mkdir optuna_lab
cd optuna_lab
```

**Step 2: Install Required Libraries**

Install Optuna, MLflow, and Scikit-learn using the following command:

```powershell
python -m pip install optuna mlflow scikit-learn
```

These libraries are used for hyperparameter optimization, experiment tracking, and Machine Learning model training.

**Step 3: Start the MLflow Server**

Open a terminal and execute the following command:

```powershell
mlflow server --host 127.0.0.1 --port 5001 --workers 1
```

The MLflow server starts on port 5001. Keep this terminal running during the experiment.

**Step 4: Create the Python File**

Create a Python file named `optuna_mlflow.py` inside the `optuna_lab` folder.

**Step 5: Write the Python Code**

Write the Python program to import the required libraries, load the Iris dataset, and split the dataset into training and testing sets.

**Step 6: Configure MLflow**

Configure MLflow to connect to the running server and create an experiment named `Optuna_Hyperparameter_Tuning`.

**Step 7: Define the Optuna Objective Function**

Define an objective function that selects different values for the `n_estimators` and `max_depth` hyperparameters. Train a Random Forest classifier and calculate its accuracy.

**Step 8: Log Experiments in MLflow**

For each trial, log the selected hyperparameters, model accuracy, and trained model artifact using MLflow.

**Step 9: Run the Optuna Study**

Execute the Python program using the following command in another terminal:

```powershell
python optuna_mlflow.py
```

Optuna performs 20 trials and searches for the hyperparameter combination that produces the highest accuracy.

**Step 10: Display the Best Results**

After the optimization finishes, the program displays the best hyperparameters and the best accuracy in the terminal.

**Step 11: Open the MLflow Dashboard**

Open a web browser and visit:

`http://127.0.0.1:5001`

Open the `Optuna_Hyperparameter_Tuning` experiment and verify the recorded runs, hyperparameters, accuracy metrics, and model artifacts.

**Step 12: Verify the Results**

Confirm that the 20 Optuna trials completed successfully and that their experiment details are available in MLflow. Capture screenshots of the terminal output and MLflow dashboard for the practical record.