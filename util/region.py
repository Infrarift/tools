# -*- coding: utf-8 -*-

"""
tools| region | 20/04/18
A region is essentially a rectangle with some extra functionality. I've made it so the attributes will update each other.
"""

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"
__version__ = "1.0.0"


class Region:
    def __init__(self, left=0, right=0, top=0, bottom=0):

        # Rect. Origin (0, 0) is top-left.
        self._left = 0
        self._right = 0
        self._top = 0
        self._bottom = 0

        # Position
        self._x = 0
        self._y = 0

        # Scale
        self._width = 0
        self._height = 0

        # Initialize
        self.set_rect(left, right, top, bottom)

    # ===============================================================================================================================
    # Functions to set the attributes explicitly.
    # ===============================================================================================================================

    def set_rect(self, left, right, top, bottom):
        if right < left:
            raise Exception("Invalid Input", "Right ({}) must be greater than left ({}).".format(right, left))

        if bottom < top:
            raise Exception("Invalid Input", "Bottom ({}) must be greater than top ({}).".format(top, bottom))

        self._left = left
        self._right = right
        self._top = top
        self._bottom = bottom
        self._calibrate_to_rect()

    def set_xy(self, x=None, y=None):
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        self._calibrate_to_xy()

    def set_size(self, width, height):
        self._width = width
        self._height = height
        self._calibrate_to_xy()

    # ======================================================================================================================
    # Utility functions.
    # ======================================================================================================================

    def contains(self, x, y) -> bool:
        """" Checks if the given x, y position is within the area of this region. """
        if x < self._left or x > self._right or y < self._top or y > self._bottom:
            return False
        return True

    def is_in_bounds(self, width, height) -> bool:
        """ Check if this entire region is contained within the bounds of a given stage size."""
        if self._top < 0 \
                or self._bottom > height \
                or self._left < 0 \
                or self._right > width:
            return False
        return True

    # ======================================================================================================================
    # Private calibration functions.
    # ======================================================================================================================

    def _calibrate_to_rect(self) -> None:
        self._width = self._right - self._left
        self._height = self._bottom - self._top
        self._x = self._left + self._width // 2
        self._y = self._top + self._height // 2

    def _calibrate_to_xy(self) -> None:
        half_width = self._width // 2
        half_height = self._height // 2
        self._left = self._x - half_width
        self._right = self._x + half_width
        self._top = self._y - half_height
        self._bottom = self._y + half_height

    # ======================================================================================================================
    # Property setters for our attributes.
    # ======================================================================================================================

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._calibrate_to_xy()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._calibrate_to_xy()

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value
        self._calibrate_to_rect()

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = value
        self._calibrate_to_rect()

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value):
        self._top = value
        self._calibrate_to_rect()

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, value):
        self._bottom = value
        self._calibrate_to_rect()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self._calibrate_to_xy()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self._calibrate_to_xy()
    


