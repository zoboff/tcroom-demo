# coding=utf8
'''
Created on 22.09.2020

@author: zobov

Command line:
simple_call.py -room_ip <room IP> -trueconf_id <trueconf id>

Example:
python simple_call.py -room_ip "127.0.0.1" -trueconf_id "john@server.trueconf"
'''

from websocket import create_connection
import json
import argparse

request_unsecured = '''{
    "method" : "auth",
    "type" : "unsecured"
}'''

# calling a user (by trueconf_id) from TrueConf Room (by IP address)
def simple_call(room_ip: str, trueconf_id: str):
    # create connection
    ws = create_connection(f'ws://{room_ip}:8765')
    ws.send(request_unsecured)
    result =  ws.recv()
    print(f'Received: {result}')
    
    # make a command        
    command = {"method": "call", "peerId": trueconf_id}
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
                    help = "Room IP", type = str)
    parser.add_argument("-trueconf_id", dest = "trueconf_id",
                    help = "User ID", type = str)
    args = parser.parse_args()
    room_ip = args.room_ip
    trueconf_id = args.trueconf_id
    # call
    simple_call(room_ip, trueconf_id)
