import pyodbc
from database import *

conn = pyodbc.connect('DRIVER={};PORT=1433;SERVER={};PORT=1443;DATABASE={};UID={};PWD={}'.format(*access))
c = conn.cursor()

c.execute('DROP TABLE ticket_data;')

conn.commit()
conn.close()

