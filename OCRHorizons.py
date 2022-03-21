from PIL import Image, ImageGrab
import numpy as np
import cv2
import pyautogui
import os
from xdo import Xdo #Only for linux, windows may require a different package
import pytesseract
import logging
import time

import helper_functions
xdo = Xdo()
log = logging.getLogger("__name__")
logging.basicConfig(level=os.environ.get("LOGLEVEL", "NOTSET"))



def setup(m, faction):
    if m == 1:
        pyautogui.press("left", presses=2, interval=0.5)
        pyautogui.press("down", presses=5, interval=0.5)#Set mission type to transport, not set already
        pyautogui.press("up", presses=7, interval=0.5)
        pyautogui.press("space", presses=1, interval=0.5)
        pyautogui.press("down", presses=4, interval=0.5)
        pyautogui.press("space", presses=1, interval=0.5)

        pyautogui.press("left", presses=4, interval=0.5)
        pyautogui.press("down", presses=7, interval=0.5)#Reset to origin, which the the back button
        logging.debug("Set mode to transport, returned to origin")

    if faction == "rook":
        pyautogui.press("left", presses=3 ,interval=0.3)
        pyautogui.press("down", presses=8 ,interval=0.3)
        pyautogui.press("up", presses=5, interval=0.5)
        pyautogui.press("down", presses=1, interval=0.5)
        pyautogui.press("space")
        pyautogui.press("right")
        logging.debug("Set faction to Rook Platoon")

    if faction == "gus fring":
        pyautogui.press("left", presses=3 ,interval=0.3)
        pyautogui.press("down", presses=8 ,interval=0.3)
        pyautogui.press("up", presses=5, interval=0.5)
        pyautogui.press("down", presses=2, interval=0.5)
        pyautogui.press("space")
        pyautogui.press("right")
        logging.debug("Set faction to Bureau of Apotanites Flag")

    if faction == "coop":
        pyautogui.press("left", presses=3 ,interval=0.3)
        pyautogui.press("down", presses=8 ,interval=0.3)
        pyautogui.press("up", presses=5, interval=0.5)
        pyautogui.press("down", presses=3, interval=0.5)
        pyautogui.press("space")
        pyautogui.press("right")
        logging.debug("Set faction to Bureau of Apotanites Flag")

    else:
        logging.debug("No faction chosen")


#win_id = xdo.search_windows(winname="EliteDangerous6")
time.sleep(10)
parse_selected_mission()
#setup(1,"rook")
print(time.asctime() + " Mission Set")
