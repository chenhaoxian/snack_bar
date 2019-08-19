import configparser
import os


class ConfigReader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = os.path.join(os.path.dirname(__file__), "../resource/config.ini")
        self.config.read(self.config_path)

    def get_config(self):
        return self.config
