import socket 
import cv2
import numpy as np
import threading 
import base64
import datetime
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('139.162.246.238', 8748))
s.listen()
print(f'[+]Server online: 139.162.246.238:8748, Ver 3.1')

loading_screens = ['characterChoosing','mapChoosing','redText','insuranceScreen','LFGScreen','earlyTermination', 'killList', 'raidStats', 'expGained', 'characterHeal','mainMenu']
loading_screens1 = ['LFGScreen','insuranceScreen','redText','mapChoosing','characterChoosing']

#Check if address is in database otherwise return

while True:
    clientsocket, address = s.accept()
    print(f"[+]Connection established to {address}")
    
    #Reason for the error is because its not recieving all the data
    #Check if smaller pictures are better and you can recieve everything
    message = clientsocket.recv(10000)
    
    print(f'[+]Recieved Message from {address}')
    now = datetime.datetime.now()
    
    template = open("template.jpeg", 'wb')
    ba = bytearray(base64.b64decode(message))
    print(ba)
    template.write(ba)
    template.close()
    
    
    #Maybe run in a sepperate thread?
    
    def checker():
        
        # Read the template
            template = cv2.imread('template.jpeg',0)
            
        # Store width and height of template in w and h
            w, h = template.shape[::-1]
        
            for x in loading_screens1:
                print(x)
                img_rgb = cv2.imread(f'pictures/{x}.jpeg')
                
                # Convert it to grayscale
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                
                # Perform match operations.
                res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                
                # Specify a threshold
                threshold = 0.80
                
                # Store the coordinates of matched area in a numpy array
                loc = np.where( res >= threshold)
                print(loc)
                if str(loc) != "(array([], dtype=int64), array([], dtype=int64))":
                    clientsocket.send(str(x).encode('utf-8'))
                    return
                
            clientsocket.send('loadingScreen'.encode('utf-8'))
            print(datetime.datetime.now() - now)
        
    
    checker()