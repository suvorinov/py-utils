# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-06-22 11:17:35
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-06-22 11:18:28

from math import log


def human_sizeof(num: int) -> str:
    units = ["bytes", "kB", "MB", "GB", "TB", "PB"]
    decimals = [0, 0, 1, 2, 2, 2]
    if num == 0:
        return "0 bytes"
    if num == 1:
        return "1 byte"
    if num > 1:
        exponent = min(int(log(num, 1024)), len(units) - 1)
        quotient = float(num) / 1024 ** exponent
        unit = units[exponent]
        num_decimals = decimals[exponent]
        format_string = "{0:.%sf} {1}" % (num_decimals)
        return format_string.format(quotient, unit)
