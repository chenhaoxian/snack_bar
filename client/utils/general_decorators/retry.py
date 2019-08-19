# -*- coding: utf-8 -*-
import functools
import time

from config import logger


class RetryFailed(Exception):
    def __init__(self, func, times):
        super(RetryFailed, self).__init__(
            "Retry \"{location}\" {time_count} times, failed.".format(
                location=func.__module__ + "." + func.__name__,
                time_count=times
            )
        )


class Retry(object):
    def __init__(self, times, interval):
        self._times = times
        self._interval = interval

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            for _ in range(self._times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    count += 1
                    logger.error(e)
                    time.sleep(self._interval)
            else:
                raise RetryFailed(func, times=count)

        return wrapper
