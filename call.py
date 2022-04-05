# coding=utf8
'''''
@author: zobov
'''
import tcroom
import time

ROOM_IP = '10.110.14.53'
PIN = '123'
CALL_USER_ID = 'echotest_ru@trueconf.com'

if __name__ =='__main__':
    room = tcroom.make_connection(room_ip = ROOM_IP, pin = PIN)

    # Just waiting for...
    while not room.isReady():
        time.sleep(0.5)

    # call
    room.call(CALL_USER_ID)
