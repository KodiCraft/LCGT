from battler import BattleHandler
import tkinter as tk
import asyncio


def main():
    win = tk.Tk()
    win.title("LCGT - Limbus Company Grind Tool")

    bh = BattleHandler(1)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bh.wait_for_turn())

    win.mainloop()


if __name__ == '__main__':
    main()