# odyssey.py
# By Pon Pon
# Low level implementation of main script functionalities for Odyssey

from time import sleep

from pydirectinput import press
from pyautogui import pixelMatchesColor
from pyautogui import size as screen_size

from helper_functions import screenHeight, screenWidth

def open_missions_board():
    press('space', presses=2, interval=0.3)
    sleep(5)  # Delay to account for load time

    # Change filter to transport
    press('d', presses=2, interval=0.3)
    press('space', interval=0.3)
    sleep(5)  # Delay to account for load time

def at_bottom():
    # TODO: Find a way to make this cockpit colour agnostic
    return pixelMatchesColor(int(screenWidth/5.8986), int(screenHeight/1.1268), (255, 111, 0))

def ocr_mission():
    # TODO: Implement this using relative screen space
    return ""

def accept_mission():
    press('space', presses=2, interval=0.3)

def next_mission():
    press('s')

def return_to_starport():
    press('backspace', presses=2, interval=0.3)