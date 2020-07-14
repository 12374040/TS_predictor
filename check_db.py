import sqlite3
import numpy
import pandas as pd

def check_database():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    df = pd.DataFrame(c.execute('''
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
        base;
    '''), columns = [
        'name',
        'aangeboden',
        'verkocht',
        'gezocht',
        'event_date', 
        'location', 
        'facebook', 
        'link',  
        'timestamp'
        ])

    df = df.sort_values(['name', 'timestamp'], ascending=[True, False])
    conn.commit()
    conn.close()

    return df

def check_links():
    conn = sqlite3.connect('links.db')
    c = conn.cursor()

    lf = pd.DataFrame(c.execute('SELECT * FROM base;'), columns=['link'])
    conn.commit()
    conn.close()

    return lf.head(50)

#print(check_links())
print(check_database())
