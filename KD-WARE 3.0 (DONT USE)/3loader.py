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
import keyboard
import os 
import sys
from os import remove
from sys import argv
import cv2
import numpy as np

print('[+]Connecting to server...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('139.162.246.238', 8748)) 
print('[+]Connected to server')

os.system('cls')
loading_screens = ['characterChoosing','mapChoosing','redText','insuranceScreen','LFGScreen','earlyTermination', 'killList', 'raidStats', 'expGained', 'characterHeal', 'loadingScreen']

try:
  fetched_hwid = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
  fetched_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
except Exception as e:
  pyautogui.alert(f'Error while fetching ip/hwid:\n\n{e}')
  sys.exit()

#On launch send ip and hwid to server if found in db go straight to toggle screen

async def bootup():
    print('KD WARE:')
    key = input('[+]Key:\n')

    #Getting vars
    s.send(f'GetVars //{fetched_hwid}//{fetched_ip}//{key}'.encode('utf-8'))
    first_login, HwidIpCheck, expiredCheck, keyCheck  = s.recv(2048).decode('utf-8').split("//")

    if first_login != 'True':
      await main_screen(fetched_ip,fetched_hwid)
        
    #Checking if key is valid
    if keyCheck != 'Valid':
        pyautogui.alert('Invalid key')
        sys.exit()

    #Checking ip and hwid
    if HwidIpCheck == 'None':
        pyautogui.alert('Hwid/ip missmatch')
        sys.exit()

    #Checking if expired
    if expiredCheck == 'True':
        pyautogui.alert('Key expired!')
        sys.exit()

def click(x,y):
    win32api.SetCursorPos((int(x),int(y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,int(x),int(y),0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,int(x),int(y),0,0)
    pyautogui.press('space')
    time.sleep(0.3)
    get_screen()

def map_choosing():
    win32api.SetCursorPos((783,446))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,783,446,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,783,446,0,0)

    time.sleep(0.3)

    x,y = 954,939 
    click(x,y)    

async def main_screen(fetched_ip,fetched_hwid):
  os.system('cls')
  current_screen = 'main_screen'
  
	#Printing main menu
  print('KD WARE:')
  print(f'Ip: {fetched_ip}')
  print(f'HWID: {fetched_hwid}')
  input('[+]Toggle')
  print('[+]Starting bot')
  get_screen()

def get_screen():
        
    for x in loading_screens:
    # Perform match operations.
        if x == 'loadingScreen':
            print('Sending')
            s.send('pic//loadingScreen'.encode('utf-8'))
            break

        if pyautogui.locate(f'pictures/{x}.jpeg', 'template.jpeg', grayscale=False, confidence=0.8) != None:
            print('Sending')
            s.send(f"pic//{x}".encode('utf-8'))
            break
        else:pass
                
    curMap, x, y = s.recv(2048).split("//")

    print(datetime.datetime.now() - now)

    if curMap == 'mapChoosing':map_choosing()
    else:click(x, y)

keyboard.on_press_key("p", lambda _:os._exit(0))
asyncio.run(bootup())