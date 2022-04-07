# odyssey.py
# By Pon Pon
# Low level implementation of main script functionalities for Odyssey

from time import sleep
from matplotlib.pyplot import cla

from pydirectinput import press
from pyautogui import pixelMatchesColor

from helper_functions import screenHeight, screenWidth, ocr_screen_location

class OdysseyHelper:
    missions_seen = 0

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
        # TODO: Find a way to make this cockpit colour agnostic
        return pixelMatchesColor(int(screenWidth/5.8986), int(screenHeight/1.1268), (255, 111, 0))

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
        press('backspace', presses=2, interval=0.3)