import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

# 1. Encode the password to handle the '@' symbol
password = urllib.parse.quote_plus("p@ssw0rd")

# 2. Construct the engine with the encoded password
# Note the {password} variable inside the string
mysql_url = f"mysql+mysqlconnector://root:{password}@localhost:1213/paymentschedule_db"
mysql_engine = create_engine(mysql_url)
sqlite_engine = create_engine("sqlite:///db.sqlite3")

# 3. Get the list of tables
print("Connecting to MySQL...")
tables = pd.read_sql("SHOW TABLES", mysql_engine)
table_list = tables.iloc[:, 0].tolist()

# 4. Transfer Data
for table in table_list:
    print(f"Transferring data for: {table}...")
    try:
        df = pd.read_sql(f"SELECT * FROM `{table}`", mysql_engine)
        df.to_sql(table, sqlite_engine, index=False, if_exists='replace')
    except Exception as e:
        print(f"Error transferring {table}: {e}")

print("\nSuccess! Your db.sqlite3 is ready.")