# -*- coding: utf-8 -*-
# @Author: Suvorinov Oleg <olegsuvorinov@me.com>
# @Date:   2023-04-07 15:07:06
# @Last Modified by:   suvorinov
# @Last Modified time: 2023-04-20 16:14:45

import time


def print_duration(method):
    """Prints out the runtime duration of a method in seconds
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r %2.2f sec' % (method.__name__, te - ts))
        return result
    return timed
