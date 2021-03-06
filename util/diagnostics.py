# -*- coding: utf-8 -*-

"""
recorder-node | diagnostics | 22/05/18
<Description>
"""

import json
from .logger import Logger

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


def show_size(name, obj):

    encoded_str = json.dumps(obj)
    obj_size = len(encoded_str.encode("utf-8"))
    readable_size = sizeof_fmt(obj_size)
    Logger.log_field("Size of {}".format(name), readable_size)


def sizeof_fmt(num):
    for unit in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, "B")
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', "B")
