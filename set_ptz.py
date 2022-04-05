# coding=utf8
'''
Created on 05.03.2021

@author: zobov
'''

import argparse
import tcroom
import time

def main(room_ip: str, pin: str):
    room = tcroom.make_connection(room_ip=room_ip, pin=pin, debug_mode=True)
    
    time.sleep(2)
    room.ptzRight()
    time.sleep(10)
    room.ptzDown()
    time.sleep(10)
    
    del room

if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-room_ip", dest = "room_ip", required=True,
                    help = "Room IP", type = str)
    parser.add_argument("-pin", dest = "pin", required=True,
                    help = "PIN auth", type = str)
    args = parser.parse_args()
    room_ip = args.room_ip
    pin = args.pin
    # call
    main(room_ip, pin)
