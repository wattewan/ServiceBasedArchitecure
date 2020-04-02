import connexion
from connexion import NoContent
import requests
import yaml
import json
import datetime
import logging
import logging.config

from pykafka import KafkaClient

from flask_cors import CORS, cross_origin


try:
    with open('/config/app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())
except IOError:
    with open('app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())

   
with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger') 








def add_ionian_champion(info):
    """ Adds a ionian champion """


    # db_request = 'http://localhost:8090/ionia/champions'

    # results = requests.post(db_request, json = info, 
    # headers={'Content-Type': 'application/json'}
    # )


    kafka_server = app_config['kafka']['kafka-server']
    kafka_port = app_config['kafka']['kafka-port']
    topic = app_config['topic']


    
    client = KafkaClient(hosts='{}:{}'.format(kafka_server, kafka_port))
    topic = client.topics['{}'.format(topic)]
    producer = topic.get_sync_producer()
    msg = { "type": "ionian_champion",
            "datetime": 
                datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"),
                "payload": info }
    print(msg)
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info('Ionian Champion Info: ' + msg_str)

    return NoContent, 200




def add_piltover_champion(info):
    """ Add a Piltover champion """


    # db_request = 'http://localhost:8090/piltover/champions'

    # results = requests.post(db_request, json = info, 
    # headers={'Content-Type': 'application/json'}
    # )



    kafka_server = app_config['kafka']['kafka-server']
    kafka_port = app_config['kafka']['kafka-port']
    topic = app_config['topic']

    client = KafkaClient(hosts='{}:{}'.format(kafka_server, kafka_port))
    topic = client.topics['{}'.format(topic)]
    producer = topic.get_sync_producer()
    msg = { "type": "piltover_champion",
            "datetime": 
                datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"),
                "payload": info }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info('Piltover Champion Info: ' + msg_str)

    return NoContent, 200













app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS']='Content-Type'
app.add_api ("openapi.yaml")





if __name__ == "__main__":
    app.run(port=8080)