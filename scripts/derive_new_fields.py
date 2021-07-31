import pandas as pd
import numpy as np

from datetime import datetime

### CONTSTANTS ###

PHYSICAL_INJURIES_PATH = "./data/processed/physical_injuries_2010_2021.csv"
PLAYER_STATS_PATH = "./data/cleaned/player_stats_2010_2021.csv"
COMBINED_DATA_PATH = "./data/processed/combined.csv"

MAJOR_INJURY_BOUNDARY = 34

### HELPER FUNCTIONS ###

def import_csv(path):
    return pd.read_csv(path, index_col=0)

### SCRIPT START ###

print("\n\Script start...\n\n")

player_stats = import_csv(PLAYER_STATS_PATH)
physical_injuries = import_csv(PHYSICAL_INJURIES_PATH)

print("Joining physical injury and player stat datasets...")
# Set multiple indexes for each of these dataframes
player_stats.set_index(
    inplace=True,
    keys=["Player", "Year", "Season"]
)
physical_injuries.set_index(
    inplace=True,
    keys=["Player", "Year", "Season"]
)

combined = player_stats.merge(
    right=physical_injuries,
    how="left",
    on=["Player", "Year", "Season"]
)
# Clean out rows with identical values across all columns
combined.drop_duplicates(inplace=True)

# Derive 'Major Injury' column
print("Deriving 'Major Injury' column...")
for i, row in combined.iterrows():
    # STARTHERE: Cannot set new value with multiple-indexes
    print(i)
    duration = row["Duration"]

    # If "Duration" has a value and is greater than 34, then
    # the player has suffered a major injury during that season
    if not np.isnan(duration) and duration > MAJOR_INJURY_BOUNDARY:
        combined.at[i, "Major Injury"] = "1"
    else:
        combined.at[i, "Major Injury"] = "0"

combined.to_csv(COMBINED_DATA_PATH)

# Derive 'Recent Minor Injury Count' column
print("Deriving 'Recent Minor Injury Count' column...")
# STARTHERE: I think it's:
#
# combined.groupby(by=["Hmmm this might need to be a shit-load of columns"], dropna=False).size()
# in "by", need to include "major injury" column

# Derive 'Previous Major Injury Count' column
print("Deriving 'Previous Major Injury Count' column...")
