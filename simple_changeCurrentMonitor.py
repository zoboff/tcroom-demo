# coding=utf8
'''
Created on 18.01.2022

@author: zobov

Command line:
simple_changeCurrentMonitor.py -room_ip <room IP> -monitor <trueconf id>

Example 1:
python simple_changeCurrentMonitor.py -monitor 1

Example 2:
python simple_changeCurrentMonitor.py -room_ip "192.168.0.100" -monitor 1
'''

from websocket import create_connection
import json
import argparse

request_unsecured = '''{
    "method" : "auth",
    "type" : "unsecured"
}'''

def change_monitor(room_ip: str, monitor: int):
    # create connection
    ws = create_connection(f'ws://{room_ip}:8765')
    ws.send(request_unsecured)
    result =  ws.recv()
    print(f'Received: {result}')
    
    # make a command        
    command = {"method": "changeCurrentMonitor", "monitorIndex": monitor}
    # send the command
    ws.send(json.dumps(command))
    # result
    result =  ws.recv()
    print(f'Result: {result}')
    
    # close connection
    ws.close()


if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-room_ip", dest = "room_ip",
                    help = "Room IP", type = str, default="127.0.0.1")
    parser.add_argument("-monitor", dest = "monitor",
                    help = "User ID", type = int)
    args = parser.parse_args()
    room_ip = args.room_ip
    monitor = args.monitor
    # changeCurrentMonitor
    change_monitor(room_ip, monitor)
