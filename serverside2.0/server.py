import random
import socket, select
from time import gmtime, strftime
from random import randint
import cv2

imgcounter = 1

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 8749))
print(f'[+]Server online: 139.162.246.238:8748, Ver 3.2')
s.listen(10)

loading_screens = ['characterChoosing','mapChoosing','redText','insuranceScreen','LFGScreen','earlyTermination', 'killList', 'raidStats', 'expGained', 'characterHeal', 'loadingScreen']

while True:
    clientsocket, address = s.accept()
    data = clientsocket.recv(40960000)

    my_file = open(r'C:\Users\micro\Documents\GitHub\KD-WARE\picturesender.py\test.png', 'wb')
    my_file.write(data)

    template = cv2.imread(r'C:\Users\micro\Documents\GitHub\KD-WARE\picturesender.py\test.png',0)
    if template == None:
        print('template is none')

    w, h = template.shape[::-1]
    for x in loading_screens:
        if x == 'loadingScreen':
            s.sendall("pic//loadingScreen".encode('utf-8'))
            break
        img_rgb = cv2.imread(f'pictures/{x}.jpeg')
                    
        # Convert it to grayscale
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                    
        # Perform match operations.
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                    
        # Specify a threshold
        threshold = 0.80
                    
        # Store the coordinates of matched area in a numpy array
        loc = np.where( res >= threshold)
        if str(loc) != "(array([], dtype=int64), array([], dtype=int64))":
            s.sendall(f"pic//{x}".encode('utf-8'))
            break
        else:pass
    print(x)