import os
import pandas as pd

# We want to append the recently scraped datasets with 
# the previous ones

def append_raw(pref):
    old_df = pd.read_csv(f"./data/raw/{pref}_2010_2019.csv")

    # Little hack just to fix in this particular case
    if pref == "all_teams_schedule":
        old_df.drop(columns=["Season"], inplace=True)

    new_df = pd.read_csv(f"./data/raw/{pref}_2019_2021.csv")
    combined_df = pd.concat(
        objs=[old_df, new_df],
        join="outer",
        ignore_index=True
    )
    # Drop the index overflow
    combined_df.drop(columns=["Unnamed: 0"], inplace=True)
    return combined_df

file_prefixes = ["all_teams_schedule", "injury_list", "missed_games", "player_stats"]

for pref in file_prefixes:
    combined_df = append_raw(pref)
    combined_df.to_csv(f"./data/cleaned/{pref}_2010_2021.csv")
