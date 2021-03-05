# coding=utf8
import paho.mqtt.client as mqtt #import the client1
import time
import tcroom
import sys

ROOM_NAME = "room"
MQTT_BROKER = "10.110.14.168"
MQTT_USER = "mqtt"
MQTT_PASSWORD = "mqtt"

CONNECTION_SUCCESSFULLY = False

def on_message(client, userdata, message):
    global CONNECTION_SUCCESSFULLY
    CONNECTION_SUCCESSFULLY = True

    print("\n  on_message:")
    print(f'    message received: {str(message.payload.decode("utf-8"))}')
    print(f'    message topic: {message.topic}')
    print(f'    message qos: {message.qos}')
    print(f'    message retain flag: {message.retain}\n')

def mqtt_connect(subscribe) -> object:
    try:
        # creating new instance
        client = mqtt.Client(ROOM_NAME)
        client.username_pw_set(username=MQTT_USER, password=MQTT_PASSWORD)
        # attach function to callback
        client.on_message = on_message
        # connecting to broker
        client.connect(host=MQTT_BROKER)
        # start the loop 
        client.loop_start() 
        #Subscribing to topic
        client.subscribe(subscribe)
        # Done        
        return client
    except Exception as e:
        print(f'Exception "{e.__class__.__name__}" in {__file__}:{sys._getframe().f_lineno}: {e}')
        return None

    return None


def main(room_ip: str, pin: str):
    global CONNECTION_SUCCESSFULLY
    mqtt_client = None
    
    topic_appstate = f'room/{ROOM_NAME}/event/appstate'
    topic_motion = f'room/{ROOM_NAME}/event/monitor'

    # ===
    async def on_change_state(state: int):
        status = tcroom.appStateToText(state)
        
        print(f'Publishing message "{status}" to topic {topic_appstate}.')
        mqtt_client.publish(topic_appstate, status)

        await asyncio.sleep(0.1)
    # ===

    room = tcroom.make_connection(room_ip=room_ip, pin=pin, cb_OnChangeState=on_change_state, debug_mode=False)
    
    mqtt_client = mqtt_connect([(topic_appstate, 0), (topic_motion, 0)])
    
    print("Connection to MQTT broker...")
    mqtt_client.publish(topic_appstate, tcroom.appStateToText(room.getAppState()))
    mqtt_client.publish(topic_motion, "on")

    while not CONNECTION_SUCCESSFULLY:
        time.sleep(0.5)
    print("Connection successfully")

    while True:
        try:    
            time.sleep(0.5)
            if not room.isConnected():
                break
        except Exception as e:
            print(f'Exception "{e.__class__.__name__}" in {__file__}:{sys._getframe().f_lineno}: {e}')
        except KeyboardInterrupt:
            print('Exit by the Ctrl + c')
            break

    print("Stop the loop")
    mqtt_client.loop_stop() #stop the loop'''


if __name__ == '__main__':
    main(room_ip="127.0.0.1", pin="123")