import pandas as pd
import numpy as np

from datetime import datetime

### CONTSTANTS ###

PHYSICAL_INJURIES_PATH = "./data/processed/physical_injuries_2010_2021.csv"
PLAYER_STATS_PATH = "./data/cleaned/player_stats_2010_2021.csv"
COMBINED_DATA_PATH = "./data/processed/combined.csv"
AGGREGATED_DATA_PATH = "./data/processed/aggregated.csv"

MAJOR_INJURY_BOUNDARY = 34

### HELPER FUNCTIONS ###

def import_csv(path):
    return pd.read_csv(path, index_col=0)

def is_major_injury(row):
    duration = row["Duration"]
    if not np.isnan(duration) and int(duration) > MAJOR_INJURY_BOUNDARY:
        return True
    else:
        return False

def is_minor_injury(row):
    duration = row["Duration"]
    if not np.isnan(duration) and not is_major_injury(row):
        return True
    else:
        return False

### SCRIPT START ###

print("\n\nScript start...\n\n")

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

combined.reset_index(
    inplace=True
)

# Derive 'Major Injury' column
print("Deriving 'Major Injury' column...")
for i, row in combined.iterrows():
    if is_major_injury(row):
        combined.loc[i, "Major Injury"] = "1"
    else:
        combined.loc[i, "Major Injury"] = "0"

# Before we groupby, let's drop some columns we don't need anymore
combined.drop(
    columns=["Team"  # There is already a column "Tm" with the team
        , "Date"     # This was the exact date of the injury, we already know the season the injury occured
        , "Acquired" # This was when the player returned from their injury, we already know how long the injury lasted for with the "Duration" column
        , "Notes"    # Notes about the injury
    ],
    inplace=True
)
combined.to_csv(COMBINED_DATA_PATH)

combined = import_csv(COMBINED_DATA_PATH)
# Derive 'Recent Minor Injury Count' column
print("Deriving 'Recent Minor Injury Count' and aggregating...\nThis may take a while")
# Note that we can't just do a groupby because players switch teams
# and which gets added in as its own row and we want to combine these
# since a player moving teams in the same season is still the same player
aggregated_indexes = []
aggregated = pd.DataFrame(columns=combined.columns)
for i, row in combined.iterrows():
    if i in aggregated_indexes:
        continue

    player = row["Player"]
    year = row["Year"]
    season = row["Season"]
    team = row["Tm"]

    # Values we will aggregate
    #
    # ASSUMPTION: Not all of the season stats are aggregated.
    # We just take the values of the first row.
    minutes_per_game = row["MP"]
    games_played = row["G"]
    games_started = row["GS"]
    major_injury = 0
    minor_injury_count = 0

    j = i
    while combined.at[j, "Player"] == player and combined.at[j, "Year"] == year and combined.at[j, "Season"] == season:
        if is_minor_injury(combined.loc[j]):
            minor_injury_count += 1

        elif is_major_injury(combined.loc[j]):
            major_injury = 1

        # If there is a new team, we need to aggregate some of the values
        if combined.at[j, "Tm"] != team:
            team = combined.at[j, "Tm"]
            # Calculate new average minutes per game
            minutes_per_game = (minutes_per_game * games_played + combined.at[j, "MP"] * combined.at[j, "G"]) / (games_played + combined.at[j, "G"])
            games_played += combined.at[j, "G"]
            games_started += combined.at[j, "GS"]

        aggregated_indexes.append(j)
        j += 1

        try:
            combined.loc[j]
        except KeyError:
            # End of dataframe
            break


    # Now let's aggregate all of these into a new row
    new_row = row
    new_row["MP"] = minutes_per_game
    new_row["G"] = games_played
    new_row["GS"] = games_started
    new_row["Major Injury"] = major_injury

    aggregated.loc[i] = new_row
    aggregated.at[i, "Minor Injury Count"] = minor_injury_count

aggregated.to_csv(AGGREGATED_DATA_PATH)

aggregated = import_csv(AGGREGATED_DATA_PATH)
print("Deriving 'Previous Major Injury Count' column...")
for i, row in aggregated.iterrows():
    player = row["Player"]
    prev_major_injuries = aggregated.loc[(aggregated["Player"] == player) & (aggregated.index < i) & (aggregated["Major Injury"] == 1)]

    aggregated.at[i, "Previous Major Injury Count"] = prev_major_injuries.shape[0]

aggregated.to_csv(AGGREGATED_DATA_PATH)
