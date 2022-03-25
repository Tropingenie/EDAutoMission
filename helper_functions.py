# OCR.py
# By Pon Pon
# Purpose: Place to store generic OCR functions for use in Ody and Horiz
# implementations of the script

import logging
import os
from shutil import copy

import pyautogui
import pytesseract
import numpy as np
from PIL import Image

def module_setup():
    """
    Set up all modules that requires setup.
    """
    # Set logging level to debug
    logging.basicConfig(level=logging.DEBUG)

    # Set up tesseract
    # TODO: Pull this out into user settings so users/devs can set the path easily
    tesseract_path = None
    potential_paths = [r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe',
                       r"P:\\Tesseract-OCR\\tesseract.exe"]
    for _path in potential_paths:
        if os.path.isfile(tesseract_path):
            tesseract_path = _path
            break
    if tesseract_path is None:
        logging.error("No valid tesseract.exe was found")
    else:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

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

def prep_reference_images():
    """
    Determines the screen resolution of the main monitor and moves the correct
    reference material for that resolution.

    :return: 2 tuple containing (width, height) or None if the resolution is not supported yet
    """
    screenWidth, screenHeight = pyautogui.size()  # Get the size of the primary monitor.
    res_dir = os.path.join("neededimages", "{}p".format(screenHeight))

    if not os.path.isdir(res_dir):
        logging.error("Directory \"{}\" was not found!".format(os.path.abspath(res_dir)))
        return None

    for _file in os.listdir(res_dir):
        copy(
            os.path.join(res_dir, _file),  # Copy will only copy files
            "neededimages"
            )

    return (screenWidth, screenHeight)

def cleanup_reference_images():
    """
    Deletes all files in the ./neededimages folder, leaving folders intact
    """
    for i in os.listdir("neededimages"):
        i = os.path.join("neededimages",i)
        if os.path.isfile(i):
            logging.debug("Attempting to remove \"{}\"".format(i))
            os.remove(i)

# Running this file as a script is for debug purposes only
if __name__ == "__main__":
    module_setup()
    # prep_reference_images()
    # cleanup_reference_images()
