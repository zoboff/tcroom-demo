# coding=utf8
'''''
@author: zobov
'''
import tcroom
import time
import asyncio

ROOM_IP = '127.0.0.1'
PIN = '123'

async def on_event(tcroom, name, data):    
    if name == "videoMatrixChanged":
        # when there are two participants
        if len(data["participants"]) == 2:
            # show the second participant on the other monitor
            peerId = data["participants"][1]["peerId"] # second participant 
            monitor = 1 # monitor index
            tcroom.moveVideoSlotToMonitor(peerId, monitor)
    await asyncio.sleep(0.1)

def main():
    room = tcroom.make_connection(room_ip = ROOM_IP, pin = PIN, cb_OnEvent = on_event)

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