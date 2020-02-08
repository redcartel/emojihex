import curses
from src.state import get_param
from src.util import y_x_to_offsets, y_x_to_row_col
from src.model import get_square, get_entities

STDSCR = curses.initscr()

HIGHLIGHTS = {}

def init(stdscr):
    global STDSCR
    STDSCR = stdscr
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

def clear_highlights():
    HIGHLIGHTS.clear()

def get_highlight(row, col):
    if row not in HIGHLIGHTS or col not in HIGHLIGHTS[row]:
        return curses.color_pair(0)
    return curses.color_pair(HIGHLIGHTS[row][col])

def highlight(row, col, pairnumber=1):
    if row not in HIGHLIGHTS:
        HIGHLIGHTS[row] = {col: 1}
    else:
        HIGHLIGHTS[row][col] = 1

# def drawmap(mapy, mapx, drawy = 0, drawx = 0, height = None, width = None):
#     if width is None:
#         stoprow = mapy + curses.LINES - drawy - 1
#         stopcol = mapx + curses.COLS - drawx - 1
#     else:
#         stoprow = mapy + height
#         stopcol = mapx + width

#     for y in range(mapy, stoprow):
#         for x in range(mapx, stopcol):
#             screen_y = y - mapy + drawy
#             screen_x = x - mapx + drawx
#             STDSCR.addstr(screen_y, screen_x, *y_x_to_mapchar_pair(y, x))

def drawmap(mapy, mapx, drawy = 0, drawx = 0, height = None, width = None):
    if width is None:
        stoprow = mapy + curses.LINES - drawy - 1
        stopcol = mapx + (curses.COLS - drawx - 1) // 2
    else:
        stoprow = mapy + height
        stopcol = mapx + width

    for y in range(mapy, stoprow):
        for x in range(mapx, stopcol):
            screen_y = y - mapy + drawy
            screen_x = (x - mapx) * 2 + drawx
            if y % 4 == 0:
                char = '--'
            elif x % 4 == 0:
                char = '|.'
            elif x % 4 == 2 and y % 4 == 2:
                char = '👨'
            else:
                char = '..'
            STDSCR.addstr(screen_y, screen_x, char)

def display():
    clear_highlights()
    highlight(get_param("select_y"), get_param("select_x"))
    drawmap(get_param("window_y"), get_param("window_x"))
    STDSCR.refresh()

def y_x_to_mapchar_pair(y, x):
    row, col = y_x_to_row_col(y, x)
    yoff, xoff = y_x_to_offsets(y, x)
    square = get_square(row, col)
    ents = get_entities(row, col)
    char = square_display(yoff, xoff, square, ents, row, col)
    pair = get_highlight(row, col)

    return char, pair

def square_display(yoff, xoff, mapsquare, ents=[], row=None, col=None):
    if not mapsquare:
        return ' ' 
    rows = ['+' + '-' * 7, '|{:<6}.'.format(mapsquare["label"]), '|'+'.' * 7, '|'+'.' * 7]
    if row is not None:
        rows[0] = '+{:<3}.{:<3}'.format(row, col)
    if ents:
        rows[2] = rows[2][:-2] + "X" + "."

    return rows[yoff][xoff]