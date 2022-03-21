# coding=utf8
'''''
@author: zobov
'''
#
# Sorry, now for Windows only
#
from PIL import Image, UnidentifiedImageError, ImageOps
from pyzbar.pyzbar import decode
import time
import tcroom
import asyncio
import subprocess

async def on_change_state(state: int):
    print(f"New state is {state}")
    await asyncio.sleep(0.1)
    
async def on_incoming_message(fromId, fromDn, msg):    
    print(f"Message - fromId: {fromId}, fromDn: {fromDn}, msg: {msg}")
    await asyncio.sleep(0.1)

OUT_FILE = "tmp_call_by_qr_conference.jpg"

def decode_file(file_name: str):
    
    def decode2(image):
        data = decode(image)
        if not data:
            data = decode(ImageOps.mirror(image)) # mirror
            
        return data
    
    img = Image.open(file_name)
    data = decode2(img)
    if data:
        cmd = data[0].data.decode("utf-8")
        print(f'type: {data[0].type}; data: {cmd}.', )
        cmd = f'"C:/Program Files/TrueConf/Room/TrueConfRoom.exe" trueconf "{cmd}"'
        print(cmd)
        subprocess.Popen(cmd, shell=True)
        time.sleep(3)


if __name__ =='__main__':
    room_ip = input('Enter TrueConf Room IP address: ')
    pin = input('Enter PIN: ')
    
    room = None
    try:
        room = tcroom.make_connection(room_ip=room_ip, pin=pin, debug_mode=True)
    except Exception as e:
        print(e)

    if room:
        try:
            while True:
                file_name = room.save_picture_selfview_to_file(OUT_FILE)
    
                try:
                    decode_file(file_name)
                except UnidentifiedImageError:
                    pass
                except Exception as e:
                    print(e)
        except KeyboardInterrupt:
            print('Exit by the Ctrl + c')
        except tcroom.RoomException:
            print('Room error.')
        except Exception as e:
            print(e)
    
        room.disconnect()

        del room
