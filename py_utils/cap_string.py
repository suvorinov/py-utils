# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-01-16 19:54:54
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-01-17 07:50:36


def cap_string(text: str) -> str:

    out = " ".join([word.capitalize() for word in text.split(" ")])
    return out
