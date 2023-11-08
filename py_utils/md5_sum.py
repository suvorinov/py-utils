# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-01-16 20:09:52
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-05-19 16:17:27

import sys
import pathlib
import hashlib
from typing import Tuple


def md5_sum(file_path: pathlib.Path, block_size: int = 4096) -> Tuple[bool, str]: # noqa

    md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            while True:
                data = f.read(block_size)
                if not data:
                    break
                md5.update(data)
    except Exception:
        return False, f'{sys.exc_info()[1]}'
    return True, md5.hexdigest()
