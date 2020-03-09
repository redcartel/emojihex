from random import randrange

GAME = {
    "maprows": 24,
    "mapcols": 40,
    "turn": 0
}

MAP = [[]]
ENTITIES = []

{y:{x:[] for x in range(GAME["mapcols"])} for y in range(GAME["maprows"])}

def init_entities():
    global ENTITIES
    cols = GAME["mapcols"]
    rows = GAME["maprows"]
    ENTITIES = [[[] for x in range(cols)] for y in range(rows)]

def init():
    init_entities()
    # init_map()
    randomize_map()
    place_entity(1,1,{"label": "X"})
    #randomize_entities()

def randomize_map():
    MAP.clear()
    for row in range(GAME["maprows"]):
        new_row = []
        for col in range(GAME["mapcols"]):
            new_row.append({"label": randrange(100)})
        MAP.append(new_row)

def randomize_entities(n = 100):
    place_entity(2,3, {"label": "X"})
    return
    for _ in range(n):
        y = 10
        x = 15
        assert len(ENTITIES) > y, f"{len(ENTITIES)}"
        place_entity(y,x, {"label": "X"})

def remove_entity(entity):
    y = entity["y"]
    x = entity["x"]
    if entity not in ENTITIES[y][x]:
        raise(ValueError(f"Entity {entity} not at {y} {x}"))
    ENTITIES[y][x].remove(entity)

def place_entity(y, x, entity):
    entity["y"] = y
    entity["x"] = x
    ENTITIES[y][x].append(entity)

def get_entities(y, x):
    if 0 <= y < GAME["maprows"] and 0 <= x < GAME["mapcols"]:
        return ENTITIES[y][x]
    return []

def get_square(row, col):
    if 0 <= row < GAME["maprows"] and 0 <= col < GAME["mapcols"]:
        return MAP[row][col]
    return {}