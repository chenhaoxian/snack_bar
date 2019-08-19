import requests

from config import config_option
from utils.general_decorators.retry import Retry
from utils.logger.decorator import dec_logging


@dec_logging(exit=True, trace=False)
@Retry(3, 1)
def load_all_encoding():
    r = requests.request('GET', config_option['BACKEND_URL'] + config_option['ENDPOINT'],timeout=3)
    r.raise_for_status()
    return r.json()