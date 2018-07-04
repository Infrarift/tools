# -*- coding: utf-8 -*-

"""
This is a universal, generic tracker system that generates tracks for an arbitrary input.
"""

from typing import List
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


class Tracker:

    REACH = 3.5

    def __init__(self):
        self.tracklet_groups: List[TrackletGroup] = []
        self.archive_tracklet_groups: List[TrackletGroup] = []

    def reset(self):
        self.tracklet_groups: List[TrackletGroup] = []

    def process(self, regions: List[TrackingRegion]):

        new_tracklets = self._covert_to_tracklets(regions)

        # Compare each detection to each other, and make a list of them.
        tracklet_pairs: List[TrackletPair] = []
        for t_group in self.tracklet_groups:

            if t_group.lost:
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
        for tg in self.tracklet_groups:
            if tg not in merged:
                tg.register(hit=False)

        # Add all the un-merged detections.
        for tracklet in new_tracklets:
            if tracklet not in merged:
                tracklet_group: TrackletGroup = TrackletGroup()
                tracklet_group.add(tracklet)
                self.tracklet_groups.append(tracklet_group)

        # Prune the list of all the tracks.
        lost_groups = [t for t in self.tracklet_groups if t.kill_finished]
        keep_groups = [t for t in self.tracklet_groups if not t.kill_finished]

        self.tracklet_groups = keep_groups
        self.archive_tracklet_groups += lost_groups

    def get_live_tracklet_groups(self) -> List[TrackletGroup]:
        return self.tracklet_groups

    def get_live_regions(self) -> List[TrackingRegion]:
        return [t.get_display_region() for t in self.tracklet_groups if t.is_live]

    def get_lost_regions(self) -> List[TrackingRegion]:
        return [t.get_display_region() for t in self.tracklet_groups if t.lost]

    @staticmethod
    def _covert_to_tracklets(regions: List[TrackingRegion]) -> List[Tracklet]:
        """ Convert from TrackingRegions to a list of Tracklets. """
        tracklets: List[Tracklet] = []
        for region in regions:
            tracklet: Tracklet = Tracklet(region)
            tracklets.append(tracklet)
        return tracklets

