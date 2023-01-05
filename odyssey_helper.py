# odyssey.py
# By Pon Pon
# Low level implementation of main script functionalities for Odyssey

import logging
from time import sleep

from pydirectinput import press
from pyautogui import screenshot
from numpy import array
from numpy import sum as array_sum

from helper_functions import screenHeight, screenWidth, ocr_screen_location

class OdysseyHelper:
    missions_seen = 0
    back_button_original = None

    @classmethod
    def open_missions_board(cls):
        press('space', presses=2, interval=0.3)
        sleep(5)  # Delay to account for load time

        # Change filter to transport
        press('d', presses=2, interval=0.3)
        press('space', interval=0.3)
        sleep(5)  # Delay to account for load time

    @classmethod
    def at_bottom(cls):
        if cls.back_button_original is None:
            cls.back_button_original = array(screenshot(
                region=(
                    int(screenWidth*235/3840),
                    int(screenHeight*1868/2160),
                    int(screenWidth*666/3840),
                    int(screenHeight*90/2160)
                )
            ))
        back_button_new = array(screenshot(
            region=(
                int(screenWidth*235/3840),
                int(screenHeight*1868/2160),
                int(screenWidth*666/3840),
                int(screenHeight*90/2160)
            )
        ))

        # logging.debug("Original:")
        # logging.debug(cls.back_button_original)
        # logging.debug("New:")
        # logging.debug(back_button_new)

        # Calculate the Mean Squared Error between the two images (i.e. the
        # average error between all the pixels). This looks complicated, but it
        # is just taking the square of the difference divided by the total
        # number of pixels in the arrays.
        # See https://pyimagesearch.com/2014/09/15/python-compare-two-images/
        # for a more in-depth explanation
        mse = array_sum((cls.back_button_original.astype("float") - back_button_new.astype("float")) ** 2)/float(cls.back_button_original.shape[0] * back_button_new.shape[1])
        logging.debug("mse = {}".format(mse))
        return mse > 1

    @classmethod
    def ocr_mission(cls):
        # Odyssey will not scroll the mission board until the first 6 missions have
        # been iterated over. Therefore, we need to specifically look at the
        # coordinates of the first 6 missions before just looking at the coordinates
        # of the bottom most mission

        # Reference screen size (used to determine relative coords)
        myScreenWidth = 3840
        myScreenHeight = 2160
        # Vertical start coordinate of each of the missions (on the reference screen)
        reference_verts = (888, 1040, 1184, 1336, 1481, 1627, 1683)

        # Actual screen size values
        horiz_start = int(screenWidth*235/myScreenWidth)
        selection_width = int(screenWidth*1563/myScreenWidth)
        selection_height = int(screenHeight*127/myScreenHeight)
        mission_coords = [
            (horiz_start, int(screenHeight*vert/myScreenHeight), selection_width, selection_height) for vert in reference_verts
        ]
        if cls.missions_seen < 6:
            return ocr_screen_location(mission_coords[cls.missions_seen])
        else:
            return ocr_screen_location(mission_coords[6])

    @classmethod
    def accept_mission(cls):
        press('space', presses=2, interval=0.3)

    @classmethod
    def next_mission(cls):
        cls.missions_seen += 1
        press('s')

    @classmethod
    def return_to_starport(cls):
        cls.missions_seen = 0
        cls.back_button_original = None  # Reset this to force a new screenshot for every board refresh
        press('backspace', presses=2, interval=0.5)

    @classmethod
    def check_missions_accepted(cls):
        mission_count = None
        # Open mission depot
        press('space', presses=2, interval=0.5)
        sleep(5)  # Delay to account for load time

        mission_depot_text = ocr_screen_location(
            [
                int(2956*screenWidth/3840),
                int(1720*screenHeight/2160),
                int(400*screenWidth/3840),
                int(80*screenWidth/2160)
            ]
        )

        # If the mission depot doesn't exist, then 0 missions
        if "MISSION DEPOT" not in mission_depot_text:
            mission_count = 0

        elif "MISSION DEPOT" in mission_depot_text: # Open mission depot
            press('d', presses=3, interval=0.3)
            press('s', presses=1, interval=0.3)
            press('space', presses=1, interval=0.3)

            mission_count = 0
            while not cls.at_bottom():
                mission_count += 1
                cls.next_mission()

        assert mission_count is not None, "OCR Failure"

        press('backspace', presses=2, interval=0.3) # Return to starport services

        cls.back_button_original = None
        cls.missions_seen = 0

        logging.debug("Detected {} missions".format(mission_count))
        return mission_count

# Run as script for debug only
if __name__ == "__main__":
    import helper_functions
    sleep(5)
    helper_functions.module_setup()
    OdysseyHelper.check_missions_accepted()