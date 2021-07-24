import asyncio
import datetime
import pymongo, dns
from pymongo import MongoClient
from colorama import Fore, Back, Style
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

ip = 'DESKTOP-CB30I3J'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 8743))


def get_screen():
    while True:
        #Writing down current time
        now = datetime.datetime.now()
        
        #Taking screenshot // Insert area 
        img = pyautogui.screenshot('template1.jpeg',region=(100, 110, 500, 150))
        img = open("template1.jpeg", 'rb')

        #Sending picture to server
        print('Sending picture to server')
        bytes = bytearray(img.read())
        strng = base64.b64encode(bytes)
        s.send(strng)
        img.close()
        
        reply = s.recv(2048)
        current_screen = reply.decode()
        print(current_screen) 
        
        
        #Checking how long it took
        ping = str(datetime.datetime.now() - now)
        print(datetime.datetime.now() - now)
        time.sleep(1)
get_screen()
