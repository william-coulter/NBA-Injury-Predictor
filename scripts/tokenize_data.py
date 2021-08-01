import pandas as pd
import pickle

from sklearn import preprocessing

### CONSTANTS ###

AGGREGATED_DATA_PATH = "./data/processed/aggregated.csv"
TOKENIZED_DATA_PATH = "./data/processed/tokenized.csv"

POSITION_ENCODER_PATH = "./encoders/player_position.ser"
SEASON_ENCODER_PATH = "./encoders/season.ser"

### HELPER FUNCTIONS ###

def import_csv(path):
    return pd.read_csv(path, index_col=0)

def serialise(o, path):
    with open(path, "wb") as f:
        pickle.dump(o, f)

### SCRIPT START ###

print("\n\nTokenizing data...\n\n")

aggregated = import_csv(AGGREGATED_DATA_PATH)
tokenized = aggregated

# Encode positions
positionLe = preprocessing.LabelEncoder()
tokenized["Pos"] = positionLe.fit_transform(tokenized["Pos"])

serialise(positionLe, POSITION_ENCODER_PATH)

# Encode season
seasonLe = preprocessing.LabelEncoder()
tokenized["Season"] = seasonLe.fit_transform(tokenized["Season"])

serialise(seasonLe, SEASON_ENCODER_PATH)

# Save dataframe
tokenized.to_csv(TOKENIZED_DATA_PATH)
