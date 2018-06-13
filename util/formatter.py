# -*- coding: utf-8 -*-

"""
Use this to format string and data into more useful, or human readable types.
"""

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


def front_pad_string(string, length: int = 2, char: str = "0") -> str:
    """ Front pad a string with a certain char if it isn't already at least a given length long. """
    string = str(string)  # Cast whatever this is into a string.
    while len(string) < length:
        string = char + string
    return string
