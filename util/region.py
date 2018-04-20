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


class RegionRect:
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


# ======================================================================================================================
# Region Class ---------------------------------------------------------------------------------------------------------
# ======================================================================================================================


class Region:
    def __init__(self):
        self._parent_region = None
        self._absolute_rect = RegionRect()
        self._relative_rect = RegionRect()

    # ---------------------------------------------------------------------------

    @property
    def width(self):
        return self._absolute_rect.width

    @property
    def height(self):
        return self._absolute_rect.height

    @property
    def absolute_x(self):
        return self._absolute_rect.x

    @property
    def absolute_y(self):
        return self._absolute_rect.y

    @property
    def absolute_left(self):
        return self._absolute_rect.left

    @property
    def absolute_right(self):
        return self._absolute_rect.right

    @property
    def absolute_top(self):
        return self._absolute_rect.top

    @property
    def absolute_bottom(self):
        return self._absolute_rect.bottom

    @property
    def relative_left(self):
        return self._relative_rect.left

    @property
    def relative_right(self):
        return self._relative_rect.right

    @property
    def relative_top(self):
        return self._relative_rect.top

    @property
    def relative_bottom(self):
        return self._relative_rect.bottom

    # ---------------------------------------------------------------------------

    def set_parent(self, parent):
        self._parent_region = parent
        self._calibrate_from_absolute()

    def set_absolute_rect(self, left, right, top, bottom):
        self._absolute_rect.set_rect(left, right, top, bottom)
        self._calibrate_from_absolute()

    def set_relative_rect(self, left, right, top, bottom):
        self._relative_rect.set_rect(left, right, top, bottom)
        self._calibrate_from_relative()

    def set_absolute_xy(self, x, y):
        self._absolute_rect.set_xy(x, y)
        self._calibrate_from_absolute()

    def set_relative_xy(self, x, y):
        self._relative_rect.set_xy(x, y)
        self._calibrate_from_relative()

    def set_size(self, width, height):
        self._absolute_rect.set_size(width, height)
        self._calibrate_from_absolute()

    def crop_to_padding(self, left_pad_percent, right_pad_percent, top_pad_percent, bottom_pad_percent):

        """ Crop the region to a percent of its parent's edges. The parent must exist, and the percents each
        expressed as a value from 0 to 1. The percent cropped is counted from the edge of the parent region."""

        # Make sure that this region has a parent.
        if self._parent_region is None or not isinstance(self._parent_region, Region):
            raise Exception("Cropping Error", "A parent region must exist for this cropping operation.")

        # Make sure that the padding values are valid.
        assert (left_pad_percent >= 0)
        assert (right_pad_percent >= 0)
        assert (left_pad_percent + right_pad_percent < 1)
        assert (top_pad_percent >= 0)
        assert (bottom_pad_percent >= 0)
        assert (top_pad_percent + bottom_pad_percent < 1)

        p_height = self._parent_region.height
        p_width = self._parent_region.width

        left = int(left_pad_percent * p_width)
        right = int(p_width - (right_pad_percent * p_width))
        top = int(top_pad_percent * p_height)
        bottom = int(p_height - (bottom_pad_percent * p_height))

        self.set_relative_rect(left, right, top, bottom)

    def contains(self, x, y):
        """ Check whether the xy point is contained within the bounds of this region.

        Returns:
            bool: Whether the point is within the region.
        """
        if x < self.absolute_left or x > self.absolute_right or y < self.absolute_top or y > self.absolute_bottom:
            return False
        return True

    def is_in_bounds(self, width, height):
        """ Check the region against an absolute space of width x height dimensions.

        Returns:
            bool: Whether all parts of this region exist wholly within the width x height bounds.
        """
        if self.absolute_top < 0 \
                or self.absolute_bottom > height \
                or self.absolute_left < 0 \
                or self.absolute_right > width:
            return False
        return True

    # ---------------------------------------------------------------------------

    def _calibrate_from_absolute(self):
        if self._parent_region is not None:
            self._relative_rect.set_rect(
                left=self._absolute_rect.left - self._parent_region._absolute_rect.left,
                right=self._absolute_rect.right - self._parent_region._absolute_rect.left,
                top=self._absolute_rect.top - self._parent_region._absolute_rect.top,
                bottom=self._absolute_rect.bottom - self._parent_region._absolute_rect.top,
            )
        else:
            self._relative_rect.set_rect(
                left=self._absolute_rect.left,
                right=self._absolute_rect.right,
                top=self._absolute_rect.top,
                bottom=self._absolute_rect.bottom,
            )

    def _calibrate_from_relative(self):
        if self._parent_region is not None:
            self._absolute_rect.set_rect(
                left=self._relative_rect.left + self._parent_region._absolute_rect.left,
                right=self._relative_rect.right + self._parent_region._absolute_rect.left,
                top=self._relative_rect.top + self._parent_region._absolute_rect.top,
                bottom=self._relative_rect.bottom + self._parent_region._absolute_rect.top,
            )
        else:
            self._absolute_rect.set_rect(
                left=self._relative_rect.left,
                right=self._relative_rect.right,
                top=self._relative_rect.top,
                bottom=self._relative_rect.bottom,
            )
