from mylogger import LoggerMixin
import multiprocessing
from multiprocessing.pool import Pool
import time

class MyTest(LoggerMixin, object):
    def __init__(self):
        self.logDir = "C:\\PARAG\\JIRA_GSD_APP"
    
    def hello_parag(self,message):
        self.logger.info(message)
        self.logger.debug(message)
        time.sleep(10)

def hello_msg(msg):
    obj = MyTest()
    obj.hello_parag(msg)
    
if __name__ == '__main__':
    pool = Pool(2)
    data = ["test1","test2","test3","test4","test5"]
    pool.map(hello_msg,data)
    pool.close()
    pool.join()
    
