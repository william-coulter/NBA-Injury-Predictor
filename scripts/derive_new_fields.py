import pandas as pd

from datetime import datetime

### CONTSTANTS ###

PHYSICAL_INJURIES_PATH = "./data/processed/physical_injuries_2010_2021.csv"
PLAYER_STATS_PATH = "./data/processed/player_stats_2010_2021.csv"

### HELPER FUNCTIONS ###

def import_csv(path):
    return pd.read_csv(path, index_col=0)

### SCRIPT START ###

print("Deriving new fields...")

physical_injuries = import_csv(PHYSICAL_INJURIES_PATH)
player_stats = import_csv(PLAYER_STATS_PATH)



