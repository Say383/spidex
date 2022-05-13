from datetime import datetime
from loguru import logger

#Decorator that return execution time of some functions
def execution_time(function):

    def get_time(*args, **kwargs):
        start = datetime.now()
        c = function(*args, **kwargs)
        logger.info("Execution time: {}".format(datetime.now() - start))
        return c

    return get_time
