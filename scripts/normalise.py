import pandas as pd

from sklearn import preprocessing

### CONSTANTS ###

TOKENIZED_DATA_PATH = "./data/processed/tokenized.csv"
NORMALISED_DATA_PATH = "./data/processed/normalised.csv"

PER_GAME_STATS = [ "FG"
    , "FGA"
    , "3P"
    , "3PA"
    , "2P"
    , "2PA"
    , "FT"
    , "FTA"
    , "ORB"
    , "DRB"
    , "TRB"
    , "AST"
    , "STL"
    , "BLK"
    , "TOV"
    , "PF"
    , "PTS"
]

STATS_TO_NORMALISE = PER_GAME_STATS + [ "Age"
    , "FGA"
    , "G"   
    , "GS"
    , "MP"
    , "FG%"
    , "3P%"
    , "2P%"
    , "eFG%"
    , "FT%"
    , "Minor Injury Count"
    , "Previous Major Injury Count"
]

### HELPER FUNCTIONS ###

def import_csv(path):
    return pd.read_csv(path, index_col=0)

### SCRIPT START ###

print("\n\nNormalising data...\n\n")
tokenised = import_csv(TOKENIZED_DATA_PATH)
normalised = tokenised

# Real quick, we should eliminate rows before 2010 since we don't
# have injury data for this and any player who played for 0 minutes
print(f"Number of entries before limiting data to >= 2010: {normalised.shape[0]}")
normalised = normalised[normalised["Year"] >= 2010]
normalised = normalised.dropna(subset=["MP"])
normalised = normalised[normalised["MP"] != 0]
print(f"Number of entries after limiting data to >= 2010: {normalised.shape[0]}")

# First create ratio with minutes player per game
for i, row in normalised.iterrows():
    avg_minutes_per_game = row["MP"]

    for stat in PER_GAME_STATS:
        normalised.at[i, stat] = row[stat] / avg_minutes_per_game

# Now normal values
normalised.fillna(value=0, inplace=True)
normalised.to_csv(NORMALISED_DATA_PATH)
