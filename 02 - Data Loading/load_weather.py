import sys

sys.path.append(r"C:\Users\radek\Git-Hub\Final_Project_Ironhack\00 - Utils")
import db_utils as db
import os
import glob
import pandas as pd

directory = r"C:\Users\radek\Git-Hub\Final_Project_Ironhack\data\weather"
table = "weather"
table_tmp = "weather_tmp"

# Purge the tables before
db.truncate(table_tmp)
db.truncate(table)

# iterate over files in
# that directory
for f in glob.glob(directory + "/*.json"):
    # checking if it is a file
    if os.path.isfile(f):
        print(f"Processing {f}")

        # Load the file into a df, with encoding iso-8859-1
        df = pd.read_json(f, encoding="iso-8859-1")

        # The days object is not yet columns,
        # we concatenate, the df minus days column
        # and we transform the data from days to column
        df = pd.concat([df.drop(["days"], axis=1), df["days"].apply(pd.Series)], axis=1)

        # drop a couple of unwanted columns
        df.drop(
            [
                "queryCost",
                "resolvedAddress",
                "timezone",
                "tzoffset",
                "precipprob",
                "preciptype",
                "winddir",
            ],
            axis=1,
            inplace=True,
            errors="ignore",
        )

        # we export the df to sql
        df.to_sql(
            "weather_tmp", db.engine, if_exists="append", index=False, chunksize=500
        )

# Check the number of rows inserted
print(f"{table_tmp} : {db.count(table_tmp)} rows")

# Populate the final table without duplicates
db.exec(f"INSERT IGNORE INTO {table} SELECT * FROM {table_tmp};")

# Check the number of rows inserted
print(f"{table} : {db.count(table)} rows")
