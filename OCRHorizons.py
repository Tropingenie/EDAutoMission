from PIL import Image, ImageGrab
import numpy as np
import cv2
import pyautogui
import os
from xdo import Xdo #Only for linux, windows may require a different package
import pytesseract
import logging
import time

xdo = Xdo()
log = logging.getLogger("__name__")
logging.basicConfig(level=os.environ.get("LOGLEVEL", "NOTSET"))


def parse_selected_mission():
    """
    Locates the selected mission on the board, and runs it through OCR.

    :return: Dump of all the text detected in the image
    :raises: Probably will raise an error if the image is not found
    """
    # Locate the mission that is selected and take a screenshot of it.
    # Confidence is low so as to catch all missions.
    selected = pyautogui.locateOnScreen("neededimages/mission.png",confidence=0.4)
    im = pyautogui.screenshot("temp_screenshot.png", region=selected)
    im1 = Image.open("comp_shot.png")
    im2 = Image.open("temp_screenshot.png")
    
    if list(im1.getdata()) == list(im2.getdata()):
        break  
    
    # Run the screenshot through OCR and save it to a variable
    text = pytesseract.image_to_string(np.array(Image.open("temp_screenshot.png")))
    im.save("comp_shot.png")
    os.remove("temp_screenshot.png")# Delete the temp file

    logging.debug(text)
    logging.debug(selected)
    pyautogui.press("up")
    return text

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
        print("done") 
    if faction == "rook":
        pyautogui.press("left", presses=3 ,interval=0.3)
        pyautogui.press("down", presses=8 ,interval=0.3)
        pyautogui.press("up", presses=5, interval=0.5)
        pyautogui.press("down", presses=1, interval=0.5)   
        pyautogui.press("right")
        logging.debug("Set faction to Rook Platoon")
        
    if faction == "gus fring":
        pyautogui.press("left", presses=3 ,interval=0.3)
        pyautogui.press("down", presses=8 ,interval=0.3)
        pyautogui.press("up", presses=5, interval=0.5)
        pyautogui.press("down", presses=2, interval=0.5)   
        pyautogui.press("right")
        logging.debug("Set faction to Bureau of Apotanites Flag")
    if faction == "coop":
        pyautogui.press("left", presses=3 ,interval=0.3)
        pyautogui.press("down", presses=8 ,interval=0.3)
        pyautogui.press("up", presses=5, interval=0.5)
        pyautogui.press("down", presses=3, interval=0.5)   
        pyautogui.press("right")
        
    else:
        logging.debug("No faction chosen")
        

#win_id = xdo.search_windows(winname="EliteDangerous6")
time.sleep(10) 
#print(parse_selected_mission())
setup(1,"rook")
print(time.asctime() + " Mission Set")