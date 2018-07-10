# -*- coding: utf-8 -*-

"""
This is a universal, generic tracker system that generates tracks for an arbitrary input.
"""

from abc import abstractmethod
from typing import List
from tools.tracking.tracking_region import TrackingRegion
from tools.tracking.track_frame import TrackFrame
from tools.tracking.tracklet import Tracklet

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Tracker:

    def __init__(self):
        self.active_tracklets: List[Tracklet] = []
        self.all_tracklets: List[Tracklet] = []

    def reset(self):
        self.active_tracklets = []
        self.all_tracklets = []

    @abstractmethod
    def process(self, regions: List[TrackingRegion], frame_index: int = 0):
        pass

    def remove_dead_tracklets(self) -> None:
        """ Get rid of the tracklets that we don't need anymore. """
        self.active_tracklets = [t for t in self.active_tracklets if not t.is_lost or t.is_displayable]

    def get_live_tracklets(self) -> List[Tracklet]:
        return self.active_tracklets

    def get_live_regions(self) -> List[TrackingRegion]:
        return [t.display_region for t in self.active_tracklets if t.is_live]

    def get_lost_regions(self) -> List[TrackingRegion]:
        return [t.display_region for t in self.active_tracklets if t.is_lost]

    def get_raw_regions(self) -> List[TrackingRegion]:
        return [t.raw_region for t in self.active_tracklets if t.is_recent]

    @staticmethod
    def _convert_to_track_frames(regions: List[TrackingRegion], frame_index: int = 0,
                                 ratio_lock: float=0.0, scale_factor: float=1.0) -> List[TrackFrame]:
        """ Convert from TrackingRegions to a list of Tracklets. """
        track_frames: List[TrackFrame] = []
        for region in regions:
            track_frame: TrackFrame = TrackFrame(region, ratio_lock=ratio_lock, scale_factor=scale_factor)
            track_frame.frame = frame_index
            track_frames.append(track_frame)
        return track_frames

