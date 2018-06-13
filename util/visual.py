# -*- coding: utf-8 -*-

"""
Library to do some cool visual stuff.
"""

import cv2
import numpy as np
import colorsys

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


# ======================================================================================================================
# Color Tools.
# ======================================================================================================================


def generate_colors(n, saturation: float=1.0, brightness: float=1.0):
    """ Generate N amount of colors spread across a range on the HSV scale.
    Will return it in a numpy format. """
    hsv = [(i / n, saturation, brightness) for i in range(n)]
    colors_raw = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    colors = np.array(colors_raw)
    colors *= 255
    return colors

# TODO: Wish list - Create a colormap system like in CV2, or adapt it so I can create my own color maps.


# ======================================================================================================================
# Progress (or custom) Bars.
# ======================================================================================================================


def draw_bar(image, progress: float, x: int, y: int, width: int, height: int,
             frame_color=(0, 0, 0), bar_color=(0, 150, 255)):
    """ Draw a rectangular bar, with the specified progress value filled out. """
    draw_bar_segment(image, 0.0, 1.0, x, y, width, height, frame_color)  # Frame
    draw_bar_segment(image, 0.0, progress, x, y, width, height, bar_color)  # Bar


def draw_bar_segment(image, p_start: float, p_end: float, x: int, y: int, width: int, height: int, color=(0, 150, 255)):
    """ Draw a segment of a bar, for example if we just wanted a start-end section.
    Starting point is the top left. """

    # Draw the bar.
    p_width = max(0.05, p_end - p_start)
    p_width = int(width * p_width)
    p_x = int(x + p_start * width)
    cv2.rectangle(image, (p_x, y), (p_x + p_width, y + height), color, thickness=-1)


# ======================================================================================================================
# Text Tools.
# ======================================================================================================================

# TODO: Split into box-align, text-align, etc.

ALIGN_CENTER: int = 0
ALIGN_LEFT: int = -1
ALIGN_RIGHT: int = 1


def create_text_box(image: np.array,
                    text: str,
                    x: int, y: int, width: int, height: int,
                    text_color=(255, 255, 255), bg_color=(0, 0, 0),
                    centered: bool=False):
    """ Create a text box, with the text written in the center."""

    # Find the corners of the box that we want to draw.
    if centered:
        bot_left = (x - width // 2, y + height // 2)
        top_right = (x + width // 2, y - height // 2)
    else:
        bot_left = (x, y + height)
        top_right = (x + width, y)

    # Create a black BG plate for the text.
    cv2.rectangle(image, bot_left, top_right, color=bg_color, thickness=-1)

    # Assign the font and get the boundary of the text.
    font = cv2.FONT_HERSHEY_PLAIN
    text_size = cv2.getTextSize(text, font, 1, 1)[0]

    # Get the text co-ordinates based on the boundary.
    if centered:
        # Center align the text content.
        tx = (width - text_size[0]) // 2 + (x - width // 2)
        ty = (height + text_size[1]) // 2 + (y - height // 2)
    else:
        # Left pad the text content.
        tx = x + 10
        ty = (height + text_size[1]) // 2 + y

    # Add the text, centered to the area.
    cv2.putText(image, text, (tx, ty), font, 1, text_color)

