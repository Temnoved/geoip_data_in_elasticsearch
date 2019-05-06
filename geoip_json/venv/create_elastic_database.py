import requests
import pprint
import random
import datetime
import json
from elasticsearch import Elasticsearch

random.seed(datetime.datetime.now())

ELASTIC_HOST = "192.168.0.92"
ELASTIC_PORT = 9200

def get_location_info(work_ip: str = ""):
    return requests.get(f"http://ip-api.com/json/{work_ip}").json()


if __name__ == "__main__":
    es = Elasticsearch([{"host": ELASTIC_HOST, "port": ELASTIC_PORT}])
    es.indices.create(index="geoip", ignore=400)
    geoip_info_list = []
    elastic_index: int = 1
    while (elastic_index <= 6):
        random_ip_raw = [str(random.randrange(15, 220)) for _ in range(4)]
        current_ip = ".".join(random_ip_raw)
        current_geoip_info = get_location_info(current_ip)
        check_create_index = es.index(index='geoip',\
                                      body=current_geoip_info,\
                                      id=elastic_index, doc_type="geoipinfo")
        print(f"index={check_create_index['_id']}",\
              f"result={check_create_index['result']}")
        geoip_info_list.append(current_geoip_info)
        elastic_index += 1


    for geo_json in geoip_info_list:
        print(geo_json)
