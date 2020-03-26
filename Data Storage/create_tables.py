import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE ionian_champion
          (id INTEGER PRIMARY KEY ASC, 
           champ_id VARCHAR(25) NOT NULL,
           champ_name VARCHAR(25) NOT NULL,
           weapon VARCHAR(25) NOT NULL,
           role VARCHAR(25) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE piltover_champion
          (id INTEGER PRIMARY KEY ASC, 
           champ_id VARCHAR(25) NOT NULL,
           champ_name VARCHAR(25) NOT NULL,
           technology_used VARCHAR(100) NOT NULL,
           city VARCHAR(25) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()