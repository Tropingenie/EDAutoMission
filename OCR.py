# OCR.py
# By Pon Pon
# Purpose: Place to store generic OCR functions for use in Ody and Horiz
# implementations of the script

import logging
import os

import pyautogui
import pytesseract
import numpy as np
from PIL import Image

def parse_selected_mission(selected_mission_sample):
    """
    Locates the selected mission on the board, and runs it through OCR.

    :return: Dump of all the text detected in the image
    :raises: Probably will raise an error if the image is not found
    """
    # Locate the mission that is selected and take a screenshot of it.
    # Confidence is low so as to catch all missions.
    selected = pyautogui.locateOnScreen(selected_mission_sample,
                                        confidence=0.4)
    pyautogui.screenshot("temp_screenshot.png", region=selected)

    # Run the screenshot through OCR and save it to a variable
    text = pytesseract.image_to_string(
        np.array(Image.open("temp_screenshot.png"))
        )
    os.remove("temp_screenshot.png")  # Delete the temp file

    logging.debug(text)
    return text