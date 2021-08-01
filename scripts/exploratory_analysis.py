import pandas as pd

### CONSTANTS ###

FINAL_DATA_PATH = "./data/processed/final.csv"

### HELPER FUNCTIONS ###

def import_csv(path):
    return pd.read_csv(path, index_col=0)

### SCRIPT START ###

print("\n\nExploratory Analysis...\n\n")
df = import_csv(FINAL_DATA_PATH)

major_injury_count = df[df["Major Injury"] == 1].shape[0]

print(f"Total number of examples: {df.shape[0]}")
print(f"Total number of features: {df.shape[1]}")
print(f"Total number of examples with major injuries: {major_injury_count}")
