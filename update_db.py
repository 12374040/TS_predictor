import pyodbc
import numpy as np
import pandas as pd
from database import *

def update_database(data): 
    '''Update db with scraped data'''
    print('updating...')

    conn = pyodbc.connect(access)
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
    city varchar(255),
    country varchar(255),
    facebook varchar(255), 
    link varchar(255),
    timestamp datetime
    );''')
    
    # update table
    new_values = [tuple(row) for row in data.itertuples(index=False)]
    c.executemany('''INSERT INTO ticket_data (
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
                                        timestamp) 
                                    VALUES 
                                        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', new_values)

    conn.commit()
    conn.close()

