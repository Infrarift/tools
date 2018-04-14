# -*- coding: utf-8 -*-

"""
clustering-research | pather | 11/04/18
Use this tool to create, clear, or guarantee that paths exist.
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import os
import shutil

__author__ = "Jakrin Juangbhanich"
__copyright__ = "Copyright 2018, GenVis Pty Ltd."
__email__ = "juangbhanich.k@gmail.com"
# GitHub: https://github.com/Infrarift


def create(path, clear=False):
    """
    Given some arbitrary path, we will create all the directory leading up to it.
    Optionally, we can also clear whatever is there.
    """
    head, tail = os.path.split(path)

    # Recursively create the heads.
    if head != "":
        create(head, clear)

    base, ext = os.path.splitext(tail)
    if ext == "":
        # No extension, this is supposed to be a directory.
        if os.path.exists(path) and clear:
            shutil.rmtree(path)

        if not os.path.exists(path):
            os.mkdir(path)

