import sys

sys.path.append(r"C:\Users\radek\Git-Hub\Final_Project_Ironhack\00 - Utils")
import db_utils as db
import os
import glob
import pandas as pd

# iterate over files in that directory
directory = r"C:\Users\radek\Git-Hub\Final_Project_Ironhack\data\airquality2"
table = "airquality_v2"
table_tmp = "airquality_tmp_v2"

lines_to_skip = 0


# Purge the tables before
db.truncate(table_tmp)
db.truncate(table)

# iterate over files in that directory
# for filename in os.listdir(directory):
for f in glob.glob(directory + "/*.csv"):
    # checking if it is a file
    if os.path.isfile(f):
        print(f"Processing {f}")

        # Load the file into a df, skipping 4 lines, with encoding UTF-8
        df = pd.read_csv(f, skiprows=lines_to_skip, encoding="utf-8", skipinitialspace=True)

        #removing space in column names
        # df.columns = df.columns.str.strip(' ')
        # for col in df.columns:
        #     df[col].str.strip(' ')

        df['City']= os.path.splitext(os.path.basename(f))[0]
        # Save to sql, keeping only the defined columns
        # ie skipping other measurements like temperature, humidity, ...
        df.to_sql(
            table_tmp, db.engine, if_exists="append", index=False, chunksize=2000
        )

# Check the number of rows inserted
# print(f"{table_tmp} : {db.count(table_tmp)} rows")

# Populate the final table without duplicates
# db.exec(f"INSERT IGNORE INTO {table} SELECT * FROM {table_tmp};")

# Check the number of rows inserted
# print(f"{table} : {db.count(table)} rows")
