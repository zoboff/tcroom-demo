# coding=utf8
'''''
@author: zobov
'''
import tcroom
import time
import asyncio
from asyncio.coroutines import _is_debug_mode
import threading
from operator import itemgetter
from urllib3.exceptions import ConnectionError

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
                    # list of participants
                    participants = data["participants"]
                    # Sorted by display name
                    participants = sorted(participants, key=itemgetter('peerDn'))
                    # Make the users list
                    users = [participant["peerId"] for participant in participants if participant["peerId"] != mx[1]]
                    # First remains the first
                    users = [mx[1]] + users
                    # Change matrix
                    room.changeVideoMatrix(mx[0], users)
                    c.notify_all()

                c.release()
        except Exception as e:
            print(f'Error in on_method: {e}')

        await asyncio.sleep(0.1)
    # ==================================================================================

    while True:
        try:
            print("Connecting to TrueConf Room...")
            room = tcroom.make_connection(room_ip = ROOM_IP, pin = PIN, cb_OnEvent = on_event, cb_OnMethod = on_method)
            print("Succesfully connected")
        # try again 
        except tcroom.ConnectToRoomException as e:
            print(f'ConnectToRoomException.')
            print('Try again...')
            time.sleep(1)
            continue # connection again
        #
        except Exception as e:
            print(f'Exception "{e.__class__.__name__}" in {__file__}:{sys._getframe().f_lineno}: {e}')
            break
        #
        except KeyboardInterrupt:
            print('Exit by the Ctrl + c')
            break

        try:
            print("Started!")
            
            # Main loop
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print('Exit by the Ctrl + c')
            break
        except tcroom.RoomException as e:
            print(f'Room error: {e}')
            break
        # Room is off
        except ConnectionError as e:
            print('ConnectionError')
            print('Try again...')
            continue # connection again
        except tcroom.ConnectToRoomException as e:
            print('ConnectToRoomException')
            print('Try again...')
            continue # connection again
        except Exception as e:
            if e.__class__.__name__ == 'ConnectionError':
                print('ConnectionError 2')
                print('Try again...')
                continue # connection again
            else:
                print(f'Unhandled exception: "{e.__class__.__name__}" in {__file__}:{sys._getframe().f_lineno}: {e}')
                continue # connection again

if __name__ =='__main__':
  main()