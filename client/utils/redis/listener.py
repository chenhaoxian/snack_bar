# -*- coding:utf-8 -*-
import json

from utils.redis.helper import RedisHelper
from utils.encoding_helper import encoding_validation, EncodingIncorrect
from config import logger, config_option


def listen(queue):
    host = config_option["host"]
    port = config_option["port"]
    password = config_option["password"]
    chanel = config_option["chanel"]

    _redis = RedisHelper(host, port, password, chanel)
    while True:
        msg = _redis.get_msg()
        if msg:
            data = json.loads(msg['data'])
            try:
                encoding_validation(data)
                queue.put(data)
            except EncodingIncorrect as e:
                logger.info(e)
