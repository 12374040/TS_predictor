import pyodbc
import numpy as np
import pandas as pd

server = 'ticketscrape.database.windows.net'
database = 'ts_db'
username = 'data_admin'
password = 'Kaasisbaas4'
driver= '{ODBC Driver 17 for SQL Server}'

def check_database():
    conn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)

    df = pd.read_sql_query('''
    SELECT 
        name,
        aangeboden, 
        verkocht, 
        gezocht,
        event_date, 
        location, 
        facebook, 
        link, 
        timestamp 
    FROM 
        ticket_data;
    ''', conn)

    df = df.sort_values(['name', 'timestamp'], ascending=[True, False])

    conn.commit()
    conn.close()

    return df.iloc[1, :]

print(check_database())
