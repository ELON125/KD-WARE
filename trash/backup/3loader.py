import asyncio
import datetime
import pymongo, dns
from pymongo import MongoClient
import pyautogui
import socket 
import subprocess
import datetime
import threading
import base64
import time
import win32api, win32con
import os 
import sys
from os import remove
from sys import argv
import cv2
import numpy as np
import keyboard

print('[+]Connecting to server...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('139.162.246.238', 8748)) 
print('[+]Connected to server')

loading_screens = ['characterChoosing','mapChoosing','redText','insuranceScreen','LFGScreen','earlyTermination', 'killList', 'raidStats', 'expGained', 'characterHeal', 'loadingScreen']

try:
  fetched_hwid = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
  fetched_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
except Exception as e:
  pyautogui.alert(f'Error while fetching ip/hwid:\n\n{e}')
  sys.exit()

#On launch send ip and hwid to server if found in db go straight to toggle screen
async def inDb_check():
  s.sendall(f'GetLogin//{fetched_hwid}//{fetched_ip}'.encode('utf-8'))
  first_login = s.recv(2048).decode('utf-8')
  if first_login == 'False':
    main_screen(fetched_ip, fetched_hwid)
  else: await bootup()

async def bootup():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('139.162.246.238', 8748)) 
  print('KD WARE:')
  key = input('[+]Key:\n')

  #Getting vars
  s.sendall(f'GetVars//{fetched_hwid}//{fetched_ip}//{key}'.encode('utf-8'))
  first_login, HwidIpCheck, expiredCheck, keyCheck  = s.recv(2048).decode('utf-8').split("//")
        
  #Checking if key is valid
  if keyCheck != 'Valid':
    pyautogui.alert('Invalid key')
    sys.exit()

  #Checking ip and hwid
  if HwidIpCheck == 'False':
    pyautogui.alert('Hwid/ip missmatch')
    sys.exit()

    #Checking if expired
  if expiredCheck == 'False':
    pyautogui.alert('Key expired!')
    sys.exit()
  
  click()

def click():
  while True:
    x,y,curMap = get_screen()
    if curMap == 'mapChoosing':
      map_choosing()
    win32api.SetCursorPos((int(x),int(y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,int(x),int(y),0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,int(x),int(y),0,0)
    pyautogui.press('space')
    time.sleep(0.5)

def map_choosing():
    win32api.SetCursorPos((783,446))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,783,446,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,783,446,0,0)

    time.sleep(0.3)

    x,y = 954,939 

    win32api.SetCursorPos((int(x),int(y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,int(x),int(y),0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,int(x),int(y),0,0)

    click()    

def main_screen(fetched_ip,fetched_hwid):
  os.system('cls')
  current_screen = 'main_screen'
  
	#Printing main menu
  print('KD WARE:')
  print(f'Ip: {fetched_ip}')
  print(f'HWID: {fetched_hwid}')
  input('[+]Toggle')
  print('[+]Starting bot')
  click()

def get_screen():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('139.162.246.238', 8748)) 

  now = datetime.datetime.now()
      
  img = pyautogui.screenshot('template.jpeg',region=(800, 52, 300, 30))

  template = cv2.imread('template.jpeg',0)
            
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
  curMap, x, y = s.recv(2048).decode('utf-8').split("//")

  return x,y, curMap

keyboard.on_press_key("p", lambda _:os._exit(0))
asyncio.run(inDb_check())