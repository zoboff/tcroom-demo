from PIL import Image, UnidentifiedImageError
from pyzbar.pyzbar import decode
import time
import tcroom

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


if __name__ =='__main__':
    room_ip = input('Enter TrueConf Room IP address: ')
    pin = input('Enter PIN: ')
    
    room = None
    try:
        room = tcroom.make_connection(room_ip, pin)
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
