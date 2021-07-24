import socket 
import cv2
import numpy as np
import threading 
import base64
import datetime
import time
import pytesseract

img = cv2.imread('test.jpeg')

text = pytesseract.image_to_string(img, config='--psm 3')
print(text)