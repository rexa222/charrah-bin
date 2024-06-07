import logging
from typing import Optional
from logging.handlers import RotatingFileHandler


def config_uvicorn_logger():
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler("app.log")

    file_formatter = logging.Formatter('%(asctime)s -%(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    uvicorn_logger.addHandler(file_handler)

    return uvicorn_logger


logger = config_uvicorn_logger()
