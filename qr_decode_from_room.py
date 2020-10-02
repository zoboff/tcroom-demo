from PIL import Image, UnidentifiedImageError
from pyzbar.pyzbar import decode
import requests
import os, time
import tcroom
from asyncio.tasks import sleep

URL_PICTURE = "http://{}:8766/frames/?peerId=%23self%3A0&token={}"
OUT_FILE = "tmp_picture_from_room.jpg"

'''
{
  "actions": [
    {
      "action": "connect",
      "server": "team.trueconf.com",
      "peerId": "125000@trueconf.com",
      "password": "90127630279365128736512897635412983745610"
    },
    {
      "action": "call",
      "peerId": "azobov@team.trueconf.com"
    }
  ]
}
'''

def decode_file(file_name: str):
    data = decode(Image.open(file_name))
    if data:
        print('type: {}; data: {}.'.format(data[0].type, data[0].data.decode("utf-8")))


def load_picture_from_room(room_ip: str, tokenForHttpServer: str) -> bool:
    url = URL_PICTURE.format(room_ip, tokenForHttpServer)
    with open(os.path.join(OUT_FILE), 'wb') as out_stream:
        req = requests.get(url, stream=True)
        for chunk in req.iter_content(10240):
            out_stream.write(chunk)
    
    return OUT_FILE


if __name__ =='__main__':
    room_ip = input('Enter IP for TrueConf Room: ')
    pin = input('Enter PIN: ')
    
    room = tcroom.Room(debug_mode=True)
    try:
        room.create_connection(room_ip, pin)
        
        # wait for connection
        while not room.isConnected():
            pass
    except Exception as e:
        print(e)

    if room.isConnected():
        try:
            while True:
                file_name = load_picture_from_room(room_ip, room.getTokenForHttpServer())
    
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
    
        if room.isConnected():
            room.getLogin() # like an empty command
            room.close_connection()
    # ===============================================

    del room
