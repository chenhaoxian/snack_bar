import logging
from logging.config import fileConfig
import os
import configparser

env = os.getenv("env", "dev")

configuration = configparser.ConfigParser()
configuration.read('./config/config.ini')
config_option = configuration[env]

fileConfig(os.path.abspath('./config/logger.ini'))
logger = logging.getLogger("root")
logger.info("Current env: %s" % env.upper())
logger.debug('Logger working good!')