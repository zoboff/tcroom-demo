from PIL import Image, UnidentifiedImageError
from pyzbar.pyzbar import decode
import requests
import os, time
import tcroom

#url_picture = "http://127.0.0.1:8766/frames/?peerId=%23self%3A0&token=5*AeeO3oGWlSh21qMR*1632067455*3735443731443646394643413541423839443033413234313442313334443631"
URL_PICTURE = "http://{}:8766/frames/?peerId=%23self%3A0&token={}"
OUT_FILE = "tmp_picture_from_room.jpg"

ROOM_IP = '127.0.0.1'
PIN = '123qwe'

def decode_file(file_name: str):
    data = decode(Image.open(file_name))
    if data:
        print('type: {}; data: {}.'.format(data[0].type, data[0].data.decode("utf-8")))


def load_picture_from_room(tokenForHttpServer: str) -> bool:
    url = URL_PICTURE.format(ROOM_IP, tokenForHttpServer)
    with open(os.path.join(OUT_FILE), 'wb') as out_stream:
        req = requests.get(url, stream=True)
        for chunk in req.iter_content(10240):
            out_stream.write(chunk)


if __name__ =='__main__':
    room = tcroom.Room(debug_mode=True)
    room.create_connection(ROOM_IP, PIN)
    try:
        while True:
            load_picture_from_room(room.getTokenForHttpServer())

            try:
                decode_file(OUT_FILE)
            except UnidentifiedImageError:
                pass
            except Exception as e:
                print(e)
    except KeyboardInterrupt:
        print('Exit by the Ctrl + c')
    except Exception as e:
        print(e)

    room.getLogin() # like an empty command
    room.close_connection()
    del room
