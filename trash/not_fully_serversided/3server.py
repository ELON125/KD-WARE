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

#-Added a check if the requesting ip is in the database so noone missuses
#-Added key+name when request is send to server 

#Working on
#-Add so if new ip/hwid is logged in with append to list and upload to server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('139.162.246.238', 8748))
s.listen(5)
print(f'[+]Server online: 139.162.246.238:8748, Ver 1.0')

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
    clientsocket, address = s.accept()
    print(address)
    
    message = clientsocket.recv(2084).decode('utf-8')
    print(f'[+]Recieved Message from {address}')

    now = datetime.datetime.now()

    print(message)
    def checker():
      if 'UpdateCheck' in message:
        cmd, clientVer = message.split("//")
        for dbFind in elonware_db.find({"serverVars"}):
            serverVer = dbFind["version"]
        if clientVer != serverVer:clientsocket.send('Update'.encode('utf-8'))
        else:clientsocket.send('Newest version installed'.encode('utf-8'))

      if 'GetLogin' in message:
        cmd, fetched_hwid, fetched_ip, curVer = message.split("//")
        if elonware_db.count_documents({"hwid": f"{fetched_hwid}"}) > 0:
          for dbFind in elonware_db.find({"hwid":fetched_hwid}):
            first_login = dbFind["first_login"]
          clientsocket.send(f'{first_login}'.encode('utf-8'))
        else: clientsocket.send(f'True'.encode('utf-8'))

      if 'GetVars' in message:
          cmd, fetched_hwid, fetched_ip, key = message.split("//")
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

              if str(fetched_ip) == str(ip):
                HwidIpCheck = 'True'
              else: 
                HwidIpCheck = 'True'

              if datetime.datetime.now() > datetime.datetime.strptime(str(expirationDate), "%Y-%m-%d %H:%M:%S.%f"):
                expiredCheck = 'False'
              else: expiredCheck = 'True'
              
              clientsocket.send(f'{first_login}//{HwidIpCheck}//{expiredCheck}//Valid'.encode('utf-8'))
          else:
            clientsocket.send(f'0//0//0//0'.encode('utf-8'))

      if 'UpdateVars_MessageCheck' in message:
        for dbFind in elonware_db.find({"serverVars"}):
            server_message = dbFind["message"]
        cmd, key, version, curTime = message.split('//')
        elonware_db.update_one(
          {"key": f"{key}"},
          {"$set":{"current_version":f"{version}", "latest_login":f"{curTime}"}}
        )
        clientsocket.send(f'{server_message}//Updated'.encode('utf-8'))
    checker()