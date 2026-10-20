Experiment-7: Data Versioning with DVC
Aim
To use DVC (Data Version Control) to track versions of datasets and trained Machine Learning models, and integrate DVC with Git for ML lifecycle version control.
Theory
Git versions source code and small text files. Machine Learning projects also use datasets and trained models that change during experiments. DVC tracks data and model files and stores lightweight .dvc metadata files in Git. The actual files are held in DVC's local cache or a configured remote storage.

In this experiment, Git tracks the code and DVC metadata, while DVC tracks the dataset and model files. The dataset is changed from Version 1 (10 records) to Version 2 (15 records), then an earlier version is restored using Git metadata and dvc checkout.
Project Structure
DOML-LAB/
└── dvc_lab/
    ├── .dvc/
    ├── .dvcignore
    ├── .gitignore
    ├── bugs.csv
    ├── bugs.csv.dvc
    ├── train.py
    ├── bug_model.pkl
    ├── bug_model.pkl.dvc
    ├── label_encoder.pkl
    ├── label_encoder.pkl.dvc
    └── README.md
Requirements
- Python
- Git
- DVC
- pandas
- scikit-learn
- joblib
- Visual Studio Code or another code editor
Procedure
Step 1: Create or open the project folder
This practical is inside the existing DOML-LAB Git repository.
cd D:\DOML-LAB
mkdir dvc_lab
cd dvc_lab
If the folder already exists, just run:
cd D:\DOML-LAB\dvc_lab
Step 2: Install DVC
python -m pip install dvc
dvc --version
Step 3: Initialize DVC
Because dvc_lab is inside an existing Git repository, initialize DVC in the subdirectory:
dvc init --subdir
Step 4: Create Dataset Version 1
Create bugs.csv with the following data:
bug_id,lines_of_code,cyclomatic_complexity,developer_experience,bug_severity
B001,120,5,2,Low
B002,450,15,1,High
B003,300,10,3,Medium
B004,700,20,1,High
B005,200,8,4,Low
B006,500,18,2,High
B007,350,12,3,Medium
B008,150,6,5,Low
B009,600,22,1,High
B010,280,9,4,Medium
Step 5: Track the dataset using DVC
dvc add bugs.csv
This creates bugs.csv.dvc and puts the data in the local DVC cache. Git tracks the .dvc metadata rather than the dataset's full contents.
Step 6: Commit the initial dataset version
git add .dvc/.gitignore .dvc/config .dvcignore .gitignore bugs.csv.dvc
git commit -m "Add initial dataset with DVC"
Step 7: Install ML libraries
python -m pip install pandas scikit-learn joblib
Step 8: Create the training script
Create train.py with this code:
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("bugs.csv")

# Select input features and target
X = df[
    [
        "lines_of_code",
        "cyclomatic_complexity",
        "developer_experience"
    ]
]
y = df["bug_severity"]

# Convert text labels into numeric labels
le = LabelEncoder()
y = le.fit_transform(y)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save model and label encoder
joblib.dump(model, "bug_model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("Bug severity model trained successfully!")
print("Model saved as bug_model.pkl")
print("Label encoder saved as label_encoder.pkl")
Run it:
python train.py
Expected output:
Bug severity model trained successfully!
Model saved as bug_model.pkl
Label encoder saved as label_encoder.pkl
Step 9: Track the trained model with DVC
dvc add bug_model.pkl
dvc add label_encoder.pkl
Commit model metadata and training code:
git add .gitignore bug_model.pkl.dvc label_encoder.pkl.dvc
git commit -m "Track trained model with DVC"
git add train.py
git commit -m "Add DVC model training script"
Step 10: Create Dataset Version 2
Append these five records to bugs.csv. Keep the existing header and B001–B010 data; do not add another header.
B011,420,14,2,Medium
B012,800,25,1,High
B013,180,7,5,Low
B014,520,17,2,High
B015,260,9,4,Medium
Version 2 now contains 15 data records.
Step 11: Track and commit Dataset Version 2
dvc add bugs.csv
git add bugs.csv.dvc
git commit -m "Update dataset to version 2"
Step 12: Retrain and track Model Version 2
python train.py
dvc add bug_model.pkl
dvc add label_encoder.pkl
git add bug_model.pkl.dvc label_encoder.pkl.dvc
git commit -m "Update model to version 2"
Switch Between Dataset Versions
Restore Dataset Version 1
Find the dataset commits:
git log --oneline -- bugs.csv.dvc
In this run, the initial dataset commit was 1bf4a1f and the Version 2 commit was 4bfacb2. Commit IDs can be different in other repositories.

Restore the Version 1 metadata and contents:
git restore --source=1bf4a1f --worktree bugs.csv.dvc
dvc checkout bugs.csv.dvc
Verify that Version 1 has 10 data records:
Import-Csv bugs.csv | Measure-Object
The Count should be 10.
Restore Dataset Version 2
git restore --source=4bfacb2 --worktree bugs.csv.dvc
dvc checkout bugs.csv.dvc
Import-Csv bugs.csv | Measure-Object
The Count should be 15.

Use the commit IDs shown by git log --oneline -- bugs.csv.dvc in your own repository. Avoid checking out an old commit of the entire repository just to restore one dataset because the repository contains other practicals too.
Useful Verification Commands
git status --short
git log --oneline
git log --oneline -- bugs.csv.dvc
dvc status
- git status --short displays changed and untracked files.
- git log --oneline lists Git commits.
- git log --oneline -- bugs.csv.dvc lists dataset-version commits.
- dvc status checks whether the tracked data matches DVC metadata and the local cache.
Upload to GitHub
From D:\DOML-LAB\dvc_lab, add only the Experiment-7 files and metadata:
git add .gitignore .dvc/.gitignore .dvc/config .dvcignore README.md train.py bugs.csv.dvc bug_model.pkl.dvc label_encoder.pkl.dvc
git commit -m "Document DVC dataset and model versioning experiment"
git push origin main
If there is nothing to commit, those files may already be committed. If push is rejected because the remote has newer commits, use:
git pull --rebase origin main
git push origin main
If a rebase conflict appears, stop and resolve the conflict before continuing.
Important Note About DVC Storage
GitHub stores the code and .dvc metadata, not the actual contents of the tracked dataset and model files. This practical uses the local DVC cache. To retrieve the actual files on another computer, configure a DVC remote storage, run dvc push from the source machine, and use dvc pull on the other machine. No remote storage is configured by the procedure above.
Result
The dataset and trained model files were tracked using DVC, while Git tracked the source code and DVC metadata. Dataset Version 1 and Version 2 were created, the model was retrained after the dataset update, and the earlier dataset version was restored and switched back to Version 2.
Conclusion
This experiment demonstrated data and model versioning with DVC integrated with Git. It showed how datasets and model artifacts can be tracked separately from source code and how dataset versions can be restored for reproducible Machine Learning workflows.