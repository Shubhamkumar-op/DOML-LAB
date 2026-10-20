import optuna
import mlflow
import mlflow.sklearn

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# Connect to MLflow server
mlflow.set_tracking_uri("http://127.0.0.1:5001")
mlflow.set_experiment("Optuna_Hyperparameter_Tuning")


# Load the Iris dataset
X, y = load_iris(return_X_y=True)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Define the Optuna objective function
def objective(trial):

    # Select hyperparameters automatically
    n_estimators = trial.suggest_int(
        "n_estimators", 10, 200
    )

    max_depth = trial.suggest_int(
        "max_depth", 2, 20
    )

    # Create the model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, predictions)

    # Log parameters, metrics, and model in MLflow
    with mlflow.start_run(
        run_name=f"Trial_{trial.number}"
    ):
        mlflow.log_param(
            "n_estimators", n_estimators
        )

        mlflow.log_param(
            "max_depth", max_depth
        )

        mlflow.log_metric(
            "accuracy", accuracy
        )

        # Fix for the skops trusted-type error.
        # This explicitly trusts the tree type used by
        # the Random Forest model created in this experiment.
        mlflow.sklearn.log_model(
            model,
            name="model",
            skops_trusted_types=[
                "sklearn.tree._tree.Tree"
            ]
        )

    print(
        f"Trial {trial.number}: "
        f"n_estimators={n_estimators}, "
        f"max_depth={max_depth}, "
        f"accuracy={accuracy:.4f}"
    )

    return accuracy


# Create an Optuna study
study = optuna.create_study(
    direction="maximize"
)

# Run 20 optimization trials
study.optimize(
    objective,
    n_trials=20
)


# Display the best results
print("\nOptimization Completed!")
print("Best Parameters:", study.best_params)
print("Best Accuracy:", study.best_value)

print("\nAll trial results:")
print(study.trials_dataframe())

print("\nExperiments logged successfully in MLflow!")