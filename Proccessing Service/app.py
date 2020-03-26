import connexion

from connexion import NoContent

import requests

import json

import datetime

import yaml

import logging
import logging.config
from apscheduler.schedulers.background import BackgroundScheduler

import os.path
from flask_cors import CORS,cross_origin


with open('log_conf.yaml', 'r') as f:
        log_config = yaml.safe_load(f.read())
        logging.config.dictConfig(log_config)


logger = logging.getLogger('basicLogger')

with open('app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())

datastore = app_config['datastore']['filename']



def get_champion_stats():
    """ Get a champion event stats """
    logger.info("Get request started")
    curr_info = {}

    if os.path.isfile(datastore):
        with open(datastore, 'r') as json_data:
            data = json.load(json_data)


            for item in data:
                curr_info.update(item)
            logger.debug("Current info: " + str(curr_info))
            logger.info("Get request completed")
            return curr_info, 200
    else:
        logger.error("Error no data exists")
        return 404
        


    

    


def populate_stats():
    """ Periodically update stats """

    logger.info("Start Periodic Processing")
    

    if os.path.isfile(datastore):
        with open(datastore, 'r') as json_data:
            data = json.load(json_data)
    else:
        data = [
            {
                "num_champion_ionia": 0
            },
            {
                "num_champion_piltover": 0
            },
            {
                "timestamp": '2020-01-01T11:55:01'

            }
            ]

        with open(datastore, 'w') as json_data:
            json.dump(data, json_data)

    

    last_search = data[2]['timestamp']
    curr_datetime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    print(last_search)
    print(curr_datetime)

    try: 
        db_request = app_config['eventstore']['url'] + '/ionia/champions'
        results = requests.get(db_request,
        params={"startDate": last_search, 
        "endDate": curr_datetime})

        num_ionian_champions = len(results.json())
        logger.info("Num Ionian Champions: " + str(num_ionian_champions))
        # print("num_ionian_champions: ", len(results.json()))
    except Exception as e:
        logger.error("Error occured: " + str(e))

    try:
        db_request = app_config['eventstore']['url'] + '/piltover/champions'

        results = requests.get(db_request,
        params={"startDate": last_search, 
        "endDate": curr_datetime})



        num_piltover_champions = len(results.json())
        logger.info("Num Piltover Champions: " + str(num_piltover_champions))
        # print("num_piltover_champions: ", len(results.json()))

    except Exception as e:
        logger.error("Error occured: " + str(e))


    
    print(data[0]['num_champion_ionia'])
    print(data[1]['num_champion_piltover'])

    if ((num_ionian_champions > 0) or (num_piltover_champions > 0)):
        data = [
                {
                    "num_champion_ionia": (data[0]['num_champion_ionia'] + num_ionian_champions) 
                },
                {
                    "num_champion_piltover": (data[1]['num_champion_piltover'] + num_piltover_champions)
                },
                {
                    "timestamp": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                    
                }
                ]


        with open(datastore, 'w') as json_data:
            json.dump(data, json_data)
            logger.debug(str(data))

    else:
        data = [
                {
                    "num_champion_ionia": data[0]['num_champion_ionia'] 
                },
                {
                    "num_champion_piltover": data[1]['num_champion_piltover']
                },
                {
                    "timestamp": data[2]['timestamp']  
                }
                ]


        with open(datastore, 'w') as json_data:
            json.dump(data, json_data)
            logger.debug(str(data))

    
    




    # print("Timestamp: ", datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    logger.info("End Periodic Processing")



def init_scheduler():

    with open('app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())


    sched = BackgroundScheduler(deamon=True)
    sched.add_job(populate_stats,
                    'interval',
                    seconds=app_config['scheduler']['period_sec'])
    
    sched.start()



app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS']='Content-Type'
app.add_api ("openapi.yaml")





if __name__ == "__main__":
    
    init_scheduler()
    app.run(port=8100, use_reloader=False, debug=True)