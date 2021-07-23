import cv2
import numpy as np
import threading 
import base64
import datetime
import time
import zmq

print('[+]Server loading up...')
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5421064")
print('[+]Server online')

loading_screens = ['mainMenu','characterChoosing','mapChoosing','redText','insuranceScreen','LFGScreen','earlyTermination', 'killList', 'raidStats', 'expGained', 'characterHeal']

while True:
  
  #Saving picture
  
  message = socket.recv()
  
  print('[+]Recieved Message')
  now = datetime.datetime.now()
  
  template = open("template.jpeg", 'wb')
  ba = bytearray(base64.b64decode(message))
  template.write(ba)
  template.close()
  
  
  #Maybe run in a sepperate thread?
  
  def checker():
    
    # Read the template
      template = cv2.imread('template.jpeg',0)
      
    # Store width and height of template in w and h
      w, h = template.shape[::-1]
    
      for x in loading_screens:
        img_rgb = cv2.imread(f'pictures/{x}.jpeg')
        
        # Convert it to grayscale
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        
        # Perform match operations.
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        
        # Specify a threshold
        threshold = 0.9
        
        # Store the coordinates of matched area in a numpy array
        loc = np.where( res >= threshold)
        
        if str(loc) != "(array([], dtype=int64), array([], dtype=int64))":
          socket.send_string(x)
          return
        
      socket.send_string('loadingScreen')
      print(datetime.datetime.now() - now)
    
  
  checker()