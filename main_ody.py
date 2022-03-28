# main_ody.py
# by ImpeccablePenguin, Pon Pon
# Purpose: Run the main auto mission selection functionality in E:D Odyssey


# from ast import parse
from lib2to3.pytree import Base
from tabnanny import check
import time
# import os
import logging

import schedule
import pyautogui
import pydirectinput
# import numpy as np
# import cv2
# from PIL import Image
# from matplotlib.pyplot import pause
# import pytesseract

import helper_functions


# Note: This will be configured to the correct resolution image when
# helper_functions.prep_reference_images() is called
selected_mission_sample = r"neededimages\\ody_selected_mission.png"

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
    pydirectinput.press('space', presses=2, interval=0.6)
    time.sleep(2)

    pydirectinput.press('d', presses=2, interval=0.9)
    pydirectinput.press('space', interval=0.6) #changes filter to transport
    time.sleep(5) #delay to account for load time

    #main mission checking loop
    # Exits when the orange scroll bar reaches bottom
    while not pyautogui.pixelMatchesColor(int(screenWidth/5.8986), int(screenHeight/1.1268), (255, 111, 0)):
        #select and parse mission
        try:
            missiontext = helper_functions.parse_selected_mission(selected_mission_sample)
            logging.debug("Detected text: {}".format(missiontext))
            if "BERTRANDITE" in missiontext or "GOLD" in missiontext or "SILVER" in missiontext:
                logging.info("Bread detected.")
                total += 1
                pydirectinput.press('space', presses=2, interval=0.3)  # accepts mission
            else:
                logging.info("Not bread")
        except Exception as e:  # TODO: Figure out what exceptions we expect and catch only those
            logging.info("failed to parse, moving on")
            logging.error(e)

        if total == 20:
            break

        pydirectinput.press('s')

    # TODO: Check the mission board one last time before exiting to scan the last mission

    #exit to refresh
    pydirectinput.press('backspace', presses=2, interval=0.3)
    logging.info("done")

def main():
    schedule.every(10).minutes.do(checkmissions) #Run every 10 mins (maybe change to do top of the 10 mins so it doesn't break during a flip)
    # schedule.every(10).minutes.do(checkmissionsOCR) #Unfinished OCR version. kinda works
    schedule.run_all() #start now


if(__name__ == "__main__"):
    time.sleep(5)  # Give some time for user to alt tab
    helper_functions.module_setup()
    screenWidth, screenHeight = helper_functions.prep_reference_images()
    # main()
    try:
        while True:
            logging.debug("Current minute reading is: {}".format(time.gmtime()[4]))
            # To check every 10 minutes, we look when the clock reads the 5 minute mark
            # e.g. for 1:55, time.gmtime()[4] will be 55, 55+5=60, 60%10 == 0
            if ((time.gmtime()[4] + 5) % 10 == 0):
                logging.info("Checking missions...")
                checkmissionsOCR() # debug
            if total == 20:
                break
            time.sleep(20) # Slows loop rate to thrice per minute
    finally:
        helper_functions.cleanup_reference_images()
    # parse_selected_mission() # debug
