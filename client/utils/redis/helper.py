# -*- coding:utf-8 -*-
import redis
import time


class RedisHelper(object):
    def __init__(self, host, port, password, chanel):
        self._conn = redis.Redis(host, port=port, password=password, decode_responses=True)
        self._chanel = chanel
        self._ps = None

    def publish(self, msg):
        self._conn.publish(self._chanel, msg)

    def subscribe(self):
        ps = self._conn.pubsub(ignore_subscribe_messages=True)
        ps.subscribe(self._chanel)
        self._ps = ps

    def get_msg(self):
        if self._ps is None:
            self.subscribe()
        message = self._ps.get_message()
        time.sleep(0.1)
        if message:
            return message
