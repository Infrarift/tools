#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
<Description>
"""
import os

import cv2

from util import text
from util.logger import Logger
import numpy as np

from util.region import Region

__author__ = "Jakrin Juangbhanich"
__copyright__ = "Copyright 2018, GenVis Pty Ltd."
__email__ = "juangbhanich.k@gmail.com"
__version__ = "0.1.0"


def show_image(text_function):
    """ Decorator to copy the input image, process it, and then show it in a window. """

    def func_wrapper(original_image, text_display: str):
        new_image = np.copy(original_image)
        new_image = text_function(new_image, text_display)
        cv2.imshow("Text Demo", new_image)
        cv2.waitKey(-1)

    return func_wrapper


def create_region_with_padding(image: np.array, pad: int):
    region: Region = Region(left=pad, right=image.shape[1] - pad,
                            top=pad, bottom=image.shape[0] - pad)
    return region


@show_image
def plain_text(image: np.array, display_text: str):
    """ Render a text straight onto the image at the x and y position. """
    return text.write_to_image_raw(image=image, text=display_text, x=0, y=0)


# ======================================================================================================================
# Region based text rendering.
# ======================================================================================================================

@show_image
def region_text(image: np.array, display_text: str):
    """ Write text into the specified region, with the anchor. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  show_region_outline=True)


@show_image
def region_text_left(image: np.array, display_text: str):
    """ Write text into the specified region, with the anchor. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  pad=15,
                                  h_align=text.ALIGN_LEFT,
                                  show_region_outline=True)


@show_image
def region_with_bg(image: np.array, display_text: str):
    """ Write text into the specified region, with a solid BG. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  bg_color=(0, 0, 0))


@show_image
def region_with_clear_bg(image: np.array, display_text: str):
    """ Write text into the specified region, with a transparent BG. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  bg_color=(0, 0, 0),
                                  bg_opacity=0.5)


# ======================================================================================================================
# Icons.
# ======================================================================================================================


@show_image
def icon_raw(image: np.array, display_text: str):
    return text.write_icon_raw(image, display_text, x=0, y=0, font_size=48)


@show_image
def inline_icon_left(image: np.array, display_text: str):
    """ Write text into the specified region, with a transparent BG. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  icon=u"\uf447",
                                  pad=12,
                                  h_align=text.ALIGN_LEFT,
                                  show_region_outline=True)


@show_image
def inline_icon_center(image: np.array, display_text: str):
    """ Write text into the specified region, with a transparent BG. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  icon=u"\uf447",
                                  pad=12,
                                  show_region_outline=True)


# ======================================================================================================================
# Location based anchoring.
# ======================================================================================================================


@show_image
def write_centered_position(image: np.array, display_text: str):
    """ Write text into the specified region, with a transparent BG. """
    return text.write_centered_at(image=image, text=display_text, x=150, y=100, pad=15, bg_color=(0, 0, 0))


# ======================================================================================================================
# Run the script.
# ======================================================================================================================


if __name__ == "__main__":
    Logger.log_header("Running Text_Example")
    Logger.log_field("Version", __version__)

    # ===================================================================================================
    # New Version.
    # ===================================================================================================

    # Load the default image to draw on.
    module_dir = os.path.dirname(__file__)
    file_path = f"{module_dir}/resources/stars.jpeg"
    base_image = cv2.imread(file_path)

    plain_text(base_image, "Plain Text")
    region_text(base_image, "Region Centered")
    region_text_left(base_image, "Region Left")
    region_with_bg(base_image, "Region With BG")
    region_with_clear_bg(base_image, "Clear BG")
    icon_raw(base_image, u"\uf447")
    inline_icon_left(base_image, "Left Inline Icon")
    inline_icon_center(base_image, "Center Inline Icon")
    write_centered_position(base_image, "Centered at Position")

    # Draw an icon in any position.

    # Overlay a text.

    # Anchor a container to a specific part of the image (center, top, left, etc).

    # Specify text position with corner align or center align.

    # Region labelling.

    # ===================================================================================================
    # Legacy.
    # ===================================================================================================

    # base_image = np.zeros((200, 300, 3), dtype=np.uint8)
    #
    # image = np.copy(base_image)
    # image = text.write_to_image2(image=image, text="Clipped", x=0, y=0)
    # show(image)
    #
    # image = np.copy(base_image)
    # image = text.write_to_image2(image=image, text="Hello World")
    # show(image)
    #
    # image = np.copy(base_image)
    # image = text.write_to_image2(image=image, icon=u"\uf447", text="12345?", font_size=26, pad=12)
    # show(image)
    #
    # image = np.copy(base_image)
    # image = text.draw_icon(image, u"\uf447", size=42)
    # show(image)
    #
    # image = np.copy(base_image)
    # image = text.draw_icon(image, u"\uf447", size=42, y=20)
    # image = text.draw_icon(image, u"\uf447", size=42, y=70)
    # image = text.draw_icon(image, u"\uf447", size=42, y=120)
    # image = text.draw_icon(image, u"\uf447", size=42, y=170)
    # show(image)

    # ======================================================================================================================
    # Creating simple text boxes without an image context.
    # ======================================================================================================================

    # base_image = np.zeros((200, 300, 3), dtype=np.uint8)
    #
    # image = np.copy(base_image)
    # image = text.write_to_image2(image=image, text="Hello World")
    # show(image)
    #
    # image = np.copy(base_image)
    # image = text.write_to_image2(image=image, icon=u"\uf447", text="Left Aligned", h_align=text.ALIGN_LEFT)
    # show(image)
    #
    # image = np.copy(base_image)
    # image = text.write_to_image2(image=image, icon=u"\uf447", text="Right Aligned", h_align=text.ALIGN_RIGHT)
    # show(image)

    # ======================================================================================================================
    # Creating simple text boxes without an image context.
    # ======================================================================================================================

    # image = np.copy(base_image)
    # image = text.write_to_image2(image=image, text="BIG TEXT", font_size=42)
    # show(image)
    #
    # image = np.copy(base_image)
    # image = text.write_to_image2(image=image, text="SMALL TEXT", font_size=14)
    # show(image)

    # ======================================================================================================================
    # Drawing onto an existing image.
    # ======================================================================================================================

    # file_path = f"{os.path.dirname(__file__)}/resources/stars.jpeg"
    # base_image = cv2.imread(file_path)  # np.zeros((800, 600, 3), dtype=np.uint8)
    #
    # image = np.copy(base_image)
    # image = text.write_to_image2(image=image, text="Opacity BG", bg_opacity=0.5)
    # show(image)
    #
    # image = np.copy(base_image)
    # image = text.write_to_image2(image=image, text="Custom Position", x=100, y=80, h_align=text.ALIGN_CENTER)
    # show(image)
    #
    # image = np.copy(base_image)
    # image = text.write_to_image2(image=image, text="Custom Size", width=300, h_align=text.ALIGN_CENTER)
    # show(image)
    #
    # image = np.copy(base_image)
    # image = text.write_to_image2(image=image, text="Normal Color", font_size=28,
    #                              color=(0, 255, 0), bg_opacity=0.0)
    # show(image)
    #
    # image = np.copy(base_image)
    # image = text.write_to_image2(image=image, text="Overlay Color", font_size=28,
    #                              color=(0, 255, 0), bg_opacity=0.0, overlay=True)
    # show(image)

    # ======================================================================================================================
    # Region Mode.
    # ======================================================================================================================

    # base_image = np.zeros((600, 800, 3), dtype=np.uint8)
    # base_image[:] = (50, 50, 50)
    #
    # image = np.copy(base_image)
    # region = Region(300, 700, 100, 300)
    # cv2.rectangle(image, (region.left, region.top), (region.right, region.bottom), color=(0, 255, 0), thickness=2)
    # image = text.write_to_region(image, "Region Marker", region, icon=u"\uf447")
    # show(image)
    #
    # image = np.copy(base_image)
    # region = Region(200, 600, 100, 300)
    # cv2.rectangle(image, (region.left, region.top), (region.right, region.bottom), color=(0, 255, 0), thickness=2)
    # image = text.write_to_region(image, "Bottom Marker", region, show_at_top=False)
    # show(image)

    # ======================================================================================================================
    # Draw Icons.
    # ======================================================================================================================

    # base_image = np.zeros((200, 300, 3), dtype=np.uint8)
    #
    # image = np.copy(base_image)
    # image = text.draw_icon(image, u"\uf447")
    # show(image)

    # ======================================================================================================================
    # End the demo.
    # ======================================================================================================================

    cv2.destroyAllWindows()
