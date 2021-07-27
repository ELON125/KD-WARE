import asyncio
import datetime
import pymongo, dns
from pymongo import MongoClient
import socket 
import subprocess
import datetime
import threading
import base64
import time
import os 
import sys
from os import remove
import cv2
import numpy as np

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('139.162.246.238', 8749))
s.listen(5)
print('[+]Server online: {}, Ver 3.2'.format('139.162.246.238'))

dbClient = MongoClient(
    "mongodb+srv://D1P:D1P9812@hokuspokusdb.gehgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = dbClient["ElonWare"]
elonware_db = db["EW-Logins"]

#Next button
nextButton_x, nextButton_y = 954,939
 
#Main screen
nextButton1_x, nextButton1_y = 956,615

#Early termination 
nextButton2_x, nextButton2_y = 950,975

loading_screens = ['characterChoosing','mapChoosing','redText','insuranceScreen','LFGScreen','earlyTermination', 'killList', 'raidStats', 'expGained', 'characterHeal']

while True:
    def checker():
      decoded_message = message.decode('utf-8')
      if 'GetLogin' in decoded_message:
        cmd, fetched_hwid, fetched_ip = decoded_message.split("//")
        if elonware_db.count_documents({"hwid": f"{fetched_hwid}"}) > 0:
          for dbFind in elonware_db.find({"hwid":fetched_hwid}):
            first_login = dbFind["first_login"]
          clientsocket.send(f'{first_login}'.encode('utf-8'))
        else: clientsocket.send(f'True'.encode('utf-8'))


      if 'GetVars' in decoded_message:
          cmd, fetched_hwid, fetched_ip, key = decoded_message.split("//")
          if elonware_db.count_documents({"key": f"{key}"}) > 0:
              for dbFind in elonware_db.find({"key":key}):
                  expirationDate = (dbFind["expirationDate"])
                  first_login = dbFind["first_login"]
                  hwid = dbFind['hwid']
                  ip = dbFind['ip']

              if first_login == 'True':
                elonware_db.update_one(
                  {"key": f"{key}"},
                  {"$set":{"hwid":f"{fetched_hwid}", "ip":f"{fetched_ip}","first_login":"False"}}
                )

              if str(fetched_ip) == str(ip) and str(fetched_hwid) == str(hwid):
                  HwidIpCheck = 'True'
              else: 
                HwidIpCheck = 'True'

              if datetime.datetime.now() > datetime.datetime.strptime(str(expirationDate), "%Y-%m-%d %H:%M:%S.%f"):
                  expiredCheck = 'False'
              else: expiredCheck = 'True'
              
              clientsocket.send(f'{first_login}//{HwidIpCheck}//{expiredCheck}//Valid'.encode('utf-8'))
          else:
            clientsocket.send(f'0//0//0//0'.encode('utf-8'))

    def get_screen():
        now = datetime.datetime.now()
        my_file = open("template1.jpeg", 'wb')
        my_file.write(bytes(message))
        my_file.close()
          
        template = cv2.imread("template1.jpeg",0)

        w, h = template.shape[::-1]
          
        for x in loading_screens:
          img_rgb = cv2.imread(f"pictures/{x}.jpeg")

          img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
              
          res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
              
          threshold = 0.7
              
          loc = np.where( res >= threshold)
          if str(loc) != "(array([], dtype=int64), array([], dtype=int64))":
            print(datetime.datetime.now() - now)
            if x == 'loadingScreen':
              clientsocket.send(f'loadingScreen//{nextButton1_x}//{nextButton1_y}'.encode('utf-8'))

            elif x == 'mapChoosing':
              clientsocket.send(f'mapChoosing//0//0'.encode('utf-8'))
            
            elif x in loading_screens: 
              clientsocket.send(f'{x}//{nextButton_x}//{nextButton_y}'.encode('utf-8'))
                
            elif x == 'earlyTermination':
              clientsocket.send(f'earlyTermination//{nextButton2_x}//{nextButton2_y}'.encode('utf-8'))
            
            else:
                clientsocket.send(f'loadingScreen//{nextButton1_x}//{nextButton1_y}'.encode('utf-8'))
        clientsocket.send(f'loadingScreen//{nextButton1_x}//{nextButton1_y}'.encode('utf-8'))
        print(datetime.datetime.now() - now)

    clientsocket, address = s.accept()
    message = clientsocket.recv(40960000)


    print(f'[+]Recieved Message from {address}')
    print(message)

    try:
      message.decode('utf-8')
      checker()
    except:
      message = clientsocket.recv(40960000)
      data = bytearray(message)
      print(message.endswith(b'\xff\xd9'))
      while message.endswith(b'\xff\xd9') != True:
        message = clientsocket.recv(40960000)
        data.extend(message)
      get_screen()
