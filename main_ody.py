# main_ody.py
# by ImpeccablePenguin, Pon Pon
# Purpose: Run the main auto mission selection functionality in E:D Odyssey


from ast import parse
import time
import os
import logging

import schedule
import pyautogui
import pydirectinput
import numpy as np
import cv2
from PIL import Image
# from matplotlib.pyplot import pause
import pytesseract

import helper_functions


# Find tesseract
# TODO: Pull this out into user settings so users/devs can set the path easily
tesseract_path = None
potential_paths = [r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe',
                   r"P:\\Tesseract-OCR\\tesseract.exe"]
for _path in potential_paths:
    if os.path.isfile(tesseract_path):
        tesseract_path = _path
if tesseract_path is None:
    logging.error("No valid tesseract.exe was found")

pytesseract.pytesseract.tesseract_cmd = tesseract_path

# TODO: Intelligently select this based on screen resolution
selected_mission_sample = r"neededimages\\orange2.png"

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

        pydirectinput.press('s')

        #tell if bottom has been reached 
        if pyautogui.pixelMatchesColor(1306, 910, (168, 73, 0)):  #this will only work on 1920x1080 displays so that must be fixed
            try:
                pyautogui.click('neededimages/bertselectedO.png')         #check one last time
                time.sleep(1)
                pyautogui.press('d') #accepts mission
                pyautogui.press('space')
            except:
                print('none found, moving on')
                x = 1

    #exit to refresh
    pydirectinput.press('backspace')
    pydirectinput.press('backspace')
    print("done")


def checkmissionsOCR():
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
        #select and parse mission
        try:
            missiontext = helper_functions.parse_selected_mission(selected_mission_sample)
            print(missiontext)
            if missiontext.contains("BERTRANDITE"):
                pyautogui.press('space')
                pyautogui.press('d')
                pyautogui.press('space') #accepts mission
            else:
                print("not found")
        except:
            print("failed to parse, moving on")

        pydirectinput.press('s')

        #tell if bottom has been reached 
        if pyautogui.pixelMatchesColor(1306, 910, (168, 73, 0)):  #this will only work on 1920x1080 displays so that must be fixed
            try:
                missiontext = helper_functions.parse_selected_mission(selected_mission_sample)
                print(missiontext)
                if missiontext.contains("BERTRANDITE"):
                    pyautogui.press('space')
                    pyautogui.press('d')
                    pyautogui.press('space') #accepts mission
                else:
                    print("not found")
            except:
                print("failed to parse, moving on")
                x = 1
    #exit to refresh
    pydirectinput.press('backspace')
    pydirectinput.press('backspace')
    print("done")

def main():
    schedule.every(10).minutes.do(checkmissions) #Run every 10 mins (maybe change to do top of the 10 mins so it doesn't break during a flip)
    # schedule.every(10).minutes.do(checkmissionsOCR) #Unfinished OCR version. kinda works
    schedule.run_all() #start now


if(__name__ == "__main__"):
    logging.basicConfig(level=logging.DEBUG)
    main()
    # parse_selected_mission() # debug
