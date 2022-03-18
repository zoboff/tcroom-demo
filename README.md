# tcroom-demo

Tested on Python 3.8.6.

Install the required modules

```python
pip install pillow
pip install pyzbar
pip install websocket-client==0.58
pip install requests
```
or
```
pip install -r requirements.txt
```

Launch the **TrueConf Room** ver. 3.2 or later.
With a command line like this:

Windows:
```
"C:\Program Files\TrueConf\Room\TrueConfRoom.exe" -pin "123"
```

Linux:
```
$ trueconf-room -pin "123"
```

And voila:
![screanroom](https://user-images.githubusercontent.com/33928051/159033567-a6bd5542-51c4-4e52-8b50-4aa4c93837c4.png)

1. Click on the link on the TrueConf Room main screen.

2. Log in to any TrueConf Server or to [TrueConf Online](https://trueconf.com/) service.

3. Launch a script *call.py*: 
    ```
    python3 call.py 
    ```

Now we calling *echotest@trueconf.com* ...

![screanroom2](https://user-images.githubusercontent.com/33928051/159035296-8ca0b3b7-376c-4f21-ac55-5248abd0d5ff.png)

## call.py

You may change in this script:
```python
...
ROOM_IP = '127.0.0.1'
PIN = '123'
CALL_USER_ID = 'echotest@trueconf.com'
...
```

## qr_decode_from_room.py

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

Enter *IP* and *PIN*

![rsq](https://user-images.githubusercontent.com/33928051/109477082-ad813880-7a88-11eb-8f5d-8c118a8f78b2.png)

#### Bring the picture with the QR-code or Barcode up to the webcam. And you may see something on the console...
