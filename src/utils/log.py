""" Logging utilities """

import logging
import os
import platform
import sys

import psutil
from gpudetect import detect_gpus

from utils.path import get_userdata_path

log_file = os.path.join(get_userdata_path(), 'debug.log')
if not os.path.exists(get_userdata_path()):
    os.makedirs(get_userdata_path())

file_handler = logging.FileHandler(filename=log_file)
stdout_handler = logging.StreamHandler(stream=sys.stdout)

handlers = [file_handler, stdout_handler]


def configure_logger(log_level) -> None:
    """ Configure logger """
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )


def log_hardware_info():
    uname = platform.uname()
    logging.info(f"OS: {uname.system} {uname.version}")
    logging.info(f"CPU: {uname.processor}")
    logging.info(f"RAM: {round(psutil.virtual_memory().total / 1024 / 1024)} MB")

    gpus = detect_gpus()

    for gpu in gpus:
        logging.info(f'GPU: {gpu}')

    if not any(gpus):
        logging.info('GPU: Unknown')