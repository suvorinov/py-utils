# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-01-16 20:22:26
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-01-16 20:22:31

def clear_string(clear: str) -> str:
    clear = clear.encode("ascii", "ignore")
    return clear.decode().strip()
