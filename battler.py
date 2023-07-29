import pyautogui
import time
import cv2 as cv
import numpy as np
import os


class BattleHandler:
    # Settings for the battlehandler
    def __init__(self, debug: bool = False):
        self.active = True
        self.imgPfx = "images/"

        self.abMode = cv.imread("images/winrate.png", 0)
        self.start = cv.imread("images/start.png", 0)
        self.postBattle = cv.imread("images/continue.png", 0)

        self.knownScale = None

        self.lastUpdate = time.time()

        self.debug = debug

    async def do_battle(self):
        self.active = True
        while True:
            if not self.active:
                break
            # Take a screenshot of the entire screen
            screen = pyautogui.screenshot()
            # Convert the screenshot to a numpy array
            screen = np.array(screen)
            screen = cv.cvtColor(screen, cv.COLOR_RGB2GRAY)

            # If we haven't found the scale yet, find it
            if self.knownScale is None:
                scales = [0.5, 1, 1.125, 1.25, 1.5, 2]
            else:
                scales = [self.knownScale]

            res = None
            found_scale = None
            for scale in scales:
                resized = cv.resize(self.abMode, (0, 0), fx=scale, fy=scale)
                found_scale = scale
                res = cv.matchTemplate(screen, resized, cv.TM_CCOEFF_NORMED)
                # We only care about the maximum value
                if np.max(res) > 0.6:
                    self.knownScale = scale # We've now found the game's scale
                    break

            # Resize the image to the scale we found
            ab_mode = cv.resize(self.abMode, (0, 0), fx=found_scale, fy=found_scale)

            threshold = 0.6
            if np.any(res >= threshold):
                loc = np.where(res >= threshold)
                print(f"Found win rate button! ({np.max(res)}/{threshold})")

                res_screen = screen.copy()
                res_screen = cv.cvtColor(res_screen, cv.COLOR_GRAY2RGB)
                if self.debug:
                    # Draw a rectangle around the button
                    for pt in zip(*loc[::-1]):
                        cv.rectangle(res_screen, pt, (pt[0] + ab_mode.shape[1], pt[1] + ab_mode.shape[0]), (0, 0, 255),
                                     2)

                # Click the button
                pyautogui.moveTo(loc[1][0] + ab_mode.shape[1] / 2, loc[0][0] + ab_mode.shape[0] / 2)
                time.sleep(0.1)
                pyautogui.click()

                # Find the start button. We don't need to resize it because it's the same size as the win rate button
                start = cv.resize(self.start, (0, 0), fx=found_scale, fy=found_scale)
                res = cv.matchTemplate(screen, start, cv.TM_CCOEFF_NORMED)
                # We are certain that we will find the start button, so we don't need to check the threshold
                loc = np.where(res >= threshold)
                print(f"Found start button! ({np.max(res)}/{threshold})")

                if self.debug:
                    # Draw a rectangle around the button
                    for pt in zip(*loc[::-1]):
                        cv.rectangle(res_screen, pt, (pt[0] + start.shape[1], pt[1] + start.shape[0]), (0, 0, 255),
                                     2)

                pyautogui.moveTo(loc[1][0] + start.shape[1] / 2, loc[0][0] + start.shape[0] / 2)
                time.sleep(0.1)
                pyautogui.click()

                if self.debug:
                    cv.imshow("Result", res_screen)
                    cv.waitKey(1)

            else:
                print(f"Could not find win rate button ({np.max(res)}/{threshold})")

            # Check if we are in the post-battle screen
            # Look for the 'continue' button
            res = None
            found_scale = None
            scales = [0.5, 1, 1.125, 1.25, 1.5, 2]  # This needs its own scales because our post-battle image is smaller
            for scale in scales:
                resized = cv.resize(self.postBattle, (0, 0), fx=scale, fy=scale)
                found_scale = scale
                res = cv.matchTemplate(screen, resized, cv.TM_CCOEFF_NORMED)
                # We only care about the maximum value
                if np.max(res) > 0.6:
                    break

            # Resize the image to the scale we found
            post_battle = cv.resize(self.postBattle, (0, 0), fx=found_scale, fy=found_scale)

            if np.any(res >= threshold):
                print(f"Found continue button! ({np.max(res)}/{threshold})")
                loc = np.where(res >= threshold)
                # Click the button
                pyautogui.moveTo(loc[1][0] + post_battle.shape[1] / 2, loc[0][0] + post_battle.shape[0] / 2)
                time.sleep(0.25)
                pyautogui.click()
                # Battle end
                print("Battle end")
                self.active = False
                break
            else:
                print(f"Could not find continue button ({np.max(res)}/{threshold})")

    async def watch(self):
        while True:
            await self.do_battle()