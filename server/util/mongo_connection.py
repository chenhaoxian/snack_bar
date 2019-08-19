from pymongo import MongoClient
import configparser
import os
from util import read_config


class MongoConnector:
    def __init__(self):
        config = read_config.ConfigReader().get_config()
        self.test = config.get("mongodb", "host")
        self.mongo_host = config.get("mongodb", "host")
        self.mongo_port = int(config.get("mongodb", "port"))
        self.db_name = config.get("mongodb", "db_name")

    def init_db(self):
        client = MongoClient(self.mongo_host, self.mongo_port)
        face_db = client[self.db_name]
        return face_db
