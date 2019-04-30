import requests
import pprint
import random
import datetime
import json
from elasticsearch import Elasticsearch

random.seed(datetime.datetime.now())

ELASTIC_INDEX = "http://192.168.0.92:9200/"

def get_location_info(work_ip: str = ""):
    return requests.get("http://ip-api.com/json/" + work_ip).json()


if __name__ == "__main__":
    es = Elasticsearch([{"host": "192.168.0.92", "port": 9200}])
    es.indices.create(index="geoip", ignore=400)
    geoip_list = []
    elastic_index: int = 1
    while (elastic_index <= 6):
        list_for_create_random_ip = [str(random.randrange(15, 220)) for _ in range(4)]
        current_ip = ".".join(list_for_create_random_ip)
        current_geoip_info = get_location_info(current_ip)
        es.index(index='geoip', body=current_geoip_info, id=elastic_index, doc_type="geoipinfo")
        geoip_list.append(current_geoip_info)
        elastic_index += 1


    for geo_json in geoip_list:
        print(geo_json)