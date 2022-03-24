


# This has not been tested nor does it work





from PIL import Image, ImageGrab
import numpy as np
import cv2
import pyautogui
import pydirectinput

total = 0

#check for edhm

#move into position
#select missions
pydirectinput.press('s')
pydirectinput.press('space')

#change filter to reduce time
pydirectinput.press('a')
for x in range (0,8):
    pydirectinput.press('w')   #since it starts on the bottom, make sure to move past the factions. Hopefully there won't be more than 7(?) or this will fail
    x = x + 1
pydirectinput.press('space')
pydirectinput.press('s')
pydirectinput.press('s')
pydirectinput.press('s')
pydirectinput.press('s')
pydirectinput.press('space')   #changes filter to transport

pydirectinput.press('d') #moves over to first mission
try:
    pyautogui.click('neededimages/bert.png')         #checks if image can be found on screen
    pyautogui.click('neededimages/acceptbuttonh.png')
except:
    print('none found, moving on')


#tell if bottom has been reached 
if pyautogui.pixelMatchesColor(1832, 1010, (168, 73, 0)):
    #move on
    print('temp message')