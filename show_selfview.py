import numpy as np
import cv2
from PIL import Image, UnidentifiedImageError
from pyzbar.pyzbar import decode
import time
import tcroom

OUT_FILE = "tmp_picture_from_room_2.jpg"

TITLE = "Self view"

def process_image(filename: str):
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    # resize
    img = cv2.resize(img, (1920, 1080), cv2.INTER_LINEAR)
    return img

if __name__ =='__main__':
    room_ip = '127.0.0.1' #input('Enter TrueConf Room IP address: ')
    pin = '123' #input('Enter PIN: ')
    
    try:
        room = tcroom.make_connection(room_ip=room_ip, pin=pin, debug_mode=True)
    except Exception as e:
        print(e)

    if room and room.isConnected():
        try:
            cv2.namedWindow(TITLE, cv2.WND_PROP_FULLSCREEN)
            cv2.moveWindow(TITLE, 1921, 0)
            cv2.setWindowProperty(TITLE, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            while True:
                file_name = room.save_picture_selfview_to_file(OUT_FILE)
    
                try:
                    img = process_image(file_name)
                    # show
                    cv2.imshow(TITLE, img)
                    cv2.waitKey(10)
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
    # ===============================================

    del room
