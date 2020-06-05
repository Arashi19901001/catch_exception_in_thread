import logging
from logging.handlers import RotatingFileHandler
import datetime
import os

LOG_DIR = "logs"


def setup_logger(name="default", dir_name="", stream=True):
    logger = logging.getLogger(name)
    if dir_name:
        log_dir = os.path.join(LOG_DIR, dir_name)
    else:
        log_dir = LOG_DIR
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
    if name == "default":
        log_name = "manager_{}.log".format(datetime.datetime.now().strftime("%Y%m%d"))
    else:
        log_name = "{}_{}.log".format(name, datetime.datetime.now().strftime("%Y%m%d"))

    has_stream = False
    for h in logger.handlers:
        if isinstance(h, logging.StreamHandler):
            has_stream = True
            continue
        if h.baseFilename == os.path.abspath(os.path.join(log_dir, log_name)):
            return logger
    formatter = logging.Formatter('[%(asctime)s] [%(filename)s:%(lineno)d]  %(levelname)s - %(message)s')
    filehandler = RotatingFileHandler(filename=os.path.join(log_dir, log_name), encoding='utf-8', maxBytes=300 * 1024 * 1024, backupCount=5)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    logger.setLevel(logging.DEBUG)
    if stream and not has_stream:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger
