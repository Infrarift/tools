# -*- coding: utf-8 -*-

"""
Tracklet: A clustered group of TrackFrames belonging to the same object.
"""

from enum import Enum
from typing import List, Tuple
from tools.util import core
from tools.util.simple_filter import SimpleFilter
from .track_frame import TrackFrame

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class VisualState(Enum):
    NORMAL = 1
    SHOWING = 2
    KILLING = 3
    KILLED = 4


class Tracklet:

    # Visual Constants
    _PINK = (80, 30, 255)
    _RED = (0, 0, 255)
    _BLACK = (0, 0, 0)
    _ANIM_SHOW_MAX = 10
    _ANIM_KILL_MAX = 10

    def __init__(self, hit_limit: int = 3, miss_limit: int = 7,
                 color: Tuple = (255, 255, 255), red_fade: bool=False):
        self.track_frames: List[TrackFrame] = []

        # TODO: We should probably allow this for config passing.

        # Smoothing Filters.
        self._position_filter: SimpleFilter = SimpleFilter(0.5)
        self._size_filter: SimpleFilter = SimpleFilter(0.5)

        # Consecutive.
        self._hit_counter: int = 0
        self._miss_counter: int = 0
        self._hit_limit = hit_limit
        self._miss_limit = miss_limit
        self._activated: bool = False
        self._lost: bool = False
        # TODO: Enum? UNTRACKED, LIVE, LOST?

        # Visual State Information.
        self._anim_show_counter: int = 0
        self._anim_kill_counter: int = 0
        self._color = color
        self._red_fade: bool = red_fade  # Fade using the red animation.
        self.visual_state: VisualState = VisualState.NORMAL

        self.image = None

    # ===================================================================================================
    # Core Public Functions.
    # ===================================================================================================

    def add(self, track_frame: TrackFrame, register_hit: bool=True):
        """ Add a new frame to this Tracklet. Filter the tracklet's display region. """

        self._filter_frame(track_frame)
        self.track_frames.append(track_frame)

        # Also automatically register a hit to this Tracklet.
        if register_hit:
            self.update(True)

    def update(self, hit: bool=True):
        """ This function should be called every frame, to either register a hit or miss. """
        if self._lost:
            self._step_kill_animation()
            return

        self._register(hit)

    # ===================================================================================================
    # Private Functions.
    # ===================================================================================================

    def _filter_frame(self, track_frame: TrackFrame) -> TrackFrame:
        """ Smoothly filter the position and size of the new frame. """
        if len(self.track_frames) > 0:
            pt: TrackFrame = self.track_frames[-1]
            track_frame.x = self._position_filter.process(track_frame.x, pt.x)
            track_frame.y = self._position_filter.process(track_frame.y, pt.y)
            track_frame.width = self._size_filter.process(track_frame.width, pt.width)
            track_frame.height = self._size_filter.process(track_frame.height, pt.height)
        return track_frame

    def _register(self, hit: bool=True):
        """ Register a hit or a miss, and update the counters. """
        if hit:
            self._hit_counter += 1
            self._miss_counter = 0
        else:
            self._miss_counter += 1
            self._hit_counter = 0

        self._check_and_activate()
        self._check_and_kill()

    def _check_and_activate(self):
        """ Check the conditions for activating this Tracklet. Execute it if passed. """
        if not self._activated and self._hit_counter >= self._hit_limit:
            self._activated = True

    def _check_and_kill(self):
        """ Check the conditions for losing this Tracklet. Execute it if passed. """
        if not self._lost and self._miss_counter >= self._miss_limit:
            self._lost = True

            # If it has never been activated, kill it immediately.
            if not self._activated:
                self.visual_state = VisualState.KILLED

    # ===================================================================================================
    # Access Properties.
    # ===================================================================================================

    @property
    def is_recent(self) -> bool:
        """ Received a hit in the latest update cycle. """
        return self._hit_counter > 0

    @property
    def is_live(self) -> bool:
        """ Received enough hits to be activated, and has not yet been lost."""
        return self._activated and not self._lost

    @property
    def is_activated(self) -> bool:
        """ Received enough hits to be considered activated. """
        return self._activated

    @property
    def is_lost(self) -> bool:
        """ Received enough misses to be considered lost."""
        return self._lost

    @property
    def is_displayable(self) -> bool:
        """ Received enough misses to be considered lost."""
        return self.is_activated and self.visual_state != VisualState.KILLED

    @property
    def first_frame(self) -> TrackFrame:
        return self.track_frames[0]

    @property
    def last_frame(self) -> TrackFrame:
        return self.track_frames[-1]

    @property
    def miss_limit(self) -> int:
        return self._miss_limit

    @property
    def hit_limit(self) -> int:
        return self._hit_limit

    # ======================================================================================================================
    # Visual and animation functions.
    # ======================================================================================================================

    @property
    def raw_region(self):
        """ Get the latest raw region of this Tracklet. """
        return self.last_frame.raw_region.clone()

    @property
    def display_region(self):
        """ Gets the display region to show for this current frame."""
        last_region = self.last_frame.display_region.clone()
        if self.is_lost:
            last_region.data["color"] = self._get_kill_animation_color()
        else:
            last_region.data["color"] = self._color
        return last_region

    def _step_kill_animation(self):
        """ Update the kill animation counter. """
        self._anim_kill_counter += 1
        if self._anim_kill_counter >= self._ANIM_KILL_MAX:
            self.visual_state = VisualState.KILLED

    def _get_kill_animation_color(self) -> Tuple:
        """ Get the current display color for this step of the animation. """
        progress = self._anim_kill_counter / self._ANIM_KILL_MAX
        if self._red_fade:
            if progress < 0.5:
                # Flash the box for a while.
                if self._anim_kill_counter % 2 == 0:
                    return self._PINK
                else:
                    return 0, 0, 100
            else:
                # Fade out.
                return core.lerp_color(self._RED, self._BLACK, progress)
        else:
            # Fade out.
            return core.lerp_color(self._color, self._BLACK, 0.5 + progress * 0.5)


