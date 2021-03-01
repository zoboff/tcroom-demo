from PIL import Image, UnidentifiedImageError, ImageOps
from pyzbar.pyzbar import decode
import time
import tcroom

OUT_FILE = "tmp_picture_from_room.jpg"

def decode_file(file_name: str):
    
    def decode2(image):
        data = decode(image)
        if not data:
            data = decode(ImageOps.mirror(image)) # mirror
            
        return data
    
    img = Image.open(file_name)
    data = decode2(img)
    if data:
        print(f'type: {data[0].type}; data: {data[0].data.decode("utf-8")}.', )


if __name__ =='__main__':
    room_ip = input('Enter TrueConf Room IP address: ')
    pin = input('Enter PIN: ')
    
    room = None
    try:
        room = tcroom.make_connection(room_ip=room_ip, pin=pin)
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
