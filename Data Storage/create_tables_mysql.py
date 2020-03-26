import mysql.connector

db_conn = mysql.connector.connect(host="localhost", user="root", password="P@ssw0rd", database="events")


db_cursor = db_conn.cursor()

db_cursor.execute('''
          CREATE TABLE ionian_champion
          (id INT NOT NULL AUTO_INCREMENT, 
           champ_id VARCHAR(25) NOT NULL,
           champ_name VARCHAR(25) NOT NULL,
           weapon VARCHAR(25) NOT NULL,
           role VARCHAR(25) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT ionian_champion_pk PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE piltover_champion
          (id INT NOT NULL AUTO_INCREMENT, 
           champ_id VARCHAR(25) NOT NULL,
           champ_name VARCHAR(25) NOT NULL,
           technology_used VARCHAR(100) NOT NULL,
           city VARCHAR(25) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT piltover_champion PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()