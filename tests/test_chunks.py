# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-06-01 09:15:25
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-06-01 09:19:20

from py_utils.chunks import chunks

lst = list(range(53))
for item in chunks(lst):
    print(item)
