# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-01-17 12:40:27
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-01-17 12:41:24

import sys
import pathlib
import json
from typing import Tuple, Union


def read_json(file_name: pathlib.Path) -> Tuple[bool, Union[str, object]]:
    data = None
    try:
        with open(file_name, 'r', encoding='utf8') as inputfile:
            data = json.load(inputfile)
    except Exception:
        return False, f'{sys.exc_info()[1]}'
    return True, data
