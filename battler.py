import pyautogui
import time
import cv2 as cv
import numpy as np


class BattleHandler:
    # Settings for the battlehandler
    def __init__(self, update_freq):
        self.active = True
        self.updateFreq = update_freq
        self.wantedButton = "Win Rate"

    async def wait_for_turn(self):
        while True:
            # Take a screenshot of the entire screen
            screen = pyautogui.screenshot()
            # Convert the screenshot to a numpy array
            screen = np.array(screen)
            # Turn the screenshot into a grayscale image
            screen = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)

            # For debugging, show the screenshot
            cv.imshow("Screen", screen)
            cv.waitKey(1)