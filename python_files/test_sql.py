from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import pandas as pd

# SQL settings
my_uid = "LAPTOP-GG7823IL\dadas"
my_pwd = "testpass"
my_host = "LAPTOP-GG7823IL\SQLEXPRESS"
my_db = "test"
my_odbc_driver = "ODBC Driver 17 for SQL Server"

connection_url = URL.create(
    "mssql+pyodbc",
    username=my_uid,
    #password=my_pwd,
    host=my_host,
    database=my_db,  # required; not an empty string
    query={
        "driver": my_odbc_driver ,
        "Trusted_Connection": "yes",
        "TrustServerCertificate": "yes",
    },
)

engine = create_engine(connection_url, fast_executemany=True)
connection = engine.raw_connection( )

def get_table_names():
    query = f"SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_catalog = '{my_db}';"
    table_names = pd.read_sql_query(query, connection)
    print(table_names)
    return table_names['table_name'].tolist()


table_names = get_table_names()
print(table_names)


query1 = f"SELECT * FROM {'BQ4050_0x0001_dataflash'}"
testt = pd.read_sql_query(query1, connection)



query2 = f"SELECT * FROM {'BQ4050_705095120210054_0x0036_dataflash'}"
testt2 = pd.read_sql_query(query2, connection)


different_measured = testt2["MEASURED VALUE"] != testt["MEASURED VALUE"]
print(different_measured)

diff_df = testt2[different_measured]
print(diff_df)




new_df = pd.concat([testt, testt2], axis=0)
