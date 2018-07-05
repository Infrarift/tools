# -*- coding: utf-8 -*-

"""
This is a universal, generic tracker system that generates tracks for an arbitrary input.
"""

from abc import abstractmethod
from typing import List
from tools.tracking.tracking_region import TrackingRegion
from tools.tracking.tracklet import Tracklet
from tools.tracking.tracklet_group import TrackletGroup

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Tracker:

    def __init__(self):
        self.active_tracks: List[TrackletGroup] = []
        self.all_tracks: List[TrackletGroup] = []

    def reset(self):
        self.active_tracks = []
        self.all_tracks = []

    @abstractmethod
    def process(self, regions: List[TrackingRegion], frame_index: int = 0):
        pass

    def get_live_tracklet_groups(self) -> List[TrackletGroup]:
        return self.active_tracks

    def get_live_regions(self) -> List[TrackingRegion]:
        return [t.display_region for t in self.active_tracks if t.is_live]

    def get_lost_regions(self) -> List[TrackingRegion]:
        return [t.display_region for t in self.active_tracks if t.is_lost]

    @staticmethod
    def _covert_to_tracklets(regions: List[TrackingRegion], frame_index: int = 0) -> List[Tracklet]:
        """ Convert from TrackingRegions to a list of Tracklets. """
        tracklets: List[Tracklet] = []
        for region in regions:
            tracklet: Tracklet = Tracklet(region)
            tracklet.frame = frame_index
            tracklets.append(tracklet)
        return tracklets

