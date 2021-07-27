print('Starting')
import random
import socket, select
from time import gmtime, strftime
from random import randint
import cv2

image = "tux.png"

print('Somethign wrong')
HOST = socket.gethostname()

print('Shit')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, 8749)
print('Connecting')
sock.connect(server_address)
print('Connected')

# open image
myfile = open(r"C:\Users\micro\Documents\GitHub\KD-WARE\template.jpeg", 'rb')
bytes = myfile.read()

# send image size to server
sock.sendall(bytes)
answer = sock.recv(4096).decode('utf-8')

print (f'answer = {answer}')
