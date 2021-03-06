import mysql.connector
import numpy as np
import pandas as pd
import time
from datetime import datetime
from database import *

def update_database(data): 
    '''Update db with scraped data'''
    print('updating...')
    timestamp = datetime.now(tz=None).strftime("%Y/%m/%d %H:%M:%S")

    conn = mysql.connector.connect(**access)
    
    
    c = conn.cursor(buffered=True)

    # create table if not exists
    # c.execute('''CREATE TABLE IF NOT EXISTS ticket_data (
    # ID int,
    # aangeboden int, 
    # verkocht int, 
    # gezocht int,
    # laagste_prijs varchar(255),
    # timestamp timedate
    # );''')
    
    # update table
    new_values = [tuple(row) for row in data.itertuples(index=False)]
    
    limit = len(new_values)
    # check if the entry will be different from the last
    c.execute('''SELECT ID, aangeboden, verkocht, gezocht, laagste_prijs
                FROM ticket_data
                    ORDER BY timestamp DESC
                    LIMIT %s''', (limit,)) 
    old_values = [tuple(row) for row in c]
    

    values_to_add = [tuple(row) for row in new_values if row not in old_values]
    print('values to add')
    print(values_to_add)

    values_to_update = [row[0] for row in new_values if row in old_values] # for setting all unchanged last values to the current timestamp
    print('values to update')
    print(values_to_update)
    
    time_list = [timestamp] * len(values_to_update)
    
    c.execute('SELECT timestamp FROM ticket_data ORDER BY timestamp DESC LIMIT 1')
    last_timestamp = [row for row in c]
    last_time_list = [last_timestamp] * len(values_to_update)
    
    data_timestamp = list(zip(time_list,values_to_update, last_time_list))# combining 3 lists to tuple list
    
    c.executemany('''INSERT INTO ticket_data (
                                        ID,
                                        aangeboden, 
                                        verkocht, 
                                        gezocht, 
                                        laagste_prijs) 
                                    VALUES 
                                        (%s, %s, %s, %s, %s);''', values_to_add)
    c.execute('UPDATE ticket_data SET timestamp = %s WHERE timestamp IS NULL;', (timestamp,))# set timestamp for added values
    c.executemany('UPDATE ticket_data SET timestamp = %s WHERE ID = %s AND timestamp = %s', (data_timestamp)) # set all unchanged last vcalues to current timestamp
    conn.commit()
    conn.close()

def update_links(links):
    '''Update db with links'''
    
    conn = mysql.connector.connect(**access)
    
    c = conn.cursor()

    # c.execute('''CREATE TABLE IF NOT EXISTS link_data (
    # ID int NOT NULL AUTO_INCREMENT,
    # name varchar(255),
    # event_date varchar(255),
    # location varchar(255),
    # city varchar(255),
    # country varchar(255),
    # facebook varchar(255), 
    # link varchar(255),
    # PRIMARY KEY (ID)
    # );''')

    # update table
    new_links = [tuple(row) for row in links.itertuples(index=False)]

    c.execute('''SELECT name, event_date, location, city, country, facebook, link FROM link_data''')
    old_links = [tuple(row) for row in c]
    print('old links')
    print(old_links)
    links_to_add = [tuple(row) for row in new_links if row not in old_links]
    print('links to add')
    print(links_to_add)
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
                                        (%s, %s, %s, %s, %s, %s, %s);''', links_to_add)

    conn.commit()
    conn.close()
