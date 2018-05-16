# -*- coding: utf-8 -*-

"""
tools| region | 20/04/18
Region is a rect with extended utility. It has not only its edges as attributes, but also central xy, and size.
The user can adjust any of these values through the setters, and all the other attributes will update accordingly.
Regions can also be nested to be relative to other regions.
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"
__version__ = "0.0.0"


# ======================================================================================================================
# Region Rect (Utility) ------------------------------------------------------------------------------------------------
# ======================================================================================================================


class Region:
    def __init__(self, left=0, right=0, top=0, bottom=0):

        # Rect. Origin (0, 0) is top-left.
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

        # Position
        self.x = 0
        self.y = 0

        # Scale
        self.width = 0
        self.height = 0

        # Initialize
        self.set_rect(left, right, top, bottom)

    def set_rect(self, left, right, top, bottom):
        if right < left:
            raise Exception("Invalid Input", "Right ({}) must be greater than left ({}).".format(right, left))

        if bottom < top:
            raise Exception("Invalid Input", "Bottom ({}) must be greater than top ({}).".format(top, bottom))

        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self._calibrate_to_rect()

    def set_xy(self, x=None, y=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self._calibrate_to_xy()

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self._calibrate_to_xy()

    # ---------------------------------------------------------------------------

    def _calibrate_to_rect(self):
        self.width = self.right - self.left
        self.height = self.bottom - self.top
        self.x = self.left + self.width // 2
        self.y = self.top + self.height // 2

    def _calibrate_to_xy(self):
        half_width = self.width // 2
        half_height = self.height // 2
        self.left = self.x - half_width
        self.right = self.x + half_width
        self.top = self.y - half_height
        self.bottom = self.y + half_height

    def contains(self, x, y):
        if x < self.left or x > self.right or y < self.top or y > self.bottom:
            return False
        return True

    def is_in_bounds(self, width, height):
        if self.top < 0 \
                or self.bottom > height \
                or self.left < 0 \
                or self.right > width:
            return False
        return True
