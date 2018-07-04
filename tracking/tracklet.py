# -*- coding: utf-8 -*-

"""
<Description>
"""

from tools.tracking.tracking_region import TrackingRegion

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Tracklet:
    def __init__(self, region: TrackingRegion):
        # Basic tracking parameters.
        self.frame = 0
        self.raw_region: TrackingRegion = None
        self.display_region: TrackingRegion = None
        self.set_region(region)

    def set_region(self, region: TrackingRegion):
        self.raw_region = region
        self.display_region = region.clone()
        self.display_region.expand_to_ratio(1.0)
        self.display_region.scale(1.5)

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

