
import pandas as pd

from sklearn import preprocessing

### CONSTANTS ###

NORMALISED_DATA_PATH = "./data/processed/normalised.csv"
FINAL_DATA_PATH = "./data/processed/final.csv"

### HELPER FUNCTIONS ###

def import_csv(path):
    return pd.read_csv(path, index_col=0)

### SCRIPT START ###

print("\n\Selecting data...\n\n")
normalised = import_csv(NORMALISED_DATA_PATH)
