import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS base;')

conn.commit()
conn.close()