from PIL import Image, ImageGrab
from matplotlib.pyplot import pause
import numpy as np
import cv2
import pyautogui
import pydirectinput
import time

total = 0

#check for edhm as it might mess it up. i think the keybind to disable it is shift+F1 but i don't use it in ody
#todo

#run at the top of every ten mins to reduce errors
#todo

#select missions
pydirectinput.press('space')
pydirectinput.press('space')
time.sleep(2)

pyautogui.click(x=1090, y=475) #changes filter to transport (only works in 1920x1080)

time.sleep(5)
#main mission checking loop
x = 0
while x != 1:
    try:
        pyautogui.click('neededimages/bertselectedO.png')         #checks if image can be found on screen
        time.sleep(1)
        pyautogui.click('neededimages/acceptbuttonO.png')
        total = total + 1
        print(total + "missions so far")
    except:
        print('none found, moving on')

    print('moving down')
    pydirectinput.press('s')

    #tell if bottom has been reached 
    if pyautogui.pixelMatchesColor(1306, 910, (168, 73, 0)):  #this will only work on 1920x1080 displays so that must be fixed
        try:
            pyautogui.click('neededimages/bertselectedO.png')         #check one last time
            time.sleep(1)
            pyautogui.click(x=1434, y=882)  #also only works in 1920x1080
        except:
            print('none found, moving on')
            x = 1

#exit to refresh
pydirectinput.press('backspace')
pydirectinput.press('backspace')