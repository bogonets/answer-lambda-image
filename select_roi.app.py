# -*- coding: utf-8 -*-
# @see <https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html>

import numpy as np

default_roi = []
roi = default_roi


def on_set(key, val):
    if key == 'roi':
        global roi
        global default_roi
        if not val:
            return

        rois = val.split('\n')

        try:
            for r in filter(lambda x: x, rois):
                roi.append(list(map(lambda x : float(x), r.split(','))))
            # sys.stderr.write((f'roi result : ({key}, {roi})'))
            # sys.stderr.flush()
        except Exception as e:
            roi = default_roi


def on_get(key):
    if key == 'roi':
        return ','.join(map(lambda x: str(x), roi))


def on_init():
    return True


def on_valid():
    return True


def on_run(preview):
    return {
        "roi": np.array((roi[0], roi[1], roi[0]+roi[2], roi[1]+roi[3]), dtype=np.float32)
    }


def on_destroy():
    return True


if __name__ == '__main__':
    pass
