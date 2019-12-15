import logging_config as conf
import logging
from logging.config import dictConfig
import re

class LoggerMixin(object):
    """
    A mixin that can be used to log messages
    """    
    loggerName = 'paragr'
    logDir = None
    logFile = conf.LOGGING['handlers']['file']['filename']
    
    @property
    def logger(self):
        logFileName = self.__getLogFile()
        if logFileName is not None:
            conf.LOGGING['handlers']['file']['filename'] = logFileName
        dictConfig(conf.LOGGING)
        return logging.getLogger(self.loggerName)
    
    def __getLogFile(self):
        if self.logDir is not None and self.logFile is not None:
            self.logDir = re.sub(r'\\',r'/',self.logDir)
            fileName = self.logDir + "/" + self.logFile
            return fileName
        else:
            return None
    
