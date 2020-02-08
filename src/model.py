from random import randrange

GAME = {
    "maprows": 24,
    "mapcols": 40,
    "turn": 0
}

MAP = [[]]
ENTITIES = {}


def init():
    randomize_map()
    randomize_entities()

def randomize_map():
    MAP.clear()
    for row in range(GAME["maprows"]):
        new_row = []
        for col in range(GAME["mapcols"]):
            new_row.append({"label": randrange(100)})
        MAP.append(new_row)

def randomize_entities(n = 100):
    ENTITIES.clear()
    for _ in range(n):
        y = randrange(GAME["maprows"])
        x = randrange(GAME["mapcols"])
        move_entity(y,x, {"label": "X"})

def move_entity(y, x, entity):
    if "y" in entity:
        try:
            ENTITIES[entity["y"]][entity["x"]].remove(entity)
        except (KeyError, ValueError):
            for row in ENTITIES:
                for col in row:
                    if entity in col:
                        col.remove(entity)
    if y not in ENTITIES:
        ENTITIES[y] = {}
    if x not in ENTITIES[y]:
        ENTITIES[y][x] = []
    ENTITIES[y][x].append(entity)

def get_entities(y, x):
    if y not in ENTITIES or x not in ENTITIES[y]:
        return []
    return ENTITIES[y][x] 

def get_square(row, col):
    if 0 < row < GAME["maprows"] and 0 < col < GAME["mapcols"]:
        return MAP[row][col]
    return {}