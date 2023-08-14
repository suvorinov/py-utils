# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2022-12-29 14:21:08
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-01-17 07:40:23

import sys
import pathlib
import json
from typing import Tuple


def write_json(data: object, file_name: pathlib.Path) -> Tuple[bool, str]:
    """Creating all parent directories if they don't exist."""
    p = pathlib.PurePath(file_name)
    pathlib.Path(p.parent).mkdir(parents=True, exist_ok=True)

    try:
        with open(file_name, 'w', encoding='utf8') as outfile:
            json.dump(data, outfile,
                      sort_keys=False, separators=(',', ': '),
                      indent=4, ensure_ascii=False)
    except Exception:
        return False, f'{sys.exc_info()[1]}'
    return True, None
