import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('DROP TABLE base;')
c.execute('DROP TABLE change;')

conn.commit()
conn.close()