import curses
from src.state import move_param, get_param, set_param

STDSCR = curses.initscr()

def init(stdscr):
    global STDSCR
    STDSCR = stdscr

def dispatch_input():
    key = STDSCR.getch()
    if key == ord('q'):
        set_param("mode", -1)
    elif key == curses.KEY_UP:
        move_param("window", -1, 0, "rel")
    elif key == curses.KEY_RIGHT:
        move_param("window", 0, 1, "rel")
    elif key == curses.KEY_DOWN:
        move_param("window", 1, 0, "rel")
    elif key == curses.KEY_LEFT:
        move_param("window", 0, -1, "rel")
    elif key == ord('h'):
        move_param("select", 0, -1, "rel")
    elif key == ord('j'):
        move_param("select", 1, 0, "rel")
    elif key == ord('k'):
        move_param("select", -1, 0, "rel")
    elif key == ord('l'):
        move_param("select", 0, 1, "rel")