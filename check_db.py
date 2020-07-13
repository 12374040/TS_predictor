import sqlite3
import numpy
import pandas as pd

def check_database():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    df = pd.DataFrame(c.execute('SELECT * FROM base;'), columns=['name', 'event_date', 'location', 'facebook', 'aangeboden', 'gezocht', 'verkocht', 'timestamp'])
    df = df.sort_values(['name', 'timestamp'], ascending=[True, False])
    conn.commit()
    conn.close()

    return df.head(50)


print(check_database())
