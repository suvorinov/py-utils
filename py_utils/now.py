# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-01-16 20:20:58
# @Last Modified by:   Suvorinov Oleg
# @Last Modified time: 2023-02-04 18:01:03

import datetime as dt


def now() -> str:
    return dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # noqa