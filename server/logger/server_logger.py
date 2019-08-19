import functools
import logging

class ServerLogger:


    def log(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('call %s():' % func.__name__)
            logging.info('call %s():' % func.__name__)
            return func(*args, **kw)

        return wrapper

    def log_with_msg(text):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kw):
                print('%s %s():' % (text, func.__name__))
                logging.info('%s %s():' % (text, func.__name__))
                return func(*args, **kw)

            return wrapper

        return decorator