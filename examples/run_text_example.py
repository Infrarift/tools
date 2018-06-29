#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
<Description>
"""
import cv2

from util import text
from util.logger import Logger
import numpy as np

from util.region import Region

__author__ = "Jakrin Juangbhanich"
__copyright__ = "Copyright 2018, GenVis Pty Ltd."
__email__ = "juangbhanich.k@gmail.com"
__version__ = "0.1.0"


def show(win_image: np.array):
    cv2.imshow("Text Demo", win_image)
    cv2.waitKey(-1)


if __name__ == "__main__":
    Logger.log_header("Running Text_Example")
    Logger.log_field("Version", __version__)

    base_image = np.zeros((200, 300, 3), dtype=np.uint8)

    image = np.copy(base_image)
    image = text.write_to_image2(image=image, text="Hello World")
    show(image)

    image = np.copy(base_image)
    image = text.write_to_image2(image=image, icon=u"\uf447", text="12345?", font_size=26, pad=12)
    show(image)

    image = np.copy(base_image)
    image = text.draw_icon(image, u"\uf447", size=42)
    show(image)

    image = np.copy(base_image)
    image = text.draw_icon(image, u"\uf447", size=42, y=20)
    image = text.draw_icon(image, u"\uf447", size=42, y=70)
    image = text.draw_icon(image, u"\uf447", size=42, y=120)
    image = text.draw_icon(image, u"\uf447", size=42, y=170)
    show(image)

    # ======================================================================================================================
    # Creating simple text boxes without an image context.
    # ======================================================================================================================

    base_image = np.zeros((200, 300, 3), dtype=np.uint8)

    image = np.copy(base_image)
    image = text.write_to_image2(image=image, text="Hello World")
    show(image)

    image = np.copy(base_image)
    image = text.write_to_image2(image=image, icon=u"\uf447", text="Left Aligned", h_align=text.ALIGN_LEFT)
    show(image)

    image = np.copy(base_image)
    image = text.write_to_image2(image=image, icon=u"\uf447", text="Right Aligned", h_align=text.ALIGN_RIGHT)
    show(image)

    # ======================================================================================================================
    # Creating simple text boxes without an image context.
    # ======================================================================================================================

    image = np.copy(base_image)
    image = text.write_to_image2(image=image, text="BIG TEXT", font_size=42)
    show(image)

    image = np.copy(base_image)
    image = text.write_to_image2(image=image, text="SMALL TEXT", font_size=14)
    show(image)

    # ======================================================================================================================
    # Drawing onto an existing image.
    # ======================================================================================================================

    base_image = cv2.imread("resources/stars.jpeg")  # np.zeros((800, 600, 3), dtype=np.uint8)

    image = np.copy(base_image)
    image = text.write_to_image2(image=image, text="Opacity BG", bg_opacity=0.5)
    show(image)

    image = np.copy(base_image)
    image = text.write_to_image2(image=image, text="Custom Position", x=100, y=80, h_align=text.ALIGN_CENTER)
    show(image)

    image = np.copy(base_image)
    image = text.write_to_image2(image=image, text="Custom Size", width=300, h_align=text.ALIGN_CENTER)
    show(image)

    image = np.copy(base_image)
    image = text.write_to_image2(image=image, text="Normal Color", font_size=28,
                                 color=(0, 255, 0), bg_opacity=0.0)
    show(image)

    image = np.copy(base_image)
    image = text.write_to_image2(image=image, text="Overlay Color", font_size=28,
                                 color=(0, 255, 0), bg_opacity=0.0, overlay=True)
    show(image)

    # ======================================================================================================================
    # Region Mode.
    # ======================================================================================================================

    base_image = np.zeros((600, 800, 3), dtype=np.uint8)
    base_image[:] = (50, 50, 50)

    image = np.copy(base_image)
    region = Region(300, 700, 100, 300)
    cv2.rectangle(image, (region.left, region.top), (region.right, region.bottom), color=(0, 255, 0), thickness=2)
    image = text.write_to_region(image, "Region Marker", region, icon=u"\uf447")
    show(image)

    image = np.copy(base_image)
    region = Region(200, 600, 100, 300)
    cv2.rectangle(image, (region.left, region.top), (region.right, region.bottom), color=(0, 255, 0), thickness=2)
    image = text.write_to_region(image, "Bottom Marker", region, show_at_top=False)
    show(image)

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
