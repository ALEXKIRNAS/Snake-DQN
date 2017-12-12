from ..gameplay.field import CellType

LEVEL_MAP_TO_CELL_TYPE = {
        'S': CellType.SNAKE_HEAD,
        's': CellType.SNAKE_BODY,
        '#': CellType.WALL,
        'O': CellType.FRUIT,
        '.': CellType.EMPTY,
}

CELL_TYPE_TO_LEVEL_MAP = {
    cell_type: level_map_char
    for (level_map_char, cell_type) in LEVEL_MAP_TO_CELL_TYPE
}
