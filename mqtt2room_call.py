import paho.mqtt.client as mqtt #import the client1
import time
from websocket import create_connection
import json

broker_ip = "10.110.14.168"
room_ip = "10.110.15.97"
switch = "zigbee2mqtt/0x00158d000317a95d" #"room/command"

mqtt_username = ""
mqtt_password = ""

call_id = "azobov@team.trueconf.com"

request_unsecured = '''{
    "method" : "auth",
    "type" : "unsecured"
}'''

def simple_call(peerId: str):
    # create connection
    print("Create connection to TrueConf Room: ws://%s:8765" % room_ip)
    ws = create_connection("ws://%s:8765" % room_ip)
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
    
############
def on_message(client, userdata, message):
    print("message received: ", str(message.payload.decode("utf-8")))
    print("message topic: " , message.topic)
    print("message qos: ", message.qos)
    print("message retain flag: ", message.retain)

    dict_rcv = json.loads(message.payload)

    if dict_rcv["action"] == "single":
        simple_call(call_id)

    print("")
########################################

if __name__ =='__main__':
    print("Creating new instance")
    client = mqtt.Client("switch") #create new instance
    client.username_pw_set(username = mqtt_username, password = mqtt_password)
    client.on_message = on_message #attach function to callback
    print("connecting to broker")
    client.connect(host = broker_ip) #connect to broker
    client.loop_start() #start the loop
    print("Subscribing to topic", switch)
    client.subscribe(switch)
    time.sleep(120) # wait
    client.loop_stop() #stop the loop'''
