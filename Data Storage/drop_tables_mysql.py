import mysql.connector

db_conn = mysql.connector.connect(host="cloudserver-acit3855.westus.cloudapp.azure.com", user="root", password="password", database="events")

db_cursor = db_conn.cursor()


db_cursor.execute('''
                  DROP TABLE ionian_champion, piltover_champion
                  ''')


db_conn.commit()
db_conn.close()