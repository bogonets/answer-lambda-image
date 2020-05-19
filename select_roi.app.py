# -*- coding: utf-8 -*-
# @see <https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html>

import numpy as np
import sys

default_roi = (0., 0., 1., 1.)
roi = default_roi


def on_set(key, val):
    # sys.stderr.write((f'on_set({key}, {val})'))
    # sys.stderr.flush()
    if key == 'roi':
        global roi
        global default_roi
        try:
            roi = list(map(lambda x : float(x), val.split(',')))
            # sys.stderr.write((f'roi result : ({key}, {roi})'))
            # sys.stderr.flush()
        except Exception as e:
            # sys.stderr.write(e)
            # sys.stderr.flush()
            roi = default_roi


def on_get(key):
    if key == 'roi':
        return ','.join(map(lambda x: str(x), roi))


def on_create():
    return True


def on_init():
    return True


def on_valid():
    return True


def on_run(preview):
    return {
        "roi": np.array(roi, dtype=np.float32)
    }


def on_destroy():
    return True


if __name__ == '__main__':
    pass
