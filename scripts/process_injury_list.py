import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import math
from datetime import datetime

### CONSTANTS ###

# Dictionary of when each regular season started
# Key is the year that the season started STARTHERE
REG_SEASON_START = { "2010": "2009-10-27"
    , "2011": "2010-10-26"
    , "2012": "2011-12-25"
    , "2013": "2012-10-30"
    , "2014": "2013-10-29"
    , "2015": "2014-10-28"
    , "2016": "2015-10-27"
    , "2017": "2016-10-25"
    , "2018": "2017-10-17"
    , "2019": "2018-10-16"
    , "2020": "2019-10-22"
    , "2021": "2020-12-22"
    }

# Dictionary of when each regular season ended
REG_SEASON_END = { "2010": "2010-04-14"
    , "2011": "2011-04-14"
    , "2012": "2012-04-26"
    , "2013": "2013-04-17"
    , "2014": "2014-04-16"
    , "2015": "2015-04-15"
    , "2016": "2016-04-13"
    , "2017": "2017-04-12"
    , "2018": "2018-04-11"
    , "2019": "2019-04-10"
    , "2020": "2020-03-11"
    , "2021": "2021-05-16"
    }

### HELPER FUNCTIONS ###

def import_csv(path):
    return pd.read_csv(path, index_col=0)

def is_acquired_entry(row):
    # Empty entries import as "NaN" which is of type float
    return isinstance(row["Relinquished"], float)

def calculate_days_on_il(row, season_val):
    # For the histogram, don't include injuries where a player was out for
    # the season. These will automatically count as a major injury.
    if row["Acquired"] == "season":
        return season_val
    else:
        start = datetime.strptime(row["Date"], "%Y-%m-%d")
        end = datetime.strptime(row["Acquired"], "%Y-%m-%d")
        return (end - start).days

def is_regular_season(s):
    year = s[0:4]
    injury_date = datetime.strptime(s, "%Y-%m-%d")


    end_date = datetime.strptime(REG_SEASON_END[year], "%Y-%m-%d")

    return injury_date <= end_date

### SCRIPT START ###

print("\n\nProcessing injury list...\n\n")

# # Import cleaned IL
# full_IL = import_csv("./data/cleaned/injury_list_2010_2021.csv")

# # For each "relinquished" entry, find the corresponding "acquired"
# # entry and add this to the empty "Acquired" column
# print("Fixing 'Acquired' column, this may take a while...")
# for i, row in full_IL.iterrows():
#     # Skip row if its an "acquired" entry
#     if is_acquired_entry(row):
#         continue

#     player = row["Relinquished"]

#     # Iterate over remaining dataframe and find the next "acquired" entry
#     # Flag to track whether the return date was found
#     found = False
#     for i2, row2 in full_IL[i+1:].iterrows():   
#         if found == True:
#             break

#         # Assume that no players have the same name
#         if row2["Acquired"] == player or row2["Relinquished"] == player:

#             if is_acquired_entry(row2):
#                 # This entry contains when the player returned from their injury
#                 full_IL.at[i, "Acquired"] = row2["Date"]
#                 found = True

#             else:
#                 # This entry is ANOTHER injury which means they were out
#                 # for the season due to their last injury
#                 #
#                 # Let's mark this injury as season
#                 full_IL.at[i, "Acquired"] = "season"
#                 found = True

#     # If the return date was not found, then the player has not returned
#     if found == False:
#         full_IL.at[i, "Acquired"] = "season"

# # Filter entries regarding when a player left the IL
# il_relinquished = full_IL.dropna(subset=["Relinquished"])
# print(f"Number of relinquished entries: {il_relinquished.shape[0]}")

# # Filter out non-injury related IL items
# illness_entries = il_relinquished[(il_relinquished['Notes'].str.contains('illness')) | (il_relinquished['Notes'].str.contains('flu'))]
# surgery_entries = il_relinquished[il_relinquished['Notes'].str.contains('surgery')]
# covid_entries = il_relinquished[il_relinquished['Notes'].str.contains('COVID-19')]
# personal_entries = il_relinquished[il_relinquished['Notes'].str.contains('personal')]

# non_injuries = pd.concat(objs=[illness_entries, surgery_entries, covid_entries, personal_entries])
# il_injuries = il_relinquished.merge(non_injuries, how="outer", indicator=True).loc[lambda x : x['_merge']=='left_only'].drop(columns=['_merge'])

# print(f"Number of injuries relating to illness: {illness_entries.shape[0]}")
# print(f"Number of injuries relating to surgery: {surgery_entries.shape[0]}")
# print(f"Number of injuries relating to COVID-19: {covid_entries.shape[0]}")
# print(f"Number of injuries relating to personal reasons: {personal_entries.shape[0]}")
# print(f"Remaining injury related entries: {il_injuries.shape[0]}")

# il_injuries.to_csv("./data/processed/physical_injuries_2010_2021.csv")
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# import math
# from datetime import datetime

# def import_csv(path):
#     return pd.read_csv(path, index_col=0)

# def is_acquired_entry(row):
#     # Empty entries import as "NaN" which is of type float
#     return isinstance(row["Relinquished"], float)

# print("\n\nProcessing injury list...\n\n")

# # Import cleaned IL
# full_IL = import_csv("./data/cleaned/injury_list_2010_2021.csv")

# # For each "relinquished" entry, find the corresponding "acquired"
# # entry and add this to the empty "Acquired" column
# print("Fixing 'Acquired' column, this may take a while...")
# for i, row in full_IL.iterrows():
#     # Skip row if its an "acquired" entry
#     if is_acquired_entry(row):
#         continue

#     player = row["Relinquished"]

#     # Iterate over remaining dataframe and find the next "acquired" entry
#     # Flag to track whether the return date was found
#     found = False
#     for i2, row2 in full_IL[i+1:].iterrows():   
#         if found == True:
#             break

#         # Assume that no players have the same name
#         if row2["Acquired"] == player or row2["Relinquished"] == player:

#             if is_acquired_entry(row2):
#                 # This entry contains when the player returned from their injury
#                 full_IL.at[i, "Acquired"] = row2["Date"]
#                 found = True

#             else:
#                 # This entry is ANOTHER injury which means they were out
#                 # for the season due to their last injury
#                 #
#                 # Let's mark this injury as season
#                 full_IL.at[i, "Acquired"] = "season"
#                 found = True

#     # If the return date was not found, then the player has not returned
#     if found == False:
#         full_IL.at[i, "Acquired"] = "season"

# # Filter entries regarding when a player left the IL
# il_relinquished = full_IL.dropna(subset=["Relinquished"])
# print(f"Number of relinquished entries: {il_relinquished.shape[0]}")

# # Filter out non-injury related IL items
# illness_entries = il_relinquished[(il_relinquished['Notes'].str.contains('illness')) | (il_relinquished['Notes'].str.contains('flu'))]
# surgery_entries = il_relinquished[il_relinquished['Notes'].str.contains('surgery')]
# covid_entries = il_relinquished[il_relinquished['Notes'].str.contains('COVID-19')]
# personal_entries = il_relinquished[il_relinquished['Notes'].str.contains('personal')]

# non_injuries = pd.concat(objs=[illness_entries, surgery_entries, covid_entries, personal_entries])
# il_injuries = il_relinquished.merge(non_injuries, how="outer", indicator=True).loc[lambda x : x['_merge']=='left_only'].drop(columns=['_merge'])

# print(f"Number of injuries relating to illness: {illness_entries.shape[0]}")
# print(f"Number of injuries relating to surgery: {surgery_entries.shape[0]}")
# print(f"Number of injuries relating to COVID-19: {covid_entries.shape[0]}")
# print(f"Number of injuries relating to personal reasons: {personal_entries.shape[0]}")
# print(f"Remaining injury related entries: {il_injuries.shape[0]}")

# il_injuries.to_csv("./data/processed/physical_injuries_2010_2021.csv")
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# import math
# from datetime import datetime

# def import_csv(path):
#     return pd.read_csv(path, index_col=0)

# def is_acquired_entry(row):
#     # Empty entries import as "NaN" which is of type float
#     return isinstance(row["Relinquished"], float)

# print("\n\nProcessing injury list...\n\n")

# # Import cleaned IL
# full_IL = import_csv("./data/cleaned/injury_list_2010_2021.csv")

# # For each "relinquished" entry, find the corresponding "acquired"
# # entry and add this to the empty "Acquired" column
# print("Fixing 'Acquired' column, this may take a while...")
# for i, row in full_IL.iterrows():
#     # Skip row if its an "acquired" entry
#     if is_acquired_entry(row):
#         continue

#     player = row["Relinquished"]

#     # Iterate over remaining dataframe and find the next "acquired" entry
#     # Flag to track whether the return date was found
#     found = False
#     for i2, row2 in full_IL[i+1:].iterrows():   
#         if found == True:
#             break

#         # Assume that no players have the same name
#         if row2["Acquired"] == player or row2["Relinquished"] == player:

#             if is_acquired_entry(row2):
#                 # This entry contains when the player returned from their injury
#                 full_IL.at[i, "Acquired"] = row2["Date"]
#                 found = True

#             else:
#                 # This entry is ANOTHER injury which means they were out
#                 # for the season due to their last injury
#                 #
#                 # Let's mark this injury as season
#                 full_IL.at[i, "Acquired"] = "season"
#                 found = True

#     # If the return date was not found, then the player has not returned
#     if found == False:
#         full_IL.at[i, "Acquired"] = "season"

# # Filter entries regarding when a player left the IL
# il_relinquished = full_IL.dropna(subset=["Relinquished"])
# print(f"Number of relinquished entries: {il_relinquished.shape[0]}")

# # Filter out non-injury related IL items
# illness_entries = il_relinquished[(il_relinquished['Notes'].str.contains('illness')) | (il_relinquished['Notes'].str.contains('flu'))]
# surgery_entries = il_relinquished[il_relinquished['Notes'].str.contains('surgery')]
# covid_entries = il_relinquished[il_relinquished['Notes'].str.contains('COVID-19')]
# personal_entries = il_relinquished[il_relinquished['Notes'].str.contains('personal')]

# non_injuries = pd.concat(objs=[illness_entries, surgery_entries, covid_entries, personal_entries])
# il_injuries = il_relinquished.merge(non_injuries, how="outer", indicator=True).loc[lambda x : x['_merge']=='left_only'].drop(columns=['_merge'])

# print(f"Number of injuries relating to illness: {illness_entries.shape[0]}")
# print(f"Number of injuries relating to surgery: {surgery_entries.shape[0]}")
# print(f"Number of injuries relating to COVID-19: {covid_entries.shape[0]}")
# print(f"Number of injuries relating to personal reasons: {personal_entries.shape[0]}")
# print(f"Remaining injury related entries: {il_injuries.shape[0]}")

# TODO: remove me
il_injuries = import_csv("./data/processed/physical_injuries_2010_2021.csv")
il_injuries.drop(columns=["Season"], inplace=True)
# Calculate days that injury left player on injury list and add season
for i, row in il_injuries.iterrows():
    il_injuries.at[i, "Duration"] = calculate_days_on_il(row, 100)
    il_injuries.at[i, "Year"] = row["Date"][0:4]
    if is_regular_season(row["Date"]):
        il_injuries.at[i, "Season"] = "regular"
    else:
        il_injuries.at[i, "Season"] = "post"

# Save dataframe
il_injuries.to_csv("./data/processed/physical_injuries_2010_2021.csv")

# Plot distribution
days_data = il_injuries["Duration"]
percentile_80 = np.percentile(days_data, 80)
print(f"80th percentile of injuries: {percentile_80}")

# Arbitarily set range between 0 and 75 to filter out outliers
plt.hist(days_data, bins="auto", range=(0,75))
plt.gca().set(title="Days Spent on IL Distribution", ylabel='Frequency')
plt.axvline(x=percentile_80, color="red")

plt.savefig("./outputs/day_spent_on_il_distribution.png")
