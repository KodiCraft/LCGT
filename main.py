from battler import BattleHandler
import tkinter as tk
import asyncio


active_task = None


def main():
    bh = BattleHandler(debug=False)
    loop = asyncio.get_event_loop()

    while True:
        print("Starting battle")
        # Start the battle in a new thread
        global active_task
        active_task = loop.create_task(bh.do_battle())
        loop.run_until_complete(active_task)
        print("Battle ended")


if __name__ == '__main__':
    main()
