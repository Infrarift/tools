# -*- coding: utf-8 -*-

"""
Draw good looking text to Cv2/Numpy images. Cv2's default text renderer is a bit ugly. I can't
specify the font, and not all sizes look great. Here I use PIL with Cv2 to get ttf fonts into the jam,
and also include support for the FontAwesome icon fonts.
"""

import os
from typing import List, Tuple, Dict
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from . import visual
from .region import Region

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"

# ======================================================================================================================
# Constants.
# ======================================================================================================================


ALIGN_LEFT = -1
ALIGN_CENTER = 0
ALIGN_RIGHT = 1

FONT_DEFAULT = "DEFAULT"
FONT_ICON = "ICON"

DEFAULT_PAD: int = 8


# ======================================================================================================================
# This will manage the PIL TrueType fonts.
# ======================================================================================================================


class TextManager:
    # TODO: I might want to create a way to custom initialize this Singleton.
    # Then I can maybe specify things like custom fonts, etc.

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


# ===================================================================================================
# Higher level text rendering functions.
# ===================================================================================================


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


def draw_icon(image, icon, x=None, y=None, size=24, h_align=ALIGN_CENTER, pad: int = 0):
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
                    show_at_top: bool = True,
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


# ===================================================================================================
# Low level text rendering function.
# ===================================================================================================


def write_to_image_raw(
        image: np.array,
        text: str,
        x: int,
        y: int,
        font_type: str = FONT_DEFAULT,
        font_size: int = 18,
        color=(255, 255, 255)
):
    """ Draw the specified text into the image at the point of the region. """

    # Convert image from CV2 to PIL.
    pil_image, pil_draw = _cv2_to_pil(image)

    # Prepare the font.
    font = TextManager.get_font(font_type=font_type, font_size_id=font_size)

    # Prepare the anchors.
    anchor_x = x
    anchor_y = y

    # Draw the text straight into the region.
    pil_draw.text((anchor_x, anchor_y), text, font=font, fill=(color[2], color[1], color[0]))

    # Convert image from PIL back to CV2.
    final_image = _pil_to_cv2(pil_image)
    return final_image


def write_icon_raw(
        image: np.array,
        text: str,
        x: int,
        y: int,
        font_size: int = 18,
        color=(255, 255, 255)
):
    """ Write a raw icon to the specified location. """
    return write_to_image_raw(image, text, x, y, font_type=FONT_ICON, font_size=font_size, color=color)


def write_into_region(
        image: np.array,
        text: str,
        region: Region,
        icon: str = None,  # Inline icon to render.
        pad: int = 0,
        h_align: int = ALIGN_CENTER,
        font_type: str = FONT_DEFAULT,
        font_size: int = 18,
        color=(255, 255, 255),
        bg_color=None,
        bg_opacity=1.0,
        show_region_outline: bool = False,
        fixed_width: bool = False  # If the width of the region was fixed from outside. Used to align the icon.
):
    """ The text will be written into this specified region.
    The y position will be centered. The x position will depend on the align type. """

    # Draw the BG into position.
    image = _fill_region(image, region, bg_color=bg_color, bg_opacity=bg_opacity)

    # Use the region to find the position.
    t_width, t_height = get_text_size(text, font_type, font_size)
    i_width, i_height = (0, 0) if icon is None else get_text_size(icon, FONT_ICON, font_size)
    b_width, b_height = (t_width, t_height) if icon is None else (t_width + i_width + pad, max(t_height, i_height))

    # Default case is central align.
    ix = region.x - b_width // 2
    iy = region.y - i_height // 2
    ty = region.y - t_height // 2
    tx = region.x - t_width // 2

    # Left align case.
    if h_align == ALIGN_LEFT or fixed_width:
        ix = region.left if icon is None else region.left + pad

    # Align the text to the icon.
    if h_align == ALIGN_LEFT or (not fixed_width and icon is not None):
        tx = ix + i_width + pad

    # Write the text.
    image = write_to_image_raw(image=image, text=text, x=tx, y=ty, font_type=font_type, font_size=font_size,
                               color=color)

    if icon is not None:
        image = write_icon_raw(image=image, text=icon, x=ix, y=iy, font_size=font_size, color=color)

    # Show an outline around the region.
    if show_region_outline:
        cv2.rectangle(image, (region.left, region.top), (region.right, region.bottom), color=(0, 255, 0), thickness=1)

    return image


# ======================================================================================================================
# Higher level function.
# ======================================================================================================================


def write_centered_at(
        image: np.array,
        text: str,
        x: int = 0,
        y: int = 0,
        width: int = None,
        height: int = None,
        icon: str = None,
        pad: int = 0,
        font_type: str = FONT_DEFAULT,
        font_size: int = 18,
        color=(255, 255, 255),
        bg_color=None,
        bg_opacity=1.0,
):
    """ Create a center-locked region, with the specified width and height. """
    region: Region = Region(0, 10, 0, 10)
    is_fixed_width = False

    # Get the meta-data of the text boxes.
    t_width, t_height = get_text_size(text, font_type, font_size)
    i_width, i_height = (0, 0) if icon is None else get_text_size(icon, FONT_ICON, font_size)
    b_width, b_height = (t_width, t_height) if icon is None else (t_width + i_width + pad, max(t_height, i_height))

    # Finalize the region width and height.
    if width is not None:
        region.width = width
        is_fixed_width = True
    else:
        region.width = b_width
    region.height = height if height is not None else b_height

    # Expand for the padding.
    region.width += pad * 2
    region.height += pad * 2
    region.x = x
    region.y = y

    # Draw the text.
    image = write_into_region(image=image, text=text, region=region, icon=icon, pad=pad, h_align=ALIGN_CENTER,
                              font_type=font_type, font_size=font_size, color=color, bg_color=bg_color,
                              bg_opacity=bg_opacity, show_region_outline=False, fixed_width=is_fixed_width)

    return image


def write_to_image2(image: np.array,
                    text: str,
                    x: int = None,
                    y: int = None,
                    width: int = None,
                    height: int = None,
                    h_align: int = ALIGN_CENTER,
                    pad: int = 10,
                    font_type: str = FONT_DEFAULT,
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


# ===================================================================================================
# Support Functions.
# ===================================================================================================


def get_text_size(text: str, font_type: str = FONT_DEFAULT, font_size: int = 16):
    """ Returns the width and height for this text, font and size. """
    font = TextManager.get_font(font_type=font_type, font_size_id=font_size)
    return font.getsize(text)


def _fill_region(image: np.array, region: Region, bg_color=None, bg_opacity: float = 1.0):
    """ Fill the region in this image with a color and opacity. """

    # No color or opacity is clear, do nothing.
    if bg_color is None or bg_opacity <= 0.0:
        return image

    # Opacity 1, just draw it onto the image.
    if bg_opacity >= 1.0:
        cv2.rectangle(image, (region.left, region.top), (region.right, region.bottom), color=bg_color, thickness=-1)
        return image

    # Opacity is semi-clear. Draw it in a different image and overlay it on.
    overlay_image = np.copy(image)
    cv2.rectangle(overlay_image, (region.left, region.top), (region.right, region.bottom), color=bg_color, thickness=-1)
    return cv2.addWeighted(image, 1.0 - bg_opacity, overlay_image, bg_opacity, 0.0)


def _cv2_to_pil(image: np.array) -> (Image, ImageDraw):
    """ Convert from a PIL ImageDraw to Cv2 Numpy. """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)
    image_draw = ImageDraw.Draw(pil_image)
    return pil_image, image_draw


def _pil_to_cv2(image: Image) -> np.array:
    """ Convert from a PIL ImageDraw back to Cv2 Numpy. """
    out_image = np.array(image)
    out_image = cv2.cvtColor(out_image, cv2.COLOR_RGB2BGR)
    return out_image


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
