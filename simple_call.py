# coding=utf8
'''
Created on 22.09.2020

@author: zobov
'''

from websocket import create_connection
import json

request_by_auth = '''{
    "method" : "auth",
    "type" : "password",
    "login" : "admin",
    "password" : "admin"
}'''

request_unsecured = '''{
    "method" : "auth",
    "type" : "unsecured"
}'''

def simple_call(peerId: str):
    # create connection
    ws = create_connection("ws://10.110.14.168:8765")
    print("Sending...")
    ws.send(request_unsecured)
    print("Sent")
    
    print("Receiving...")
    result =  ws.recv()
    print("Received '%s'" % result)
    
    # make a command        
    command = {"method": "call", "peerId": peerId}
    # send the command
    ws.send(json.dumps(command))
    # result
    result =  ws.recv()
    print("Result: '%s'" % result)
    
    # close connection
    ws.close()


if __name__ =='__main__':
    simple_call("azobov@team.trueconf.com")
