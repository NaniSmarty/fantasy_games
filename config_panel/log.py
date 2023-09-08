import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

import requests

var = datetime.now()
# var1 = var.date()
s =var.strftime("%d-%m-%Y")
# print(s)
#
# IO_log_flag = 0
#
# IOlog_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
# IOlogFile = '/home/narayanaraju/fantasy_game/log/IOlog'+str(s)+'.txt'
# IOmy_handler = RotatingFileHandler(IOlogFile, mode='a', maxBytes=10*1024*1024, backupCount=500, encoding=None, delay=0)
# IOmy_handler.setFormatter(IOlog_formatter)
# IOmy_handler.setLevel(logging.INFO)
# io_log = logging.getLogger('root1')
# io_log.setLevel(logging.INFO)
# io_log.addHandler(IOmy_handler)

class graylog_io:
    def info(logroot, req_id, data, method, client_ip):
        json_body={
         "short_message": method,
         "host": "Fantasy_Game",
         "_ip": client_ip,
         "_req_id": req_id,
         "facility": "0",           #0 - app  1 - error
         "_logroot": logroot,   # DB-in DB-out REQ RES
         "_message": "logTxt",
         "full_message": data
        }
        requests.post("http://192.168.10.155:12212/gelf", json=json_body)

class graylog_error():
    def exception(trace_back, req_id, error, method, data, client_ip):
        json_body = {
            "short_message": method,
            "host": "Fantasy_Game",
            "facility": "1",
            "_ip": client_ip,
            "_req_id": req_id,
            "_message": error,
            "_trace": trace_back,
            "full_message": data
        }
        requests.post("http://192.168.10.155:12212/gelf", json=json_body)


err_log = graylog_error
app_log = graylog_io
