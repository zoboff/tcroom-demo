# coding=utf8
'''''
@author: zobov
'''
import tcroom
import time
import asyncio

mx = '''{
  "method": "event",
  "event": "videoMatrixChanged",
  "matrixType": 7,
  "mainWindowWidth": 1920,
  "mainWindowHeight": 1080,
  "participants": [
    {
      "peerId": "#self:0",
      "peerDn": "TrueConf Kiosk",
      "left": 1,
      "top": 179,
      "width": 639,
      "height": 360
    },
    {
      "peerId": "#emptySlot:1",
      "peerDn": "",
      "left": 640,
      "top": 179,
      "width": 639,
      "height": 360
    },
    {
      "peerId": "#emptySlot:2",
      "peerDn": "",
      "left": 1278,
      "top": 179,
      "width": 639,
      "height": 360
    },
    {
      "peerId": "#emptySlot:3",
      "peerDn": "",
      "left": 1,
      "top": 539,
      "width": 639,
      "height": 360
    },
    {
      "peerId": "#emptySlot:4",
      "peerDn": "",
      "left": 640,
      "top": 539,
      "width": 639,
      "height": 360
    },
    {
      "peerId": "#contentSharing:contentInCustomMatrix",
      "peerDn": "",
      "left": 1278,
      "top": 539,
      "width": 639,
      "height": 360
    }
  ],
  "externVideoSlots": [],
  "hiddenVideoSlots": [
    {
      "callId": "#self:0"
    },
    {
      "callId": "#emptySlot:1"
    },
    {
      "callId": "#emptySlot:2"
    },
    {
      "callId": "#emptySlot:3"
    },
    {
      "callId": "#contentSharing:contentInCustomMatrix"
    },
    {
      "callId": "#emptySlot:4"
    }
  ]
}

'''

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