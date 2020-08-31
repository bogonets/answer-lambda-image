# -*- coding: utf-8 -*-
# @see <https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html>

import numpy as np

TYPE_ABSOLUTE = 'absolute'
TYPE_RATIO = 'ratio'

default_roi = []
roi = default_roi
point_type = TYPE_ABSOLUTE


def on_set(key, val):
    if key == 'roi':
        global roi
        global default_roi
        if not val:
            return

        rois = val.split('\n')

        try:
            roi = []
            for r in filter(lambda x: x, rois):
                roi.append(list(map(lambda x : float(x), r.split(','))))
            # sys.stderr.write((f'roi result : ({key}, {roi})'))
            # sys.stderr.flush()

        except Exception as e:
            roi = default_roi
    elif key == 'point_type':
        global point_type
        point_type = val


def on_get(key):
    if key == 'roi':
        # return ','.join(map(lambda x: str(x), roi))
        return str(roi)
    elif key == 'point_type':
        return point_type


def on_init():
    return True


def on_valid():
    return True


def on_run(preview):
    if not preview.shape:
        return {'roi': None}
    h, w, c = preview.shape

    result = roi
    if point_type == TYPE_ABSOLUTE:
        result = to_absolute(roi, w, h)
    return {
        "roi": np.array(result)
    }

def on_destroy():
    return True

def to_absolute(roi, width, height):
    return [[p * width if idx % 2 == 0 else p * height for idx, p in enumerate(r)] for r in roi]
