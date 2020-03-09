import curses

CONS = lambda x : None      # used as empty object

def init(stdscr):
    CONS.C_BLACK = 16
    curses.init_color(CONS.C_BLACK, 0, 0, 0)
    CONS.C_WHITE = 17
    curses.init_color(CONS.C_WHITE, 1000, 1000, 1000)