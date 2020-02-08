STATE = {
    "window_x": 0,
    "window_y": 0,
    "select_x": 5,
    "select_y": 5,
    "mode": 1
}

def move_param(pname, y, x, mode="abs"):
    if mode == "abs":
        STATE[pname + "_x"], STATE[pname + "_y"] = x, y
    elif mode == "rel":
        STATE[pname + "_x"] += x
        STATE[pname + "_y"] += y
    else:
        raise ValueError("mode must be abs or rel")

def get_param(pname):
    return STATE[pname]

def set_param(pname, value, mode="abs"):
    if mode == "abs":
        STATE[pname] = value
    elif mode == "rel":
        STATE[pname] += value
    else:
        raise ValueError("mode must be abs or rel")

MAP = [[]]

HIGHLIGHTS = {}

ENTITIES = {}