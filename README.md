# EDAutoMission
Automatically accepts missions of a type
(This is a work in progress so expect bugs)

## Installation
Currently, there are no builds available.

For development/testing purposes:
1. Ensure Python 3 is installed
2. Pull repo
4. [Install Tesseract](https://github.com/tesseract-ocr/tessdoc/blob/main/Installation.md)
3. \[PLACEHOLDER FOR USER SETTINGS]: If Tesseract was not installed to the default location (`C:\\Program Files\\Tesseract-OCR\\tesseract.exe`) then modify `helper_functions.setup()` to try the path
3. Install requirements (`pip install -r requirements.txt`)

## How to use:
1. Dock and click starport services
2. Make sure mission board is selected (see image, below)
3. Tab over to your terminal
4. Start program (`python main_ody.py`)
5. Tab back to the game

## Roadmap/Plans
(Subject to change, though if its possible by my knowledge it will be added)
  - Have a GUI and standalone application
  - Add configurations for missions of other commodities/types
  - Horizons support (in progress)
  - Extend support for resolutions other than 1920x1080 (in progress)
