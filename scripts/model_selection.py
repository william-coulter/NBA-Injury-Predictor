import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sklearn import preprocessing
from sklearn.metrics import log_loss, make_scorer, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

### CONSTANTS ###

FINAL_DATA_PATH = "./data/processed/final.csv"

PER_GAME_STATS = [ "3PA"
    , "2PA"
    , "FTA"
    , "ORB"
    , "DRB"
    , "AST"
    , "STL"
    , "BLK"
    , "TOV"
    , "PF"
]

STATS_TO_NORMALISE = PER_GAME_STATS + [ "Age"
    , "G"
    , "GS"
    , "MP"
    , "3P%"
    , "2P%"
    , "FT%"
    , "Minor Injury Count"
    , "Previous Major Injury Count"
]

### HELPER FUNCTIONS ###

def import_csv(path):
    return pd.read_csv(path, index_col=0)

def normalise_data_for_bayes(df):
    # scale all values between 0 and 1
    scaler = preprocessing.MinMaxScaler()
    scaler.fit(df)
    df = scaler.transform(df)
    return df

def normalise_data_for_logistic(df):
    # scale all values such that the mean is 0
    df = preprocessing.scale(df, with_std=True)
    return df

### SCRIPT START ###

print("\n\Selecting models...\n\n")

# Hyperparameters
C = 5

# Create classifiers
classifiers = { "Logistic (L1)": LogisticRegression(penalty='l1', solver='liblinear', C=C)
    , "Logistic (L2 Saga Solver)": LogisticRegression(C=C, penalty='l2',
                                                    solver='saga',
                                                    multi_class='multinomial',
                                                    max_iter=10000)
    , "Linear SVC (linear)": SVC(kernel='linear', C=C, probability=True, random_state=0)
    , "Linear SVC (gamma)": SVC(gamma=5, C=C)
    , "Naive Bayes (Multinomial)": MultinomialNB()
    , "Random Forest": RandomForestClassifier(max_depth=10, random_state=0),
}

data = import_csv(FINAL_DATA_PATH)

for i, (name, model) in enumerate(classifiers.items()):
    X = data.drop(columns=["Major Injury"])
    Y = data["Major Injury"]

    # Split data
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(
        X, Y, test_size=0.33, random_state=0
    )

    # Normalise and standardise
    if name.startswith("Naive Bayes"):
        Xtrain_normalised = normalise_data_for_bayes(Xtrain)
        Xtest_normalised = normalise_data_for_bayes(Xtest)

    elif name.startswith("Logistic") or name.startswith("Linear"):
        Xtrain_normalised = normalise_data_for_logistic(Xtrain)
        Xtest_normalised = normalise_data_for_logistic(Xtest)

    else:
        Xtrain_normalised = Xtrain
        Xtest_normalised = Xtest

    # Fit model
    model.fit(Xtrain_normalised, Ytrain)

    # Test model
    y_pred = model.predict(Xtest)
    score = model.score(Xtest_normalised, Ytest)
    loss = log_loss(Ytest, y_pred)

    print(f"Score for {name}: {score}")
    print(f"Log-loss for {name}: {loss}\n")

    # Plot a confusion matrix
    conf_mat = confusion_matrix(Ytest, y_pred)
    fig, ax = plt.subplots(figsize=(10,10))
    sns.heatmap(conf_mat, annot=True, fmt='d',
                xticklabels=["No Major Injury","Major Injury"], yticklabels=["No Major Injury","Major Injury"])
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title(f"Confusion Matrix: {name}.png")
    plt.savefig(f"outputs/confusion_matrix_{name}.png")
