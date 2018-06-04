# -*- coding: utf-8 -*-

"""
visual | cell-scan | 4/06/18
Library to do some cool visual stuff.
"""

import numpy as np
import colorsys

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


def random_colors(n):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0
    hsv = [(i / n, 1, brightness) for i in range(n)]
    colors_raw = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    colors = np.array(colors_raw)
    colors *= 255
    # np.random.shuffle(colors)
    return colors
