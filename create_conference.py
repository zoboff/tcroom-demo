# coding=utf8
'''''
@author: zobov
'''
import tcroom
import time

ROOM_IP = '127.0.0.1'
PIN = '123'
PORT = 1515

if __name__ =='__main__':
    room = tcroom.make_connection(room_ip=ROOM_IP, pin=PIN, port=PORT)

    # Just waiting for...
    while not room.isReady():
        time.sleep(0.5)

    # call
    idx = 1
    while True:
        print(f'Starting a new conference... {idx}')
        room.createConferenceSymmetric(title="Test createConferenceSymmetric", autoAccept=True, 
                                       inviteList=["azobov@team.trueconf.com"])
        print("Conference created.")
        time.sleep(5)
        room.hangUp(forAll = True)
        print("Conference ended.")
        time.sleep(5)
        idx += 1

    room.disconnect()
    del room
