# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-01-16 20:09:52
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-01-16 20:10:29

import hashlib


def md5_key(clean: str) -> str:
    return hashlib.md5(clean.encode('utf-8')).hexdigest()
