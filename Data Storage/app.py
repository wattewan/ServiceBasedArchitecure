import connexion

import yaml
import pymysql
import mysql.connector

from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from ionian_champion import IonianChampion
from piltover_champion import PiltoverChampion
from sqlalchemy import and_, func
import datetime
from datetime import datetime
from pykafka import KafkaClient
from threading import Thread
import json
import logging
import logging.config
from flask_cors import CORS,cross_origin

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')



try:
    with open('/config/app_conf.yml', 'r') as f:
        app_config = yaml.safe_load(f.read())
except IOError:
    with open('app_conf.yml', 'r') as f:
        app_config = yaml.safe_load(f.read())





user = app_config['datastore']['user']
password = app_config['datastore']['password']
hostname = app_config['datastore']['hostname']
port = app_config['datastore']['port']
db = app_config['datastore']['db']

login = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, hostname, port, db)


DB_ENGINE = create_engine(login)



Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)



# def add_ionian_champion(reading):
#     """ Adds a ionian champion to database """

#     session = DB_SESSION()

#     ic = IonianChampion(reading['champ_id'],
#                        reading['champ_name'],
#                        reading['weapon'],
#                        reading['role'])

#     session.add(ic)

#     session.commit()
#     session.close()

#     return NoContent, 201



def get_ionian_champion(startDate, endDate):
    """ Gets an ionian champions info from database """

    results_list = []
    

    session = DB_SESSION()

    print(startDate)
    print(endDate)

    results = session.query(IonianChampion).filter(IonianChampion.date_created >= datetime.fromisoformat(startDate), IonianChampion.date_created <= datetime.fromisoformat(endDate))
    
    

    for result in results:
        print("Specific result:", result)
        results_list.append(result.to_dict())


    print("List: ", results_list)
    print("DB request output: ", results)
    session.close()

    return results_list, 200




# def add_piltover_champion(reading):
#     """ Add a piltover champion to database """

#     session = DB_SESSION()

#     pc = PiltoverChampion(reading['champ_id'],
#                    reading['champ_name'],
#                    reading['technology_used'],
#                    reading['city'])

#     session.add(pc)

#     session.commit()
#     session.close()

#     return NoContent, 201



def get_piltover_champion(startDate, endDate):
    """ Get a plitover champions information from the database """

    results_list = []

    session = DB_SESSION()

    results = session.query(PiltoverChampion).filter(PiltoverChampion.date_created >= datetime.fromisoformat(startDate), PiltoverChampion.date_created <= datetime.fromisoformat(endDate))


    for result in results:
        results_list.append(result.to_dict())

    session.close()

    return results_list, 200




def process_messages():

    with open('app_conf.yaml', 'r') as app_config:
        app_config = yaml.safe_load(app_config.read())

        


        kafka_server = app_config['kafka']['kafka-server']
        kafka_port = app_config['kafka']['kafka-port']
        kafka_topic = app_config['kafka']['topic']

        client = KafkaClient(hosts='{}:{}'.format(kafka_server, kafka_port))
        topic = client.topics['{}'.format(kafka_topic)]

        consumer = topic.get_simple_consumer(consumer_group="events", auto_commit_enable=True)


        for message in consumer:
            message_string = message.value.decode('utf-8')
            message_value = json.loads(message_string)
            print("checking Ionian")
            if message_value['type'] == "ionian_champion":
                session = DB_SESSION()
                
                champion = message_value['payload']
                print(champion)
                
                ic = IonianChampion(champion['champ_id'],
                                champion['champ_name'],
                                champion['weapon'],
                                champion['role'])

                session.add(ic)

                session.commit()
                session.close()

            logger.info(f'New Message: {message_string}')
            if message_value["type"] == "piltover_champion":
                    session = DB_SESSION()

                    champion = message_value['payload']

                    pc = PiltoverChampion(champion['champ_id'],
                                champion['champ_name'],
                                champion['technology_used'],
                                champion['city'])

                    session.add(pc)

                    session.commit()
                    session.close()
    


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS']='Content-Type'
app.add_api ("openapi.yaml")



if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)