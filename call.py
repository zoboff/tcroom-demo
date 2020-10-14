# coding=utf8
'''''
@author: zobov
'''
import tcroom
import time

ROOM_IP = '127.0.0.1'
PIN = '123'
CALL_USER_ID = 'azobov@team.trueconf.com'

if __name__ =='__main__':
    room = tcroom.make_connection(ROOM_IP, PIN)
    # call
    room.call(CALL_USER_ID)
    room.disconnect()
    del room
