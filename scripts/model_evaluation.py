import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

### CONSTANTS ###

FINAL_DATA_PATH = "./data/processed/final.csv"

### HELPER FUNCTIONS ###

def import_csv(path):
    return pd.read_csv(path, index_col=0)

### SCRIPT START ###

print("\n\nEvaluating models...\n\n")

model = RandomForestClassifier(max_depth=10, random_state=0)

data = import_csv(FINAL_DATA_PATH)

X = data.drop(columns=["Major Injury"])
Y = data["Major Injury"]

# Split data
Xtrain, Xtest, Ytrain, Ytest = train_test_split(
    X, Y, test_size=0.8, random_state=0
)

Xtrain_normalised = Xtrain
Xtest_normalised = Xtest

# Fit model
model.fit(Xtrain_normalised, Ytrain)

# Grab Giannias' data
mvp_data = data.drop(columns=["Major Injury"]).loc[25415].array.reshape(1, -1)

# Evaluate model
y_pred = model.predict_proba(mvp_data)
print(y_pred)
print(f"predicted probability of injury for Antetokounmpo: {y_pred[0][1]}")
