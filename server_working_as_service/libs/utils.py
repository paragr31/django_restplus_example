#!C:/ProgramData/Anaconda2/python
__author__ = 'parag rajabhoj'
import random
import string
import json
import time
from log_mgr import MyLogger

class MyUtilities:
    
    def __init__(self,buffer_size):
        self.BUFFER_SIZE = buffer_size
        obj = MyLogger()
        self.logger = obj.getLogHandler()
        
    def set_length(self,length):
        self.length = length
    
    def get_length(self):
        return self.length
        
    def get_chunks(self, string):
        for i in xrange(0, len(string), self.BUFFER_SIZE):
            yield string[i:i+self.BUFFER_SIZE]
            
    def get_string(self,length):
        try:
            if type(length) == int and length > 0:
                return ''.join(random.choice(string.lowercase) for x in range(length))
            else:
                self.logger.debug("Requested Parameter should be Integer and Should be greator than Zero.")
        except Exception as err:
            self.logger.debug("Exception occured %s"% err)
    
    def get_num(self,length):
        try:
            if type(length) == int and length > 0:
                return random.randint(1,length)
            else:
                self.logger.debug("Requested Parameter should be Integer and Should be greator than Zero.")
        except Exception as err:
            self.logger.debug("Exception occured %s"% err)