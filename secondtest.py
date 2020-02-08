import curses
from random import randrange

def main(stdscr):
    for y in range(curses.LINES - 1):
        for x in range(curses.COLS - 1):
            stdscr.addstr(y, x, str(y % 2 * 2 + x % 2))
    stdscr.refresh()
    stdscr.getkey()

if __name__ == "__main__":
    curses.wrapper(main)