import itertools
import random
from typing import List

import numpy as np

from gameplay.snake import Snake
from utils.point import Point


class CellType(object):
    """ Defines all types of cells that can be found in the game. """

    EMPTY = 0
    FRUIT = 1
    SNAKE_HEAD = 2
    SNAKE_BODY = 3
    WALL = 4


LEVEL_MAP_TO_CELL_TYPE = {
        'S': CellType.SNAKE_HEAD,
        's': CellType.SNAKE_BODY,
        '#': CellType.WALL,
        'O': CellType.FRUIT,
        '.': CellType.EMPTY,
}


CELL_TYPE_TO_LEVEL_MAP = {
    cell_type: level_map_char
    for (level_map_char, cell_type) in LEVEL_MAP_TO_CELL_TYPE.items()
}


class Field(object):
    """ Represents the playing field for the Snake game. """

    def __init__(self, level_map: List[str]):
        """
        Create a new Snake field.

        Args:
            level_map: field representation.
        """
        self.level_map = level_map
        self._cells = None
        self._empty_cells = set()
        self._level_map_to_cell_type = LEVEL_MAP_TO_CELL_TYPE
        self._cell_type_to_level_map = CELL_TYPE_TO_LEVEL_MAP

    def __getitem__(self, point: tuple):
        """ Get the type of cell at the given point. """
        x, y = point
        return self._cells[y, x]

    def __setitem__(self, point: tuple, cell_type: CellType):
        """ Update the type of cell at the given point. """
        x, y = point
        self._cells[y, x] = cell_type

        if cell_type == CellType.EMPTY:
            self._empty_cells.add(point)
        elif point in self._empty_cells:
            self._empty_cells.remove(point)

    def __str__(self):
        return '\n'.join(
            ''.join(self._cell_type_to_level_map[cell] for cell in row)
            for row in self._cells
        )

    @property
    def size(self):
        """ Get the size of the field (size == width == height). """
        return len(self.level_map)

    def create_level(self):
        """ Create a new field based on the level map. """
        try:
            self._cells = np.array([
                [self._level_map_to_cell_type[symbol] for symbol in line]
                for line in self.level_map
            ])
        except KeyError as err:
            raise ValueError(f'Unknown level map symbol: "{err.args[0]}"')

        assert self._cells.dtype != np.object, 'Invalid format. Level map ' \
                                               'must be a square'

        self._empty_cells = {
            Point(x, y)
            for y in range(self.size)
            for x in range(self.size)
            if self[(x, y)] == CellType.EMPTY
        }

    def find_snake_head(self):
        """ Find the snake's head on the field. """
        for y in range(self.size):
            for x in range(self.size):
                if self[(x, y)] == CellType.SNAKE_HEAD:
                    return Point(x, y)
        raise ValueError('Initial snake position '
                         'not specified on the level map')

    def get_random_empty_cell(self):
        """ Get the coordinates of a random empty cell. """
        return random.choice(list(self._empty_cells))

    def place_snake(self, snake: Snake):
        """ Put the snake on the field and fill the cells with its body. """

        self[snake.head] = CellType.SNAKE_HEAD
        snake_body_cells_slice = itertools.islice(snake.body,
                                                  1,
                                                  len(snake.body))
        for snake_cell in snake_body_cells_slice:
            self[snake_cell] = CellType.SNAKE_BODY

    def update_field_repr(self,
                          old_head: Point,
                          old_tail: Point,
                          new_head: Point):
        """
        Update field cells according to the new snake position.

        Environment must be as fast as possible to speed up agent training.
        Therefore, we'll sacrifice some duplication of information between
        the snake body and the field just to execute timesteps faster.

        Args:
            old_head: position of the head before the move.
            old_tail: position of the tail before the move.
            new_head: position of the head after the move.
        """

        self[old_head] = CellType.SNAKE_BODY

        # If we've grown at this step, the tail cell shouldn't move.
        if old_tail:
            self[old_tail] = CellType.EMPTY

        if self[new_head] not in (CellType.WALL, CellType.SNAKE_BODY):
            self[new_head] = CellType.SNAKE_HEAD
