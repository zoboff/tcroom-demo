# coding=utf8
'''
Created on 22.09.2020

@author: zobov
'''

from websocket import create_connection
import json
import argparse

request_unsecured = '''{
    "method" : "auth",
    "type" : "unsecured"
}'''

def simple_call(room_ip: str, trueconf_id: str):
    # create connection
    ws = create_connection("ws://%s:8765" % room_ip)
    ws.send(request_unsecured)
    result =  ws.recv()
    print("Received '%s'" % result)
    
    # make a command        
    command = {"method": "call", "peerId": trueconf_id}
    # send the command
    ws.send(json.dumps(command))
    # result
    result =  ws.recv()
    print("Result: '%s'" % result)
    
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
