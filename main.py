from battler import BattleHandler
import tkinter as tk
import asyncio
import cv2 as cv

def main():
    win = tk.Tk()
    win.title("LCGT - Limbus Company Grind Tool")

    bh = BattleHandler(False)

    btn = tk.Button(win, text="Start", command=bh.do_battle)
    btn.grid(column=0, row=0)

    win.mainloop()


if __name__ == '__main__':
    main()