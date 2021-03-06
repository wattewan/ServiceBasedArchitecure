import connexion
from connexion import NoContent
import requests
import yaml
import json
from pykafka import KafkaClient
from flask_cors import CORS,cross_origin

try:
    with open('/config/app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())
except IOError:
    with open('app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())


def event1_offset(Offset):
    

  


    kafka_server = app_config['kafka']['kafka-server']
    kafka_port = app_config['kafka']['kafka-port']
    kafka_topic = app_config['topic']

    client = KafkaClient(hosts='{}:{}'.format(kafka_server, kafka_port))
    topic = client.topics['{}'.format(kafka_topic)]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=500)
    for message in consumer:
        message_string = message.value.decode('utf-8')
        message_value = json.loads(message_string)
        
        if (message.offset == Offset) and (message_value['type'] == "ionian_champion"):
            
            return message_value['payload'], 200


    return 400



def event2_oldest():



    


    kafka_server = app_config['kafka']['kafka-server']
    kafka_port = app_config['kafka']['kafka-port']
    kafka_topic = app_config['topic']

    client = KafkaClient(hosts='{}:{}'.format(kafka_server, kafka_port))
    topic = client.topics['{}'.format(kafka_topic)]
    

    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=500)
    for message in consumer:
        message_string = message.value.decode('utf-8')
        message_value = json.loads(message_string)
        if message_value["type"] == "piltover_champion":
            
            return message_value['payload'], 200
        

    return 400


def all_history():


    message_list = []


    kafka_server = app_config['kafka']['kafka-server']
    kafka_port = app_config['kafka']['kafka-port']
    kafka_topic = app_config['topic']

    client = KafkaClient(hosts='{}:{}'.format(kafka_server, kafka_port))
    topic = client.topics['{}'.format(kafka_topic)]
    

    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=500)
    for message in consumer:
        message_string = message.value.decode('utf-8')
        message_value = json.loads(message_string)
        print("Offeset: " + str(message.offset) + " Type: " + message_value['type'] + " Message: " + str(message_value['payload']))
        message_list.append("Offeset: " + str(message.offset) + " Type: " + message_value['type'] + " Message: " + str(message_value['payload']))

    
        

    return message_list, 200














app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS']='Content-Type'
app.add_api ("openapi.yaml")



if __name__ == "__main__":
    app.run(port=8110)