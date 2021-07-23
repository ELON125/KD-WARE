import zmq
import base64
import pyautogui
import threading
import datetime


context = zmq.Context()

print("[+]Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5421064")
print("[+]Connected to server")


def get_screen():
  
    #Writing down current time
    now = datetime.datetime.now()
    
    #Taking screenshot // Insert area 
    img = pyautogui.screenshot('template.jpeg',region=(830, 50, 250, 25))
    img = open("template.jpeg", 'rb')

    #Sending picture to server
    bytes = bytearray(img.read())
    strng = base64.b64encode(bytes)
    socket.send(strng)
    img.close()
    
    reply = socket.recv()
    current_screen = reply
    print(current_screen) 
    
    #Checking how long it took
    print(datetime.datetime.now() - now)
    
x = threading.Thread(target=get_screen)
x.start()