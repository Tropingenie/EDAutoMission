# ----------------------------------
# 
# 
# 
# 
# This was an early test i made to try and
# use OCR to read the available missions
# 
# could still be usefull
# 
# 
# ----------------------------------

from PIL import Image, ImageGrab
import numpy as np
import cv2
import pyautogui
import pydirectinput

import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

total = 0

#get region of screen function
def screenshot(a, b, c, d):
    return ImageGrab.grab(bbox=(a, b, c, d), include_layered_windows=False, all_screens=False, xdisplay=None)

def processimage(toprocess):        #de-noises image and returns text
    img = np.array(Image.open(toprocess))
    #de-noise image
    norm_img = np.zeros((img.shape[0], img.shape[1]))
    img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
    img = cv2.GaussianBlur(img, (1, 1), 0)
    outputtext = pytesseract.image_to_string(img)
    return outputtext

#loop to check onscreen missions
def checkscreen():
    i = 0
    while i < 1000:
        #get first mission
        mission1 = screenshot(728,638,1332,661) #coords of first mission on list
        text = processimage(mission1)
        if text.contains("BERTRANDITE"): #more options in the future
            pydirectinput.press('space')
            pydirectinput.press('d')
            pydirectinput.press('space')
        else:
            pydirectinput.press('s')
        #get second mission
        mission2 = screenshot(728,727,1332,749) #coords of second mission on list
        text = processimage(mission2)
        if text.contains("BERTRANDITE"): 
            pydirectinput.press('space')
            pydirectinput.press('d')
            pydirectinput.press('space')
        else:
            pydirectinput.press('s')
        #get third mission
        mission2 = screenshot(728,727,1332,749) #coords of third mission on list
        text = processimage(mission2)
        if text.contains("BERTRANDITE"): 
            pydirectinput.press('space')
            pydirectinput.press('d')
            pydirectinput.press('space')
        else:
            pydirectinput.press('s')

            
#select missions
pydirectinput.press('s')
pydirectinput.press('space')

#change filter to reduce time
pydirectinput.press('a')
for x in range (0,10):
    pydirectinput.press('w')   #since it starts on the bottom, make sure to move past the factions. Hopefully there won't be more than 9 or this will fail
    x = x + 1
pydirectinput.press('space')
pydirectinput.press('s')
pydirectinput.press('s')
pydirectinput.press('s')
pydirectinput.press('s')
pydirectinput.press('space')   #changes filter to transport

pydirectinput.press('d') #select first mission

#check if there are any missions
check = screenshot(1057, 730, 1425, 754)
img = np.array(Image.open(check))              #get and de-noise text
norm_img = np.zeros((img.shape[0], img.shape[1]))
img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
img = cv2.GaussianBlur(img, (1, 1), 0)
text = pytesseract.image_to_string(img)
if text.contains("SOME RESULTS ARE BEING FILTERED."):
    pydirectinput.press('s')
    pydirectinput.press('space')
else:
    checkscreen()
#move to next faction and repeat