import pyodbc
import numpy as np
import pandas as pd
from database import *

def update_database(data): 
    '''Update db with scraped data'''
    print('updating...')

    conn = pyodbc.connect('DRIVER={};PORT=1433;SERVER={};PORT=1443;DATABASE={};UID={};PWD={}'.format(*access))
    c = conn.cursor()

    # create table if not exists
    c.execute('''IF OBJECT_ID('dbo.ticket_data', 'U') IS NULL
    CREATE TABLE ticket_data (
    aangeboden int, 
    verkocht int, 
    gezocht int, 
    name varchar(255), 
    event_date varchar(255), 
    location varchar(255), 
    facebook varchar(255), 
    link varchar(255),
    timestamp varchar(255)
    );''')
    
    # update table
    new_values = [tuple(row) for row in data.itertuples(index=False)]
    c.executemany('INSERT INTO ticket_data (aangeboden, verkocht, gezocht, name, event_date, location, facebook, link, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);', new_values)

    conn.commit()
    conn.close()

