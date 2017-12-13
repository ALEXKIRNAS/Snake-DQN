from collections import deque

from utils.point import Point


class SnakeDirections(object):
    """
    Defines all possible directions the snake can take,
    as well as the corresponding offsets.
    """

    NORTH = Point(0, -1)
    EAST = Point(1, 0)
    SOUTH = Point(0, 1)
    WEST = Point(-1, 0)


class SnakeActions(object):
    """
    Defines all possible actions the agent can take
    in the environment.
    """

    MAINTAIN_DIRECTION = 0
    TURN_LEFT = 1
    TURN_RIGHT = 2


ALL_SNAKE_ACTIONS = [
    SnakeActions.TURN_LEFT,
    SnakeActions.TURN_RIGHT,
    SnakeActions.MAINTAIN_DIRECTION,
]


class Snake(object):
    """
    Represents the snake that has a position,
    can move, and change directions.
    """

    ON_LEFT_TURN_DIRECTION_MAPPING = {
        SnakeDirections.NORTH: SnakeDirections.EAST,
        SnakeDirections.WEST: SnakeDirections.NORTH,
        SnakeDirections.SOUTH: SnakeDirections.WEST,
        SnakeDirections.EAST: SnakeDirections.SOUTH,
    }

    ON_RIGHT_TURN_DIRECTION_MAPPING = {
        SnakeDirections.NORTH: SnakeDirections.WEST,
        SnakeDirections.WEST: SnakeDirections.SOUTH,
        SnakeDirections.SOUTH: SnakeDirections.EAST,
        SnakeDirections.EAST: SnakeDirections.NORTH,
    }

    def __init__(self, head_coordinates: Point, length: int = 3):
        """
        Create a new snake.

        Args:
            head_coordinates: initial position of the snake.
            length: initial length of the snake.
        """

        # Place the snake vertically, heading north.
        self.body = deque([
            Point(head_coordinates.x, head_coordinates.y + i)
            for i in range(length)
        ])

        self.direction = SnakeDirections.NORTH

    @property
    def head(self):
        """ Get the position of the snake's head. """
        return self.body[0]

    @property
    def tail(self):
        """ Get the position of the snake's tail. """
        return self.body[-1]

    @property
    def length(self):
        """ Get the current length of the snake. """
        return len(self.body)

    def get_next_point(self):
        """ Get the point the snake will move to at its next step. """
        return self.head + self.direction

    def turn_left(self):
        """
        At the next step, take a left turn relative to the current direction.
        """
        self.direction = Snake.ON_LEFT_TURN_DIRECTION_MAPPING[self.direction]

    def turn_right(self):
        """
        At the next step, take a right turn relative to the current direction.
        """
        self.direction = Snake.ON_RIGHT_TURN_DIRECTION_MAPPING[self.direction]

    def grow(self):
        """
        Grow the snake by 1 block from the head.
        """
        self.body.appendleft(self.get_next_point())

    def move(self):
        """
        Move the snake 1 step forward.
        """
        self.body.appendleft(self.get_next_point())
        self.body.pop()
