import pyautogui
import cv2
test = pyautogui.locateOnScreen('pictures/characterChoosing.jpeg', confidence = 0.5)
while True:
    print(test)

