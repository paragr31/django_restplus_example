__author__ = 'parag rajabhoj'

import os
import sys
import pickle
import functools
import time
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def getLogHandler(vmId):
    """
        Creates a log handler for each vm based on vm id
    """
    logger = logging.getLogger(str(vmId))
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        log_file = BASE_DIR + "\\flas_api_service.log"
        fileHandler = logging.FileHandler(log_file)
        fileHandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s : %(filename)s:%(lineno)s:%(funcName)s() -\t%(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
    return logger
