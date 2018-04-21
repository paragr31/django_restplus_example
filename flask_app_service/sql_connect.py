import sqlite3
import datetime
import time
from pprint import pprint

class SQLLiteDB:

    def __init__(self,db_name):
        self.db_name = db_name
        self.conn = self.connect()
        
    def connect(self):
        return sqlite3.connect(self.db_name)
        
    def create_table(self):
        if not self.conn:
            self.conn = self.connect()
        self.cursor = self.conn.cursor()
        query = "CREATE TABLE request_queue (request_id integer primary key autoincrement,requester char(250) not null,request_time timestamp not null,request_status text not null, request_message text)"
        self.cursor.execute(query)
        self.cursor.close()
        self.conn.commit()
    
    def drop_table(self):
        if not self.conn:
            self.conn = self.connect()
        self.cursor = self.conn.cursor()
        query = "drop table request_queue"
        self.cursor.execute(query)
        self.cursor.close()
        self.conn.commit()
        
    def get_status(self,request_id):
        if not self.conn:
            self.conn = self.connect()
        self.cursor = self.conn.cursor()
        request_id = int(request_id)
        self.cursor.execute("""select * from request_queue where request_id = ?""",[request_id])
        data = self.cursor.fetchall()
        self.cursor.close()
        return data
        
    def all_requests(self):
        if not self.conn:
            self.conn = self.connect()
        self.cursor = self.conn.cursor()
        self.cursor.execute("""select * from request_queue order by request_id""")
        data = self.cursor.fetchall()
        self.cursor.close()
        return data
        
    def pending_requests(self):
        if not self.conn:
            self.conn = self.connect()
        self.cursor = self.conn.cursor()
        self.cursor.execute("""select * from request_queue where request_status = 'pending' order by request_id""")
        data = self.cursor.fetchall()
        self.cursor.close()
        return data
    
    def get_timestamp(self):
        ts = time.time()
        req_time = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H-%M-%S")
        return req_time
        
    def raise_request(self,requester):
        if not self.conn:
            self.conn = self.connect()
        self.cursor = self.conn.cursor()
        ts = self.get_timestamp()
        self.cursor.execute("""INSERT INTO request_queue (requester,request_time,request_status,request_message) VALUES (?,?,?,?)""",(requester,ts,'pending',""))
        status = self.cursor.lastrowid
        self.conn.commit()
        self.cursor.close()
        return status
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
            
if __name__ == "__main__":
    
    obj = SQLLiteDB("summitqueue.db")
    #obj.drop_table()
    #obj.create_table()
    #obj.raise_request()
    data = obj.all_requests()
    print data