import tcroom
import time

if __name__ == "__main__":
    #websocket.enableTrace(False)

    room_ip = "127.0.0.1" #input('Enter TrueConf Room IP address: ')
    pin = "123" #input('Enter PIN: ')

    try:
        room = tcroom.make_connection_to_room(room_ip, pin)
    
        room.call("azobov@team.trueconf.com")
    
        while room.isReadyToWork():
            time.sleep(1)

    except KeyboardInterrupt:
        print('Exit by the Ctrl + c')
    except Exception as e:
        print(e)
