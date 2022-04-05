# coding=utf8
'''''
@author: zobov
'''

'''
    For TrueConf Room v. 4.1.* or later
'''
import tcroom
import time
import asyncio

async def on_change_state(state: int):
    print(f"New state is {state}")
    await asyncio.sleep(0.1)
    
async def on_incoming_message(fromId, fromDn, msg):    
    print(f"Message - fromId: {fromId}, fromDn: {fromDn}, msg: {msg}")
    await asyncio.sleep(0.1)

async def on_method(method, response):    
    print(f"Method: {method}")
    print(f"  Response: {response}")
    await asyncio.sleep(0.1)

async def on_event(event, response):    
    print(f"Event: {event}")
    print(f"  Response: {response}")
    await asyncio.sleep(0.1)

def main():
    room_ip = input('Enter TrueConf Room IP address: ')
    pin = input('Enter PIN: ')

    room = tcroom.make_connection(pin=pin, room_ip=room_ip, 
                                  cb_OnChangeState=on_change_state, cb_OnIncomingMessage=on_incoming_message, 
                                  cb_OnMethod=on_method, cb_OnEvent=on_event)
    
    time.sleep(1.0)

    command = {"method": "fireMyEvent", "data": "any data"}
    room.send_command_to_room(command)

    try:
        while room.isConnected():
            time.sleep(0.3)
    except KeyboardInterrupt:
        print('Exit by the Ctrl + c')
    except tcroom.RoomException:
        print('Room error.')
    except Exception as e:
        print(e)

    room.disconnect()
    del room    


if __name__ =='__main__':
  main()