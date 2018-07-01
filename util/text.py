# -*- coding: utf-8 -*-

"""
<Description>
"""
import os
from typing import List, Tuple, Dict
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from . import visual
from .region import Region

__author__ = "Jakrin Juangbhanich"
__copyright__ = "Copyright 2018, GenVis Pty Ltd."
__email__ = "juangbhanich.k@gmail.com"

# ======================================================================================================================
# Constants.
# ======================================================================================================================


ALIGN_LEFT = -1
ALIGN_CENTER = 0
ALIGN_RIGHT = 1

FONT_DEFAULT = "DEFAULT"
FONT_ICON = "ICON"


# ======================================================================================================================
# This will manage the PIL TrueType fonts.
# ======================================================================================================================


class TextManager:
    INSTANCE = None

    def __init__(self):

        self.base_path = os.path.join(os.path.dirname(__file__), "fonts")
        self.fonts_by_size: Dict[int, dict] = {}

        self.font_path_map: Dict[str, str] = {
            FONT_DEFAULT: "RobotoMono-Medium.ttf",
            FONT_ICON: "fa-solid-900.ttf"
        }

    @staticmethod
    def instance() -> 'TextManager':
        if TextManager.INSTANCE is None:
            TextManager.INSTANCE = TextManager()
        return TextManager.INSTANCE

    @staticmethod
    def get_font(font_type: str = FONT_DEFAULT, font_size_id: int = 18):
        text_manager = TextManager.instance()
        text_manager._load_font(font_type, font_size_id)
        return text_manager.fonts_by_size[font_size_id][font_type]

    def _load_font(self, font_type: str = FONT_DEFAULT, size: int = 18):
        if size not in self.fonts_by_size:
            self.fonts_by_size[size] = {}

        font_dict = self.fonts_by_size[size]
        if font_type not in font_dict:
            font_path = os.path.join(self.base_path, self.font_path_map[font_type])
            font_dict[font_type] = ImageFont.truetype(font_path, size)


def get_text_size(text: str, font_type: str=FONT_DEFAULT, font_size: int=16):
    """ Returns the width and height for this text. """
    font = TextManager.get_font(font_type=font_type, font_size_id=font_size)
    return font.getsize(text)


def create_v2_text_box(text: str, width: int, height: int,
                       color=(255, 255, 255),
                       box_color=(0, 0, 0),
                       h_align: int = ALIGN_CENTER,
                       pad: int = 10,
                       font_size: int = 18):
    """ Create a new box with the specified dimensions, and draw a text inside. Color is BGR format. """

    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = box_color
    image = write_to_image(image, text, color=color, h_align=h_align, pad=pad, font_size=font_size)
    return image


def draw_icon(image, icon, x=None, y=None, size=24, h_align=ALIGN_CENTER, pad: int=0):
    icon_image = write_to_image(image, icon, font_size=size, font_type=FONT_ICON, x=x, y=y,
                                h_align=h_align, pad=pad)
    return icon_image


def write_to_region(image: np.array,
                    text: str,
                    region: Region,
                    pad: int = 10,
                    font_size: int = 18,
                    color=(255, 255, 255),
                    bg_color=(0, 0, 0),
                    bg_opacity=1.0,
                    overlay: bool = False,
                    gap: int = 10,
                    show_at_top: bool=True,
                    icon: str = None
                    ):

    # Prepare the font.
    fnt = TextManager.get_font(font_type=FONT_DEFAULT, font_size_id=font_size)
    _, text_height = fnt.getsize(text)

    x = region.x
    if show_at_top:
        y = region.top - (text_height + pad * 2) // 2 - gap
    else:
        y = region.bottom + (text_height + pad * 2) // 2 + gap

    write_image = write_to_image2(image=image, text=text, x=x, y=y, width=region.width, h_align=ALIGN_CENTER, pad=pad,
                                  font_size=font_size, color=color, bg_color=bg_color, bg_opacity=bg_opacity,
                                  overlay=overlay, icon=icon)

    return write_image


def write_to_image2(image: np.array,
                    text: str,
                    x: int = None,
                    y: int = None,
                    width: int = None,
                    height: int = None,
                    icon: str = None,
                    h_align: int = ALIGN_CENTER,
                    pad: int = 10,
                    font_size: int = 18,
                    color=(255, 255, 255),
                    bg_color=(0, 0, 0),
                    bg_opacity=1.0,
                    overlay: bool = False):

    # Find the missing parameters.
    auto_width: bool = False

    if width is None or height is None:
        # Prepare the font.
        text_width, text_height = get_text_size(text, FONT_DEFAULT, font_size)

        if width is None:
            auto_width = True
            width = text_width + pad * 2
            if icon is not None:
                icon_width, _ = get_text_size(icon, FONT_ICON, font_size)
                width += icon_width + pad

        if height is None:
            height = text_height + pad * 2

    if x is None:
        if h_align == ALIGN_LEFT:
            x = 0
        else:
            x = image.shape[1] // 2

    if y is None:
        y = image.shape[0] // 2

    # Find the aligned anchors.

    left = x
    top = y - height // 2

    if h_align == ALIGN_CENTER:
        left = x - width // 2

    if h_align == ALIGN_RIGHT:
        left = image.shape[1] - width

    right = left + width
    bottom = top + height

    # Create a sub-image to draw on.
    sub_image = visual.safe_extract(image, left, right, top, bottom)

    # Set the BG Color.
    if bg_color is not None and bg_opacity > 0:
        r_opacity = 1.0 - bg_opacity
        bg_box = np.zeros_like(sub_image)
        bg_box[:] = bg_color
        sub_image = cv2.addWeighted(sub_image, r_opacity, bg_box, bg_opacity, 0.0)

    # Write the image, accounting for overlay mode.
    if overlay:
        overlay_image = np.zeros_like(sub_image)
        overlay_image = write_to_image(overlay_image,
                                       text=text, color=color, h_align=h_align, pad=pad, font_size=font_size)

        text_image = cv2.addWeighted(sub_image, 1.0, overlay_image, 1.0, 0.0)

    else:
        x_offset = 0
        if icon is not None:
            sub_image = draw_icon(sub_image, icon=icon, size=font_size, h_align=ALIGN_LEFT, pad=pad)
            icon_width, _ = get_text_size(icon, FONT_ICON, font_size)

            if h_align == ALIGN_LEFT:
                x_offset = icon_width + pad
            if h_align == ALIGN_CENTER and auto_width:
                x_offset = (icon_width + pad) // 2

        text_image = write_to_image(sub_image,
                                        text=text, color=color, h_align=h_align, pad=pad, font_size=font_size,
                                        x_offset=x_offset)

    image = visual.safe_implant(image, text_image, left, right, top, bottom)
    # cv2.rectangle(image, (left, top), (right, bottom), color=(50, 50, 50), thickness=1)
    return image


def write_to_image(image: np.array,
                   text: str,
                   x_offset: int = 0,
                   x: int = None,
                   y: int = None,
                   color=(255, 255, 255),
                   h_align: int = ALIGN_CENTER,
                   pad: int = 10,
                   font_size: int = 18,
                   font_type: str = FONT_DEFAULT):
    # Create CV2 Image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image)

    frame_width = image.shape[1]
    frame_height = image.shape[0]

    # Prepare the font.
    font = TextManager.get_font(font_type=font_type, font_size_id=font_size)
    text_width, text_height = font.getsize(text)
    fy_offset = 2 if font_type == FONT_ICON else 1.8

    # Set the position.
    if y is None:
        y = frame_height // 2

    # Position the text.
    anchor_x = _get_aligned_anchor(frame_width, text_width, h_align, pad, x) + x_offset
    anchor_y = y - text_height / fy_offset  # Because text bounding box isn't great, small height offset.
    d.text((anchor_x, anchor_y), text, font=font, fill=(color[2], color[1], color[0]))

    # Convert back to cv2 format.
    final_image = np.array(pil_image)
    final_image = cv2.cvtColor(final_image, cv2.COLOR_RGB2BGR)

    if False:
        x1 = int(anchor_x)
        x2 = int(anchor_x + text_width)
        y1 = int(anchor_y)
        y2 = int(anchor_y + text_height)

        cv2.rectangle(final_image, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=1)
    return final_image


def _get_aligned_anchor(frame_size: int, text_size: int, align: int, pad: int = 0, position: int = None) -> int:
    """ Find the text anchor position. """

    if align == ALIGN_CENTER:
        if position is None:
            position = frame_size // 2
        return position - text_size // 2

    if align == ALIGN_LEFT:
        if position is None:
            position = 0
        return position + pad

    if align == ALIGN_RIGHT:
        if position is None:
            position = frame_size
        return position - text_size - pad

