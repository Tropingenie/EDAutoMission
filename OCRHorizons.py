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
log = logging.getLogger("log")

 os.remove("temp_screenshot.png")#Remember to put it back



def parse_selected_mission():
    """
    Locates the selected mission on the board, and runs it through OCR.

    :return: Dump of all the text detected in the image
    :raises: Probably will raise an error if the image is not found
    """
    # Locate the mission that is selected and take a screenshot of it.
    # Confidence is low so as to catch all missions.
    selected = pyautogui.locateOnScreen("neededimages/mission.png",
                                        confidence=0.1)
    pyautogui.screenshot("temp_screenshot.png", region=selected)

    # Run the screenshot through OCR and save it to a variable
    text = pytesseract.image_to_string(
        np.array(Image.open("temp_screenshot.png"))
        )
      # Delete the temp file

    logging.debug(text)
    return text, selected




win_id = xdo.search_windows(pid = 15347)
print(win_id)
time.sleep(10)
parse_selected_mission()
