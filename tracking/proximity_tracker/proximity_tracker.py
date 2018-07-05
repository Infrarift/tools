# -*- coding: utf-8 -*-

"""
This is an example extension of the base tracking class, how to use it.
"""

from typing import List

from tools.tracking.tracker import Tracker
from tools.tracking.tracking_region import TrackingRegion
from tools.tracking.tracklet import Tracklet
from tools.tracking.tracklet_group import TrackletGroup
from tools.util.region import Region

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class TrackletPair:
    def __init__(self, tracklet_group: TrackletGroup, new_tracklet: Tracklet, distance: float):
        self.tracklet_group: TrackletGroup = tracklet_group
        self.new_tracklet: Tracklet = new_tracklet
        self.distance: float = distance


class ProximityTracker(Tracker):

    REACH = 1.5

    def __init__(self):
        super().__init__()

    def process(self, regions: List[TrackingRegion], frame_index: int = 0):
        new_tracklets = self._covert_to_tracklets(regions, frame_index)

        # Compare each detection to each other, and make a list of them.
        tracklet_pairs: List[TrackletPair] = []
        for t_group in self.active_tracks:

            if t_group.is_lost:
                continue

            old_t = t_group.tracklets[-1]
            for new_t in new_tracklets:
                distance = Region.distance(new_t.raw_region, old_t.raw_region)
                reach = new_t.raw_region.biggest_edge * self.REACH
                if distance < reach:
                    t_pair: TrackletPair = TrackletPair(t_group, new_t, distance)
                    tracklet_pairs.append(t_pair)

        # For each valid pair, merge them.
        tracklet_pairs.sort(key=lambda x: x.distance)
        merged = {}

        for pair in tracklet_pairs:
            if pair.new_tracklet not in merged and pair.tracklet_group not in merged:
                merged[pair.new_tracklet] = True
                merged[pair.tracklet_group] = True
                pair.tracklet_group.add(pair.new_tracklet)

        # TODO: This loop is probably not efficient.
        # Decay the non-hit tracklets.
        for tg in self.active_tracks:
            if tg not in merged:
                tg.update(hit=False)

        # Add all the un-merged detections.
        for tracklet in new_tracklets:
            if tracklet not in merged:
                tracklet_group: TrackletGroup = TrackletGroup(color=(255, 150, 30))
                tracklet_group.add(tracklet)
                self.active_tracks.append(tracklet_group)
                self.all_tracks.append(tracklet_group)

        # Prune the list of all the tracks.
        keep_groups = [t for t in self.active_tracks if not t.is_lost or t.is_displayable]
        self.active_tracks = keep_groups

