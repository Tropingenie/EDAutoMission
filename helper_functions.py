# OCR.py
# By Pon Pon
# Purpose: Place to store generic OCR functions for use in Ody and Horiz
# implementations of the script

import logging
import os
from string import ascii_uppercase as ALPHABET
from shutil import copy
from time import sleep

import pyautogui
import pydirectinput
import pytesseract
import numpy as np
from PIL import Image
from psutil import process_iter

screenWidth, screenHeight = pyautogui.size()  # Get the size of the primary monitor.

def module_setup():
    """
    Set up all modules that requires setup.
    """
    # Set logging level to debug
    logging.basicConfig(level=logging.DEBUG)

    # Set up tesseract
    # TODO?: Pull this out into user settings so users/devs can set the path easily
    tesseract_path = None
    potential_paths = [os.path.join("C:\\", "Program Files", "Tesseract-OCR", "tesseract.exe")]
    # Use list comprehension to generate paths of the form
    # "D:/Tesseract-OCR/tesseract.exe" for all possible drive letters
    potential_paths.extend(
                       [os.path.join("{}:\\".format(drive_letter), "Tesseract-OCR", "tesseract.exe") for drive_letter in ALPHABET]
                       )
    logging.debug("Potential paths: {}".format(potential_paths))
    for _path in potential_paths:
        logging.debug("Checking \"{}\" for tesseract.exe".format(_path))
        if os.path.isfile(_path):
            tesseract_path = _path
            break
    if tesseract_path is None:
        raise NotImplementedError("No valid tesseract.exe was found")
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

    return ocr_screen_location(selected)

def ocr_screen_location(selected):
    """
    Perform OCR on the selected region of the main monitor

    :return: Dump of the text detected by OCR
    """
    screen = pyautogui.screenshot(region=selected)

    # Run the screenshot through OCR and save it to a variable
    text = pytesseract.image_to_string(screen)

    logging.debug(text)
    return text

def prep_reference_images():
    """
    Determines the screen resolution of the main monitor and moves the correct
    reference material for that resolution.

    :return: 2 tuple containing (width, height) or None if the resolution is not supported yet
    """
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

def game_running():
    for process in process_iter():
        # logging.debug(process.name())
        if "elitedangerous" in process.name().lower():
            logging.debug(process)
            return True
        elif "edlaunch" in process.name().lower():
            logging.debug(process)

    return False

def game_mode():
    pydirectinput.press('esc', presses=2, interval=0.6)  # Open pause menu
    check_for_odyssey = ocr_screen_location(  # Look at logo in top left
        (int(0.09583*screenWidth),int(0.1361*screenHeight),
         int(0.20625*screenWidth),int(0.10278*screenHeight))
        )
    pydirectinput.press('esc', interval=0.5)  # Close pause menu
    pydirectinput.press('space', interval=0.5)  # Reopen starport services
    sleep(1) # Pause to let starport services load
    return("odyssey" if "odyssey" in check_for_odyssey.lower() else "horizons")

# Running this file as a script is for debug purposes only
if __name__ == "__main__":
    sleep(1)
    module_setup() # Leave this uncommented even in testing
    # prep_reference_images()
    # cleanup_reference_images()
    logging.debug(game_running())
    # ocr_screen_location((0,0,445,324))
