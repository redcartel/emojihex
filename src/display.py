import curses
from random import randrange
from collections import OrderedDict

from src.state import get_param
from src.util import y_x_to_offsets, y_x_to_row_col
from src.model import get_square, get_entities, GAME
from src.resources import CONS


STDSCR = curses.initscr()

TERRAIN = OrderedDict()

TERRAIN['OCEAN'] = '🌊'[0] + '\0'
TERRAIN['SHALLOW'] = '💧'[0] + '\0'
TERRAIN['PLAINS'] = '🌾'[0] + '\0'
TERRAIN['GRASSLAND'] = '🌱'[0] + '\0'
TERRAIN['FOREST'] = '🌳'[0] + '\0'
TERRAIN['HILLS'] = '🌄'[0] + '\0'
TERRAIN['DESERT'] = '🏜'[0] + '\0'
TERRAIN['TUNDRA'] = '⛄'[0] + '\0'
TERRAIN['MOUNTAIN'] = '⛰'[0] + '\0'
TERRAIN_LIST = list(TERRAIN.values())

ENTS = OrderedDict()
ENTS['NONE'] = "\u2003" + '\0'
ENTS['WORKER'] = '👨‍🔧'[0] + '\0'
ENTS['WARRIOR'] = '💪'[0] + '\0'

def init(stdscr):
    global STDSCR
    if stdscr:
        STDSCR = stdscr
    # curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.curs_set(0)
    STDSCR.refresh()

HIGHLIGHTS = {}

def display():
    clear_highlights()
    STDSCR.clear()
    highlight(get_param("select_y"), get_param("select_x"))
    drawmap(get_param("window_y"), get_param("window_x"))
    STDSCR.refresh()

def map_square_chars(mapsquare, ents=[], row=0, col=0):
    rows = [" " * 8] * 4
    if not mapsquare:
        return rows

    military = ENTS['NONE']
    civilian = ENTS['NONE']
    if ents:
        if len(ents) >= 2:
            military = ENTS['WARRIOR']
            civilian = ENTS['WORKER']
        elif (row + col) % 2:
            military = ENTS['WARRIOR']
        else:
            civilian = ENTS['WORKER']
    entstr = military + civilian
    assert(len(entstr) == 4)

    terrain = TERRAIN_LIST[row // 2 * col // 2 % len(TERRAIN_LIST)]

    terrainstr = terrain * 2

    rows[0] = "+{:=^7}".format("{}={}".format(str(row), str(col)))
    rows[1] = "| " + entstr + '  '
    rows[2] = "| " + terrainstr + '  '
    rows[3] = "| " + '  ' * 3
    return rows

def drawmap(mapy, mapx, drawy = 0, drawx = 0, height = None, width = None):
    if width is None:
        stoprow = mapy + curses.LINES - drawy - 1
        stopcol = mapx + curses.COLS - drawx - 1
    else:
        stoprow = mapy + height
        stopcol = mapx + width

    for y in range(mapy, stoprow):
        for x in range(mapx, stopcol):
            screen_y = y - mapy + drawy
            screen_x = x - mapx + drawx
            char, pair = y_x_to_char(y, x), y_x_to_pair(y, x)
            lchar = y_x_to_char(y, x-1)
            if ord(lchar) >= 128512 or char == '\0':
                pass
            else:
                STDSCR.addstr(screen_y, screen_x, char, pair)

def y_x_to_char(y, x):
    row, col = y_x_to_row_col(y, x)
    square = get_square(row, col)
    if not square:
        return '\0'
    yoff, xoff = y_x_to_offsets(y, x)
    ents = get_entities(y, x)
    chargrid = map_square_chars(square, ents, row, col)
    return chargrid[yoff][xoff]

def y_x_to_pair(y, x):
    row, col = y_x_to_row_col(y, x)
    yoff, xoff = y_x_to_offsets(y, x)
    square = get_square(row, col)
    char = y_x_to_char(y, x)
    highlight = get_highlight(y, x)
    if highlight:
        return curses.color_pair(1)
    return curses.color_pair(0)

# def y_x_to_mapchar_pair(y, x):
#     row, col = y_x_to_row_col(y, x)
#     yoff, xoff = y_x_to_offsets(y, x)
#     square = get_square(row, col)
#     ents = get_entities(row, col)
#     display = square_display(square, ents, row, col)
#     char = display[yoff][xoff]
#     pair = y_x_to_color_pair
#     pair = get_highlight(row, col)
#     return char, pair

def clear_highlights():
    HIGHLIGHTS.clear()

def get_highlight(row, col):
    if row not in HIGHLIGHTS or col not in HIGHLIGHTS[row]:
        return 0
    if HIGHLIGHTS[row][col]:
        return 1

def highlight(row, col, pairnumber=1):
    if row not in HIGHLIGHTS:
        HIGHLIGHTS[row] = {col: 1}
    else:
        HIGHLIGHTS[row][col] = 1