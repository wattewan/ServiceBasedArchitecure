import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE ionian_champion
          ''')

c.execute('''
          DROP TABLE piltover_champion
          ''')

conn.commit()
conn.close()