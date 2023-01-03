# EDAutoMission
Automatically accepts missions of a type
(This is a work in progress so expect bugs)

## Installation
There are two ways to run the program: As a python script, or the built code. The raw python supports both command-line and gui control, while the built .exe only can be run through the gui. 

### For development/testing purposes:
1. Ensure Python 3 is installed
2. Clone the repo
4. [Install Tesseract](https://github.com/tesseract-ocr/tessdoc/blob/main/Installation.md)
    - It is recommended to install to the default path (`C:/Program Files/Tesseract`), however, if installing to a different drive, ensure that you install directly to the drive, i.e. to `D:/Tesseract` (where `D:` is the drive you are installing Tesseract to)
3. Install requirements (`pip install -r requirements.txt`)

### Built GUI Version
1. Download the .exe file from the releases section
4. [Install Tesseract](https://github.com/tesseract-ocr/tessdoc/blob/main/Installation.md)
    - It is recommended to install to the default path (`C:/Program Files/Tesseract`), however, if installing to a different drive, ensure that you install directly to the drive, i.e. to `D:/Tesseract` (where `D:` is the drive you are installing Tesseract to)

## How to use:
1. Dock and click starport services
2. Make sure mission board is selected (see image, below)
3. Go to the GUI or your terminal
4. Run the script (`python main_ody.py` for current features or `python main.py` for experimental branch), or click the go button on the GUI
5. (non-Windows only) Tab back to the game within 5 seconds

To prematurely exit the program:
1. Wait for the script to finish checking missions, if it is doing so
1. Alt tab back to the terminal or GUI
2. Manually interrupt the program (`ctrl-c` on most terminals), or click the exit button

![Screenshot of starting state](https://cdn.discordapp.com/attachments/945223875279601687/957878152657526784/unknown.png)

## Current Features
- Odyssey support through CLI (run as script)
- Automatically checks and accepts missions for Bertrandite, Gold, and Silver every 10 minutes
- 16:9 resolutions supported: 720p, 1080p, 2160p

## Features in Testing
- Consolidate code in `main.py`
- All cockpit colours should work (when running `main.py`)
- All 16:9 resolutions should work (`main.py`)

## Roadmap/Plans
(Subject to change, though if its possible by my knowledge it will be added)
  - Have a GUI and standalone application
    - User input of Tesseract binary file path
    - User selection of Horizons/Odyssey
  - Add configurations for missions of other commodities/types
  - Horizons support (in progress)
  - Extend support to aspect ratios other than 16:9 (in testing)
  - Extend support to cockpit colors other than the default (in testing)
  - Code ruggedization
    - Improve reliability of mse difference detection for exiting mission board
    - Improve reliability and simplicity of internal mission count
    - Remove hard coding of mission names and implement more generic detection
