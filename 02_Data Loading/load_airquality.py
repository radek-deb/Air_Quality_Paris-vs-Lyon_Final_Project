import sys

sys.path.append(r"C:\Users\radek\Git-Hub\Final_Project_Ironhack\00 - Utils")
import db_utils as db
import os
import glob
import pandas as pd

# iterate over files in that directory
directory = r"C:\Users\radek\Git-Hub\Final_Project_Ironhack\data\airquality"
table = "airquality"
table_tmp = "airquality_tmp"

lines_to_skip = 4
species_to_keep = ["co", "no2", "o3", "pm10", "pm25", "so2"]
# cols_to_keep = [
#     "Date",
#     "Country",
#     "City",
#     "co_min",
#     "no2_min",
#     "o3_min",
#     "pm10_min",
#     "pm25_min",
#     "so2_min",
#     "co_max",
#     "no2_max",
#     "o3_max",
#     "pm10_max",
#     "pm25_max",
#     "so2_max",
#     "co_median",
#     "no2_median",
#     "o3_median",
#     "pm10_median",
#     "pm25_median",
#     "so2_median",
#     "co_variance",
#     "no2_variance",
#     "o3_variance",
#     "pm10_variance",
#     "pm25_variance",
#     "so2_variance",
# ]

eu = r"C:\Users\radek\Git-Hub\Final_Project_Ironhack\data\eu.cities.csv"
eu = pd.read_csv(eu, encoding="utf-8")
cities = [
    # "Berlin",
    # "Caen",
    # "Krakow",
    # "Lisbon",
    # "Lyon",
    # "Marseille",
    "Lyon",
    # "Rome",
    # "Warsaw",
]

# Purge the tables before
# db.truncate(table_tmp)
# db.truncate(table)

# iterate over files in that directory
# for filename in os.listdir(directory):
for f in glob.glob(directory + "/waqi*.csv"):
    # checking if it is a file
    if os.path.isfile(f):
        print(f"Processing {f}")

        # Load the file into a df, skipping 4 lines, with encoding UTF-8
        df = pd.read_csv(f, skiprows=lines_to_skip, encoding="utf-8")
        df.drop(columns=["count", "min", "max", "variance"], inplace=True)

        # Remove unwanted species
        df.drop(df.index[~df["Specie"].isin(species_to_keep)], inplace=True)

        # Remove non european countries
        df.drop(df.index[~df["Country"].isin(eu["Country"].unique())], inplace=True)

        # Keep only the cities we want
        df.drop(df.index[~df["City"].isin(cities)], inplace=True)

        # we pivot the specie columns to have, one column for each measures, ie co_min, no2_min, ...
        df2 = df.pivot(
            index=["Date", "Country", "City"],
            columns="Specie",
            values=["median"],
        )

        # Rename the columns ie co_min, no2_min, and reset the index
        df2.columns = [s2 for (s1, s2) in df2.columns.tolist()]
        df2.reset_index(inplace=True)

        # Save to sql, keeping only the defined columns
        # ie skipping other measurements like temperature, humidity, ...
        df2.to_sql(
            "airquality_tmp", db.engine, if_exists="append", index=False, chunksize=2000
        )

# Check the number of rows inserted
# print(f"{table_tmp} : {db.count(table_tmp)} rows")

# Populate the final table without duplicates
# db.exec(f"INSERT IGNORE INTO {table} SELECT * FROM {table_tmp};")

# Check the number of rows inserted
# print(f"{table} : {db.count(table)} rows")
