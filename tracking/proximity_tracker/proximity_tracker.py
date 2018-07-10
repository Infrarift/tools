# -*- coding: utf-8 -*-

"""
This is an example extension of the base tracking class, how to use it.
"""

from typing import List

from tools.tracking.tracker import Tracker
from tools.tracking.tracking_region import TrackingRegion
from tools.tracking.track_frame import TrackFrame
from tools.tracking.tracklet import Tracklet
from tools.util.region import Region

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class TrackletPair:
    def __init__(self, tracklet: Tracklet, new_frame: TrackFrame, distance: float):
        self.tracklet: Tracklet = tracklet
        self.new_frame: TrackFrame = new_frame
        self.distance: float = distance


class ProximityTracker(Tracker):

    REACH = 1.5

    def __init__(self):
        super().__init__()

    def process(self, regions: List[TrackingRegion], frame_index: int = 0):
        new_frames = self._convert_to_track_frames(regions, frame_index, ratio_lock=1.0, scale_factor=1.5)

        # Compare each detection to each other, and make a list of them.
        tracklet_pairs: List[TrackletPair] = []
        for tracklet in self.active_tracklets:

            if tracklet.is_lost:
                continue

            old_t = tracklet.track_frames[-1]
            for new_t in new_frames:
                distance = Region.distance(new_t.raw_region, old_t.raw_region)
                reach = new_t.raw_region.biggest_edge * self.REACH
                if distance < reach:
                    t_pair: TrackletPair = TrackletPair(tracklet, new_t, distance)
                    tracklet_pairs.append(t_pair)

        # For each valid pair, merge them.
        tracklet_pairs.sort(key=lambda x: x.distance)
        merged = {}

        for pair in tracklet_pairs:
            if pair.new_frame not in merged and pair.tracklet not in merged:
                merged[pair.new_frame] = True
                merged[pair.tracklet] = True
                pair.tracklet.add(pair.new_frame)

        # TODO: This loop is probably not efficient.
        # Decay the non-hit tracklets.
        for tracklet in self.active_tracklets:
            if tracklet not in merged:
                tracklet.update(hit=False)

        # Add all the un-merged detections.
        for frame in new_frames:
            if frame not in merged:
                tracklet: Tracklet = Tracklet(color=(255, 150, 30), red_fade=True)
                tracklet.add(frame)
                self.active_tracklets.append(tracklet)
                self.all_tracklets.append(tracklet)

        # Prune the list of all the tracks.
        self.remove_dead_tracklets()

