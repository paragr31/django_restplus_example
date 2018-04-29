#!C:/ProgramData/Anaconda2/python
__author__ = 'parag rajabhoj'

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import configs.settings as config
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

class MyLogger:

    def __init__(self):
        self.logdir = config.LOG_DIR
        self.logfile = config.LOG_FILE
        self.logger = "TCP_SERVER"
        self.log_file = self.logdir + "/" + self.logfile

    def createLogDirectory(self):
        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)

    def getLogHandler(self):
        self.createLogDirectory()
        self.logger = logging.getLogger(str(self.logger))
        if not self.logger.handlers:
            #Adding File Handler
            self.logger.setLevel(logging.DEBUG)
            filehandler = ConcurrentRotatingFileHandler(self.log_file,"a",512*1024,5)
            filehandler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s : %(filename)s:%(lineno)s:%(funcName)s() -%(levelname)s - %(message)s')
            filehandler.setFormatter(formatter)
            self.logger.addHandler(filehandler)
            #Adding Console Handler
            consoleHandler = logging.StreamHandler()
            consoleHandler.setLevel(logging.INFO)
            cformatter = logging.Formatter('%(asctime)s -%(levelname)s - %(message)s')
            consoleHandler.setFormatter(cformatter)
            self.logger.addHandler(consoleHandler)
        return self.logger
