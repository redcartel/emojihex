import curses
from random import randrange
from src import controls
from src import display
from src import model
from src.state import get_param

MAPROWS = 24
MAPCOLS = 40
MAP = [[]]
ENTITIES = {}
HIGHLIGHTS = {}
STDSCR = None

def clear_highlights():
    global HIGHLIGHTS
    HIGHLIGHTS = {}

def get_highlight(row, col):
    if row not in HIGHLIGHTS or col not in HIGHLIGHTS[row]:
        return 0
    return HIGHLIGHTS[row][col]

def highlight(row, col):
    if row not in HIGHLIGHTS:
        HIGHLIGHTS[row] = {col: 1}
    else:
        HIGHLIGHTS[row][col] = 1

def move_entity(y, x, entity):
    if "x" in entity and "y" in entity:
        ENTITIES[y][x].remove(entity)
    entity["x"] = x
    entity["y"] = y
    if y not in ENTITIES:
        ENTITIES[y] = {}
    if x not in ENTITIES[y]:
        ENTITIES[y][x] = []
    ENTITIES[y][x].append(entity)

def getents(y, x):
    if y not in ENTITIES:
        return []
    if x not in ENTITIES[y]:
        return []
    return ENTITIES[y][x]

def newmap():
    global MAP
    MAP = [[{"label":str(randrange(100))} for _ in range(MAPCOLS)] for _ in range(MAPROWS)]

def add_random_ents(n=100):
    for _ in range(n):
        ent = {"label": "X"}
        move_entity(randrange(MAPROWS), randrange(MAPCOLS), ent)

def mapsquare(row, col):
    if row < 0 or row >= MAPROWS or col < 0 or col >= MAPCOLS:
        return [' ' * 6] * 3
    #rows = ['+-----', '|{:<3}..'.format(MAP[row][col]["label"]), '|{:<2}.{:<2}'.format(row,col)]
    rows = ['+-----', '|{:<3}..'.format(get_highlight(row,col)), '|{:<2}.{:<2}'.format(row,col)]
    ents = getents(row, col)
    if len(ents) > 0:
        rows[1] = rows[1][:-1] + ents[-1]["label"][0]
    return rows


def y_x_to_mapchar(y, x):
    row = y // 3
    y_offset = y % 3
    col = (x - 3) // 6 if row % 2 else x // 6
    x_offset = (x - 3) % 6 if row % 2 else x % 6
    square = mapsquare(row, col)
    return square[y_offset][x_offset]

def y_x_to_row_col(y, x):
    row = y // 3
    col = (x - 3) // 6 if row % 2 else x // 6
    return row, col

def init_colors():
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

def drawmap(y, x):
    startrow = y
    startcol = x
    stoprow = y + curses.LINES - 1
    stopcol = x + curses.COLS - 1
    for row in range(startrow, stoprow):
        for col in range(startcol, stopcol):
            screen_y = row - startrow
            screen_x = col - startcol
            map_row, map_col = y_x_to_row_col(row, col)
            high = get_highlight(map_row, map_col)
            pair = curses.color_pair(high)
            STDSCR.addstr(screen_y, screen_x, y_x_to_mapchar(row, col), pair)


# def main(stdscr):
#     global STDSCR
#     STDSCR = stdscr

#     newmap()
#     add_random_ents()
#     init_colors()
#     highlight(3,3)
#     highlight(7,9)

#     x_off = 0
#     y_off = 0
#     select_row = 5
#     select_col = 5
#     stopgame = False
#     while not stopgame:
#         clear_highlights()
#         highlight(select_row, select_col)
#         drawmap(y_off, x_off)

def main(stdscr):
    controls.init(stdscr)
    display.init(stdscr)
    model.init()

    while get_param("mode") != -1:
        display.display()
        controls.dispatch_input()



if __name__ == "__main__":
    curses.wrapper(main)
