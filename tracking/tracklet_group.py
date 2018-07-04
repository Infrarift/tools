# -*- coding: utf-8 -*-

"""
<Description>
"""
from typing import List

from .tracklet import Tracklet

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class TrackletGroup:

    FILTER = 0.85
    R_FILTER = 1.0 - FILTER

    S_FILTER = 0.15
    R_S_FILTER = 1.0 - S_FILTER
    
    HIT_LIMIT = 3
    MISS_LIMIT = 7

    ANIM_SHOW_MAX = 10
    ANIM_KILL_MAX = 10

    def __init__(self):
        self.tracklets: List[Tracklet] = []

        # Consecutive.
        self.hits: int = 0
        self.misses: int = 0
        self.activated: bool = False
        self.lost: bool = False

        # Animation
        self.anim_show_counter: int = 0
        self.anim_kill_counter: int = 0
        self.show_finished: bool = False
        self.kill_finished: bool = False

    def add(self, tracklet: Tracklet):

        if len(self.tracklets) > 0:
            pt: Tracklet = self.tracklets[-1]
            tracklet.x = tracklet.x * self.FILTER + pt.x * self.R_FILTER
            tracklet.y = tracklet.y * self.FILTER + pt.y * self.R_FILTER
            tracklet.width = tracklet.width * self.S_FILTER + pt.width * self.R_S_FILTER
            tracklet.height = tracklet.height * self.S_FILTER + pt.height * self.R_S_FILTER

        self.tracklets.append(tracklet)
        self.register(hit=True)

    def register(self, hit: bool=True):

        if self.lost:
            self.step_kill_animation()
            return

        if hit:
            self.hits += 1
            self.misses = 0
        else:
            self.misses += 1
            self.hits = 0

        if not self.activated and self.hits >= self.HIT_LIMIT:
            self.activated = True

        if not self.lost and self.misses >= self.MISS_LIMIT:
            self.lost = True
            if not self.activated:
                self.kill_finished = True

    @property
    def recent_hit(self) -> bool:
        return self.hits > 0

    @property
    def is_live(self) -> bool:
        return self.activated and not self.lost

    # ======================================================================================================================
    # Hit and Loss Animation.
    # ======================================================================================================================

    def get_display_region(self):
        last_region = self.tracklets[-1].display_region.clone()
        return last_region

    def step_kill_animation(self):
        self.anim_kill_counter += 1

        if self.anim_kill_counter >= self.ANIM_KILL_MAX:
            self.kill_finished = True

