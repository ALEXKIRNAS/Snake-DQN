from ..gameplay.field import CellType


class Colors:
    SCREEN_BACKGROUND = (170, 204, 153)
    CELL_TYPE = {
        CellType.WALL: (56, 56, 56),
        CellType.SNAKE_BODY: (105, 132, 164),
        CellType.SNAKE_HEAD: (122, 154, 191),
        CellType.FRUIT: (173, 52, 80),
    }
