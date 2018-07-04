# -*- coding: utf-8 -*-

"""
A sub-class of region with some added meta-data for better tracking performance.
"""

from tools.util.region import Region

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class TrackingRegion(Region):

    def __init__(self, left=0, right=0, top=0, bottom=0):
        super().__init__(left, right, top, bottom)

        self.confidence: float = 0.0
        self.label: str = None
        self.data: dict = {}  # Arbitrary data pointer.

    def clone(self) -> 'TrackingRegion':
        region = TrackingRegion()
        region.set_rect(self.left, self.right, self.top, self.bottom)
        region.confidence = self.confidence
        region.label = self.label
        region.data = self.data
        return region

