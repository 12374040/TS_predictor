import pyodbc
from database import *

conn = pyodbc.connect(access)
c = conn.cursor()

c.execute('DROP TABLE ticket_data;')

conn.commit()
conn.close()

