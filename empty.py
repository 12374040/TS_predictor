import pyodbc

server = 'ticketscrape.database.windows.net'
database = 'ts_db'
username = 'data_admin'
password = 'Kaasisbaas4'
driver= '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
c = conn.cursor()

c.execute('DROP TABLE ticket_data;')

conn.commit()
conn.close()