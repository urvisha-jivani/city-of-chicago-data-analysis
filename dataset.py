
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from prettytable import PrettyTable

# Connect to SQLite database
db_name = "socioeconomic.db"
con = sqlite3.connect(db_name)

# Download the dataset
url = "https://data.cityofchicago.org/resource/jcxq-k9xf.csv"
table_name = "chicago_socioeconomic_data"

try:
    df = pd.read_csv(url)
    print(f"Downloaded {len(df)} rows.")
except Exception as e:
    print("Error while downloading data:", e)
    con.close()
    exit()

# Store data in SQLite
try:
    df.to_sql(table_name, con, if_exists='replace', index=False, method="multi")
    print(f"Saved data to table '{table_name}' in {db_name}.")
except Exception as e:
    print("Error while saving to database:", e)

# Using PrettyTable to display first 5 rows nicely in terminal
print("\nPreview of first 5 rows using PrettyTable:")
table = PrettyTable()

# Use columns from dataframe
columns = df.columns.tolist()
table.field_names = columns

# Add first 5 rows to the PrettyTable

preview = df.head(5)
table = PrettyTable()
table.field_names = preview.columns

for i in range(len(preview)):
    table.add_row(preview.iloc[i])

print(table)

# Plot distribution of adults aged 25+ without high school diploma
column_name = "percent_aged_25_without_high_school_diploma"

if column_name in df.columns:
    plt.figure(figsize=(10,6))
    sns.histplot(df[column_name].dropna(), kde=True, color='skyblue')
    plt.title("Distribution of Adults (25+) Without High School Diploma (%)")
    plt.xlabel("Percent")
    plt.ylabel("Number of Community Areas")
    plt.tight_layout()
    plt.show()
    plt.savefig("assets/no_high_school_distribution.png")

else:
    print(f" Column '{column_name}' not found in dataset.")


# Close DB connection
con.close()
print("\n Database connection closed.")
