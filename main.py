import curses
from random import randrange
from src import controls
from src import display
from src import model
from src import resources
from src.util import logger
from src.state import get_param
import datetime

def main(stdscr):
    logger.info(f"\nmain() at {datetime.datetime.now().isoformat()}")
    controls.init(stdscr)
    resources.init(stdscr)
    display.init(stdscr)
    model.init()

    while get_param("mode") != -1:
        display.display()
        controls.dispatch_input()

if __name__ == "__main__":
    curses.wrapper(main)
