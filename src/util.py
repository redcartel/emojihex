def y_x_to_row_col(y, x):
    row = y // 4
    col = (x + 4) // 8 if row % 2 else x // 8
    return row, col

def y_x_to_offsets(y, x):
    row = y // 4
    yoff = y % 4
    xoff = (x + 4) % 8 if row % 2 else x % 8
    return yoff, xoff

# DIRECTIONS: 0 = right, 1 = down/right 2 = down/left 3 = left 4 = up/left 5 = up/right
# MOVE_DELTA[y%2][2] = delta y, delta x to move down and to the left
# MOVE_DELTAS = [
#     [[0][1], [1][0], [1][-1], [0][-1], [-1][-1], [-1][0]],
#     [[0][1], [1][1], [1][0], [0][-1], [-1][0], [-1][1]]
# ]