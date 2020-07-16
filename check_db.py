import pyodbc
import numpy as np
import pandas as pd
from database import *


def check_database():
    conn = pyodbc.connect(access)

    df = pd.read_sql_query('''
    SELECT 
        name,
        aangeboden, 
        verkocht, 
        gezocht,
        event_date, 
        location,
        city,
        country,
        facebook, 
        link, 
        timestamp 
    FROM 
        ticket_data;
    ''', conn)

    conn.commit()
    conn.close()

    df = df.sort_values(['name', 'timestamp'], ascending=[True, False])

    return print(df)

check_database()