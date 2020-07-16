import pyodbc
import numpy as np
import pandas as pd
from database import *


def check_database():
    conn = pyodbc.connect('DRIVER={};PORT=1433;SERVER={};PORT=1443;DATABASE={};UID={};PWD={}'.format(*access))

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

    conn.commit()
    conn.close()

    df = df.sort_values(['name', 'timestamp'], ascending=[True, False])

    return print(df.iloc[0, :])

check_database()