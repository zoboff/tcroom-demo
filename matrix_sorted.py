# coding=utf8
'''''
@author: zobov
'''
import tcroom
import time
import asyncio
from asyncio.coroutines import _is_debug_mode
import threading

ROOM_IP = '127.0.0.1'
PIN = '123'

flag_matrix_changed = None 

def main():
    room = None
    c = threading.Condition()    

    # ==================================================================================
    async def on_event(name, data):
        global flag_matrix_changed

        if name == "videoMatrixChanged":
            users = [participant["peerId"] for participant in data["participants"]]
            if len(users) > 2:
                my_id = room.getMyId()

                # Reaplace SELF_VIEW_SLOT to my ID
                # users - list of all users
                if my_id:
                    for i, user in enumerate(users):
                        if tcroom.SELF_VIEW_SLOT == user:
                           users[i] = my_id
    
                c.acquire()
                # Save matrixType & first user
                flag_matrix_changed = [data["matrixType"], users[0]]                
                c.notify_all()
                c.release()

                # Request for activate
                room.requestConferenceParticipants()

        await asyncio.sleep(0.1)
    # ==================================================================================
    async def on_method(name, data):
        global flag_matrix_changed
        
        try:
            if room.getAppState() == 5 and name == "getConferenceParticipants":
                c.acquire()

                if flag_matrix_changed:
                    mx = flag_matrix_changed
                    flag_matrix_changed = None
                    # Make the users list
                    users = [participant["peerId"] for participant in data["participants"] if participant["peerId"] != mx[1]]
                    users = [mx[1]] + sorted(users)
                    # Change matrix
                    room.changeVideoMatrix(mx[0], users)
                    c.notify_all()

                c.release()
        except Exception as e:
            print(f'Error in on_method: {e}')

        await asyncio.sleep(0.1)
    # ==================================================================================

    room = tcroom.make_connection(room_ip = ROOM_IP, pin = PIN, cb_OnEvent = on_event, cb_OnMethod = on_method)

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