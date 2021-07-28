import pandas as pd
import math

def import_csv(path):
    return pd.read_csv(path, index_col=0)

def is_acquired_entry(row):
    # Empty entries import as "NaN" which is of type float
    return isinstance(row["Relinquished"], float)

print("\n\nProcessing data...\n\n")

### INJURY LIST ###

# Import cleaned IL
full_IL = import_csv("./data/cleaned/injury_list_2010_2021.csv")

# For each "relinquished" entry, find the corresponding "acquired"
# entry and add this to the empty "Acquired" column
for i, row in full_IL.iterrows():
    # Skip row if its an "acquired" entry
    if is_acquired_entry(row):
        continue

    player = row["Relinquished"]

    # Iterate over remaining dataframe and find the next "acquired" entry
    # Flag to track whether the return date was found
    found = False
    for i2, row2 in full_IL[i+1:].iterrows():   

        # Assume that no players have the same name
        if row2["Relinquished"] == player:

            if is_acquired_entry(row2):
                # This entry contains when the player returned from their injury
                row["Acquired"] = row2["Date"]
                print(row)
                found = True

            else:
                # STARTHERE: Always entering here

                # This entry is ANOTHER injury which means they were out
                # for the season due to their last injury
                #
                # Let's mark this injury until the end of the year
                row["Acquired"] = f"{row2['Date'][0:4]}-12-31"
                print("BOOM")
                found = True

    # If the return date was not found, then the player has not returned
    # Let's mark this injury until the end of the year
    row["Acquired"] = f"{row2['Date'][0:4]}-12-31"


# Filter entries regarding when a player left the IL
il_relinquished = full_IL.dropna(subset=["Relinquished"])
print(f"Number of relinquished entries: {il_relinquished.shape[0]}")

# Filter out non-injury related IL items
illness_entries = il_relinquished[(il_relinquished['Notes'].str.contains('illness')) | (il_relinquished['Notes'].str.contains('flu'))]
surgery_entries = il_relinquished[il_relinquished['Notes'].str.contains('surgery')]
covid_entries = il_relinquished[il_relinquished['Notes'].str.contains('COVID-19')]
personal_entries = il_relinquished[il_relinquished['Notes'].str.contains('personal')]

non_injuries = pd.concat(objs=[illness_entries, surgery_entries, covid_entries, personal_entries])
il_injuries = il_relinquished.merge(non_injuries, how="outer", indicator=True).loc[lambda x : x['_merge']=='left_only'].drop(columns=['_merge'])

print(f"Number of injuries relating to illness: {illness_entries.shape[0]}")
print(f"Number of injuries relating to surgery: {surgery_entries.shape[0]}")
print(f"Number of injuries relating to COVID-19: {covid_entries.shape[0]}")
print(f"Number of injuries relating to personal reasons: {personal_entries.shape[0]}")
print(f"Remaining injury related entries: {il_injuries.shape[0]}")

il_injuries.to_csv("./data/processed/physical_injuries_2010_2021.csv")

print(il_injuries.head())

### ADD NEW FIELDS ###
