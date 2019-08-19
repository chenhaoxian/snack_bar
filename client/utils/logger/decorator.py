import functools

import sys

from config import logger


def dec_logging(*args, **kwargs):
    def exec_func(func, *_args, **_kwargs):
        @functools.wraps(func)
        def wrapper(*__args, **__kwargs):
            try:
                return func(*__args, **__kwargs)
            except Exception as e:
                if "trace" in _kwargs.keys() and _kwargs.get("trace"):
                    logger.exception("Exception for function: %s.%s" % (func.__module__, func.__name__,))
                else:
                    logger.error(e)

                if "exit" in _kwargs.keys() and _kwargs.get("exit"):
                    sys.exit(-1)

        return wrapper

    # if there is no any args pass to the decorator, just simply wrap the function
    if len(args) == 1 and callable(args[0]):
        return exec_func(args[0])
    # else pass all the args / kwargs to the wrapper function
    else:
        def decorator(func):
            return exec_func(func, *args, **kwargs)

        return decorator
