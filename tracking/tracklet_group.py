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

    BLUE_FADE = True

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
        if self.lost:
            last_region.data["color"] = self._get_kill_animation_color()
        return last_region

    def step_kill_animation(self):
        self.anim_kill_counter += 1

        if self.anim_kill_counter >= self.ANIM_KILL_MAX:
            self.kill_finished = True

    def _get_kill_animation_color(self):

        black = (0, 0, 0)
        progress = self.anim_kill_counter / self.ANIM_KILL_MAX

        if self.BLUE_FADE:
            return self._lerp_color((200, 75, 15), black, progress)
        else:
            pink = (80, 30, 255)
            red = (0, 0, 255)
            if progress < 0.5:
                if self.anim_kill_counter % 2 == 0:
                    return pink
                else:
                    return 0, 0, 100
            else:
                return self._lerp_color(red, black, progress)

    # TODO: Split this out into another module.

    def _lerp_color(self, c1, c2, factor: float):
        new_color = []
        for i in range(3):
            new_color.append(int(self.lerp(c1[i], c2[i], factor)))
        return new_color

    def lerp(self, f1: float, f2: float, factor: float):
        return f1 + (f2 - f1) * factor

