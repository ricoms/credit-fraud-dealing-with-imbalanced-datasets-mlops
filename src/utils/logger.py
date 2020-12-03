import os
import logging

from pythonjsonlogger import jsonlogger


def setup_json_logger():
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    json_logger = logging.getLogger()
    json_logger.setLevel(log_level)

    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter('%(message)%(levelname)%(name)%(asctime)')
    log_handler.setFormatter(formatter)
    json_logger.addHandler(log_handler)

    return json_logger


logger = setup_json_logger()
