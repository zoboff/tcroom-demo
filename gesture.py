import cv2
import numpy as np
import math
# cap = cv2.VideoCapture(0)
     
     
import time
import tcroom

OUT_FILE = "tmp_picture_from_room_2.jpg"

def process_image(filename: str):
    frame = cv2.imread(filename, cv2.IMREAD_COLOR)
    
    try:  #an error comes if it does not find anything in window as it cannot find contour of max area
          #therefore this try error statement
        kernel = np.ones((3,3), np.uint8)
        
        #define region of interest
        roi = frame#[100:300, 100:300]        
        
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # define range of skin color in HSV
        lower_skin = np.array([0,20,70], dtype=np.uint8)
        upper_skin = np.array([20,255,255], dtype=np.uint8)

        #extract skin colur imagw  
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        cv2.imshow('mask 1', mask)

        #extrapolate the hand to fill dark spots within
        mask = cv2.dilate(mask, kernel, iterations = 4)
        
        #blur the image
        mask = cv2.GaussianBlur(mask, (5,5), 100) 

        #show the windows
        cv2.imshow('hsv', hsv)
        cv2.imshow('mask', mask)
        cv2.imshow('frame', frame)
    except:
        pass    
    
    return mask

if __name__ =='__main__':
    room_ip = '127.0.0.1' #input('Enter TrueConf Room IP address: ')
    pin = '123' #input('Enter PIN: ')
    
    try:
        room = tcroom.make_connection(room_ip, pin)
    except Exception as e:
        print(e)

    if room and room.isConnected():
        try:
            while True:
                file_name = room.save_picture_selfview_to_file(OUT_FILE)
    
                try:
                    img = process_image(file_name)
                    cv2.imshow(file_name, img)
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

    cv2.destroyAllWindows()
    del room
         
