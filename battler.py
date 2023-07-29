import pyautogui
import time
import cv2 as cv
import numpy as np
import os


class BattleHandler:
    # Settings for the battlehandler
    def __init__(self, update_freq, debug: bool = False):
        self.active = True
        self.updateFreq = update_freq
        self.imgPfx = "images/"

        self.abMode = "winrate.png"
        self.start = "start.png"
        self.postBattle = "continue.png"

        self.debug = debug

        # Check that the images exist
        self.check_images()

    def check_images(self):
        if not os.path.isfile(self.imgPfx + self.abMode):
            raise FileNotFoundError("Image not found: " + self.imgPfx + self.abMode)
        if not os.path.isfile(self.imgPfx + self.start):
            raise FileNotFoundError("Image not found: " + self.imgPfx + self.start)
        if not os.path.isfile(self.imgPfx + self.postBattle):
            raise FileNotFoundError("Image not found: " + self.imgPfx + self.postBattle)

    def do_battle(self):
        while True:
            # Take a screenshot of the entire screen
            screen = pyautogui.screenshot()
            # Convert the screenshot to a numpy array
            screen = np.array(screen)
            screen = cv.cvtColor(screen, cv.COLOR_RGB2GRAY)

            # Load the image of the win rate button
            ab_mode = cv.imread(self.imgPfx + self.abMode, 0)

            # Use template matching to find the win rate button
            # Try with different scales of the button: people will have different resolutions
            scales = [0.5, 0.75, 1.0, 1.25, 1.5]

            res = None
            found_scale = None
            for scale in scales:
                resized = cv.resize(ab_mode, (0, 0), fx=scale, fy=scale)
                found_scale = scale
                res = cv.matchTemplate(screen, resized, cv.TM_CCOEFF_NORMED)
                # We only care about the maximum value
                if np.max(res) > 0.6:
                    break

            # Resize the image to the scale we found
            ab_mode = cv.resize(ab_mode, (0, 0), fx=found_scale, fy=found_scale)

            threshold = 0.6
            if np.any(res >= threshold):
                loc = np.where(res >= threshold)
                print(f"Found win rate button! ({np.max(res)}/{threshold})")
                if self.debug:
                    loc = list(zip(*loc[::-1]))
                    res_screen = screen.copy()
                    # Make it a color image
                    res_screen = cv.cvtColor(res_screen, cv.COLOR_GRAY2RGB)
                    for pt in loc:
                        cv.rectangle(res_screen, pt, (pt[0] + ab_mode.shape[1], pt[1] + ab_mode.shape[0]), (0, 255, 0), 2)
                    res_screen = cv.resize(res_screen, (960, 540))
                    cv.imshow("win rate button", res_screen)
                    cv.waitKey(1)
            else:
                print(f"Could not find win rate button ({np.max(res)}/{threshold})")

            time.sleep(self.updateFreq)
