# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-06-01 09:01:20
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-06-01 09:06:38

from typing import List


def chunks(sequence, chunk_size: int = 5) -> List:
    # Делим массив на части
    res = []
    for item in sequence:
        res.append(item)
        if len(res) >= chunk_size:
            yield res
            res = []
    if res:
        yield res  # yield the last, incomplete, portion
