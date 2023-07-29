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
            screen = cv.cvtColor(screen, cv.COLOR_BGR2RGB)

            # Load the image of the win rate button
            ab_mode = cv.imread(self.imgPfx + self.abMode)

            # If we can find the win rate button, it's our turn
            res = cv.matchTemplate(screen, ab_mode, cv.TM_CCOEFF_NORMED)

            threshold = 0.8
            if np.any(res >= threshold):
                # Click the win rate button
                loc = np.where(res >= threshold)
                print(f"Found ({np.max(res)}/{threshold}), clicking...")

                if self.debug:
                    self.display_locations(screen, ab_mode, loc)

                # pyautogui.click(loc[1][0] + 10, loc[0][0] + 10)

            else:
                # Wait for the next turn
                print(f"Not found ({np.max(res)}/{threshold}), waiting...")

            time.sleep(self.updateFreq)

    @staticmethod
    def display_locations(img, template, locs):
        w, h = template.shape[::-1]
        for pt in zip(*locs[::-1]):
            cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        cv.imshow('screen', img)
        cv.waitKey(1)
        cv.destroyAllWindows()
