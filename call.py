# coding=utf8
'''''
@author: zobov
'''
import tcroom
import time

ROOM_IP = '169.254.22.1'
PIN = '123qwe'
CALL_USER_ID = 'azobov@team.trueconf.com'

if __name__ =='__main__':
    room = tcroom.Room(debug_mode=True)
    room.create_connection(ROOM_IP, PIN)
    # call
    room.call(CALL_USER_ID)
    time.sleep(3)
    room.close_connection()
    del room
