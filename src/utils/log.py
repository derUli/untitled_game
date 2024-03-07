""" Logging utilities """

import logging
import os
import platform
import sys
from logging.handlers import RotatingFileHandler

import arcade
import psutil
import sounddevice

from . import path
from .text import label_value

log_file = os.path.join(path.get_userdata_path(), 'debug.log')
if not os.path.exists(path.get_userdata_path()):
    os.makedirs(path.get_userdata_path())

file_handler = RotatingFileHandler(
    filename=log_file,
    maxBytes=5 * 1024 * 1024,  # Maximum log file size 5 MB
    # Keep previous 3 log files
    backupCount=3,
)
stdout_handler = logging.StreamHandler(stream=sys.stdout)

handlers = [file_handler, stdout_handler]


def configure_logger(log_level: int | str = logging.INFO) -> None:
    """ Configure logger
    @param log_level: Log level
    """
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )


def log_hardware_info() -> None:
    """
    Log hardware info
    """

    # Log OS info
    uname = platform.uname()
    logging.info(label_value('OS', f"{uname.system} {uname.version}"))

    # Log CPU model
    logging.info(label_value('CPU', uname.processor))

    # Log the ram size
    ram_size = round(psutil.virtual_memory().total / 1024 / 1024 / 1024)
    logging.info(label_value('RAM', f"{ram_size} GB"))

    # Open a hidden window to get the renderer
    window = arcade.Window(visible=False)
    # The renderer is the GPU model
    renderer = window.ctx.info.RENDERER
    window.close()

    # Log the GPU model
    logging.info(label_value('GPU', renderer))

    # Log the audio devices
    for audio in sounddevice.query_devices():
        logging.info(label_value('Audio', audio['name']))
