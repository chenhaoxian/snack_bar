import functools

import redis
import json

from util.read_config import ConfigReader


class DataNotifier:

    def publish_change_to_redis_chanel(config,face):
        redis_host = config.get("redis", "host")
        redis_port = config.get("redis", "port")
        redis_password = config.get("redis", "password")
        r = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
        r.publish(config.get("redis", "chanel"), json.dumps(face, default=lambda x: x.__dict__))
