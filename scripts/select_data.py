
import pandas as pd
import matplotlib.pyplot as plt

### CONSTANTS ###

NORMALISED_DATA_PATH = "./data/processed/normalised.csv"
FINAL_DATA_PATH = "./data/processed/final.csv"
INITIAL_CORRELATIONS_PATH = "./outputs/correlations_initial.png"
POST_CORRELATIONS_PATH = "./outputs/correlations_post.png"

### HELPER FUNCTIONS ###

def import_csv(path):
    return pd.read_csv(path, index_col=0)

### SCRIPT START ###

print("\n\nSelecting data...\n\n")
normalised = import_csv(NORMALISED_DATA_PATH)

# First drop columns that are straight-up not relevant
normalised.drop(columns=[ "Player"
    , "Year"
    , "Tm"
    , "Duration"
], inplace=True)

# Now let's inpect correlations
f = plt.figure(figsize=(19, 15))
plt.matshow(normalised.corr(), fignum=f.number)
plt.xticks(range(normalised.select_dtypes(['number']).shape[1]), normalised.select_dtypes(['number']).columns, fontsize=14, rotation=45)
plt.yticks(range(normalised.select_dtypes(['number']).shape[1]), normalised.select_dtypes(['number']).columns, fontsize=14)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
plt.title('Correlation Matrix', fontsize=16)

# We can see that there are a lot of correlated fields
plt.savefig(INITIAL_CORRELATIONS_PATH)

# Let's remove some of these
normalised.drop(columns=[ "FG" # "Field Goals" are a combination of 3-points and 2-points
    , "FGA"
    , "FG%"
    , "3P"
    , "2P"
    , "FT"
    , "eFG%"
    , "TRB"
    , "PTS"
], inplace=True)

# and re-plot correlations
f = plt.figure(figsize=(19, 15))
plt.matshow(normalised.corr(), fignum=f.number)
plt.xticks(range(normalised.select_dtypes(['number']).shape[1]), normalised.select_dtypes(['number']).columns, fontsize=14, rotation=45)
plt.yticks(range(normalised.select_dtypes(['number']).shape[1]), normalised.select_dtypes(['number']).columns, fontsize=14)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
plt.title('Correlation Matrix', fontsize=16)
plt.savefig(POST_CORRELATIONS_PATH)

# save final dataset
normalised.to_csv(FINAL_DATA_PATH)
