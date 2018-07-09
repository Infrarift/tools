# -*- coding: utf-8 -*-

"""
This is a tracking frame for a particular track. It essentially contains a raw region of the detection,
and a modified display region.
"""

from tools.tracking.tracking_region import TrackingRegion

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class TrackFrame:
    def __init__(self, region: TrackingRegion=None, ratio_lock: float=0.0, scale_factor: float=1.0):
        # Basic tracking parameters.
        self.scale_factor = scale_factor
        self.ratio_lock = ratio_lock
        self.frame = 0
        self.raw_region: TrackingRegion = None
        self.display_region: TrackingRegion = None

        if region is not None:
            self.set_region(region)

    def set_region(self, region: TrackingRegion):
        if region is not None:
            self.raw_region = region
            self.display_region = region.clone()
            if self.ratio_lock != 0:
                self.display_region.expand_to_ratio(self.ratio_lock)
            self.display_region.scale(self.scale_factor)

    @property
    def x(self):
        return self.display_region.x

    @x.setter
    def x(self, value):
        self.display_region.x = int(value)

    @property
    def y(self):
        return self.display_region.y

    @y.setter
    def y(self, value):
        self.display_region.y = int(value)

    @property
    def width(self):
        return self.display_region.width

    @width.setter
    def width(self, value):
        self.display_region.width = int(value)

    @property
    def height(self):
        return self.display_region.height

    @height.setter
    def height(self, value):
        self.display_region.height = int(value)

