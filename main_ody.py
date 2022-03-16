from PIL import Image, ImageGrab
from matplotlib.pyplot import pause
import numpy as np
import cv2
import pyautogui
import pydirectinput
import time
import schedule

total = 0

#check for edhm as it might mess it up. i think the keybind to disable it is shift+F1 but i don't use it in ody
#todo

def checkmissions():
    #select missions
    pydirectinput.press('space')
    pydirectinput.press('space')
    time.sleep(2)

    pydirectinput.press('d') 
    pydirectinput.press('d')
    pydirectinput.press('space') #changes filter to transport
    time.sleep(5) #delay because sometimes it lags

    #main mission checking loop
    x = 0
    while x != 1:
        try:
            pyautogui.click('neededimages/bertselectedO.png')         #checks if image can be found on screen
            time.sleep(1)
            pyautogui.click('neededimages/acceptbuttonO.png')
            total = total + 1
            print("got one")
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
    print("done")
    #needs check to see if missions are full

#run every 10 mins when boards flip
schedule.every(10).minutes.do(checkmissions) #Run every 10 mins (maybe change to do top of the 10 mins so it doesn't break during a flip)
schedule.run_all() #start now

while True:  #main loop
    schedule.run_pending() #scheduler has a pending function
    time.sleep(1) #check every 1 seconds