# tcroom-demo

## qr_decode_from_room.py

Tested on Python 3.8.6.

Install the required modules

```
pip install pillow
pip install pyzbar
pip install websocket-client
pip install requests
```

Launch the TrueConf Room ver. 3.2 or later.
With a command line like this:

```
"C:\Program Files\TrueConf\Room\TrueConfRoom.exe" -pin 123
```

Run script:

```
c:\this_project>python qr_decode_from_room.py 

Enter TrueConf Room IP address: 127.0.0.1
Enter PIN: 123
```
You can terminate that script by pressing Ctrl+C

### How to use "qr_decode_from_room.py"

#### Launch TrueConf Room application with *pin* param

Command line example: 
```
"C:\Program Files\TrueConf\Room\TrueConfRoom.exe" -pin "123"
```

#### Set "Enhance quality of the video displayed in the control panel"

![evq](https://user-images.githubusercontent.com/33928051/109476259-ba515c80-7a87-11eb-89e6-7e51622a783f.png)

#### Run *qr_decode_from_room.py* script

#### Bring the picture with the QR-code or Barcode up to the webcam. And you may see something on the console...
