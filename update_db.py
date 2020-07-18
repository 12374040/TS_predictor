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
    name varchar(255),
    aangeboden int, 
    verkocht int, 
    gezocht int, 
    event_date varchar(255), 
    timestamp varchar(255)
    );''')
    
    # update table
    new_values = [tuple(row) for row in data.itertuples(index=False)]
    c.executemany('''INSERT INTO ticket_data (
                                        name,
                                        aangeboden, 
                                        verkocht, 
                                        gezocht, 
                                        event_date, 
                                        timestamp) 
                                    VALUES 
                                        (?, ?, ?, ?, ?, ?);''', new_values)

    conn.commit()
    conn.close()

def update_links(links):
    '''Update db with links'''
    conn = pyodbc.connect(access)
    c = conn.cursor()

    c.execute('''IF OBJECT_ID('dbo.link_data', 'U') IS NULL
    CREATE TABLE link_data (
    name varchar(255),
    event_date varchar(255),
    location varchar(255),
    city varchar(255),
    country varchar(255),
    facebook varchar(255), 
    link varchar(255),
    );''')

    # update table
    new_links = [tuple(row) for row in links.itertuples(index=False)]

    c.execute('''SELECT * FROM link_data''')
    old_links = [tuple(row) for row in c.itertuples(index=False)]

    links_to_add = [tuple(row) for row in new_links.itertuples(index=False) if row not in old_links]

    # add new links to table
    c.executemany('''INSERT INTO link_data (
                                        name,
                                        event_date,
                                        location,
                                        city,
                                        country,
                                        facebook,
                                        link)
                                    VALUES
                                        (?, ?, ?, ?, ?, ?, ?);''', links_to_add)

    conn.commit()
    conn.close()
