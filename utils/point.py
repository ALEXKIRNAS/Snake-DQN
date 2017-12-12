from collections import namedtuple


class Point(namedtuple('BasePoint', ['x', 'y'])):
    """ Represents a 2D point with named axes. """

    def __add__(self, other):
        """ Add two points coordinate-wise. """
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """ Subtract two points coordinate-wise. """
        return Point(self.x - other.x, self.y - other.y)

