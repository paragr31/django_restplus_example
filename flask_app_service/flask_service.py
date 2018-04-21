#!C:/ProgramData/Anaconda2/python

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import os
from flask import Flask,jsonify,abort,make_response,request
from sql_connect import SQLLiteDB
from log_mgr import getLogHandler

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/raise_request',methods=['POST'])
def raise_request():
    """
    This api will log the request in database
    """
    logger = getLogHandler("flas_api_service")
    logger.info("*************** Start logging for new request for raise_request method ***************")
    logger.info("Request receied with following request body")
    logger.info(request.json)
    requester = request.json['requester']
    obj = SQLLiteDB(BASE_DIR + "\\summitqueue.db")
    request_id = obj.raise_request(requester)
    logger.info("*************** end logging for raise_request method ***************")
    return jsonify({"request_id": request_id})
    
@app.route('/request_status',methods=['POST'])
def request_status():
    """
    This api will return the request status
    """
    logger = getLogHandler("flas_api_service")
    logger.info("*************** Start logging for new request for request_status method ***************")
    logger.info("Request receied with following request body")
    logger.info(request.json)
    request_id = request.json['request_id']
    obj = SQLLiteDB(BASE_DIR + "\\summitqueue.db")
    data = obj.get_status(request_id)
    logger.info("*************** end logging for request_status method ***************")
    return jsonify({"responce": data})
    
@app.route('/all_requests',methods=['GET'])
def all_requests():
    """
    This api will return all the requests
    """
    logger = getLogHandler("flas_api_service")
    logger.info("*************** Start logging for new request for all_requests method ***************")
    logger.info("Request receied with following request body")
    logger.info(request.json)
    obj = SQLLiteDB(BASE_DIR + "\\summitqueue.db")
    data = obj.all_requests()
    logger.info("*************** end logging for all_requests method ***************")
    return jsonify({"responce": data})

@app.route('/pending_requests',methods=['GET'])
def pending_requests():
    """
    This api will return all pending requests
    """
    logger = getLogHandler("flas_api_service")
    logger.info("*************** Start logging for new request for pending_requests method ***************")
    logger.info("Request receied with following request body")
    logger.info(request.json)
    obj = SQLLiteDB(BASE_DIR + "\\summitqueue.db")
    data = obj.pending_requests()
    logger.info("*************** end logging for pending_requests method ***************")
    return jsonify({"responce": data})
    
@app.route('/delete_request',methods=['POST'])
def delete_request():
    """
    This api will delete given request
    """
    logger = getLogHandler("flas_api_service")
    logger.info("*************** Start logging for new request for delete_request method ***************")
    logger.info("Request receied with following request body")
    logger.info(request.json)
    request_id = request.json['request_id']
    obj = SQLLiteDB(BASE_DIR + "\\summitqueue.db")
    data = obj.delete_request(request_id)
    logger.info("*************** end logging for delete_request method ***************")
    return jsonify({"responce": data})  

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "FlaskRESTAPIApp"
    _svc_display_name_ = " Test Service to Check Flask API connectivitiry as windows service."


    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                          servicemanager.PYS_SERVICE_STARTED,
                          (self._svc_name_,''))
        self.main()

    def main(self):
        # Your business logic or call to any class should be here
        # this time it creates a text.txt and writes Test Service in a daily manner 
        app.run(threaded=True,debug=False,host='0.0.0.0',port=9092)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)