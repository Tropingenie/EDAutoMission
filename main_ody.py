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

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

total = 0

#check for edhm as it might mess it up. i think the keybind to disable it is shift+F1 but i don't use it in ody
#todo


def parse_selected_mission():
    """
    Locates the selected mission on the board, and runs it through OCR.

    :return: Dump of all the text detected in the image
    :raises: Probably will raise an error if the image is not found
    """
    # Locate the mission that is selected and take a screenshot of it.
    # Confidence is low so as to catch all missions.
    selected = pyautogui.locateOnScreen("neededimages/orange2.png",
                                        confidence=0.4)
    pyautogui.screenshot("temp_screenshot.png", region=selected)

    # Run the screenshot through OCR and save it to a variable
    text = pytesseract.image_to_string(
        np.array(Image.open("temp_screenshot.png"))
        )
    os.remove("temp_screenshot.png")  # Delete the temp file

    logging.debug(text)
    return text


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
            missiontext = parse_selected_mission()
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
                missiontext = parse_selected_mission()
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
