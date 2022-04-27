# tab_to.py
# By Pon Pon
# Class to tab to a specific window based on a regex input. Based on code from:
# https://stackoverflow.com/questions/2090464/python-window-activation

from re import match
import logging

import win32gui

class tab_to:
    """Class that behaves as a function; will attempt to tab to the window matching the regex given"""

    def __init__ (self, wildcard):
        """Constructor"""
        self._handle = None
        self._find_window_wildcard(wildcard)
        self._set_foreground()

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        window_text = str(win32gui.GetWindowText(hwnd))
        if window_text:
            logging.debug("Checking window: {}".format(window_text))
        if match(wildcard, window_text) is not None:
            self._handle = hwnd

    def _find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def _set_foreground(self):
        """put the window in the foreground"""
        logging.debug("Alt-tabbing to {}".format(win32gui.GetWindowText(self._handle)))
        win32gui.SetForegroundWindow(self._handle)


# Debug only
if __name__ == "__main__":
    tab_to("Elite.+Dangerous.+CLIENT")