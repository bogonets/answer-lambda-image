# -*- coding: utf-8 -*-

import numpy as np

snapshot_flag = False
snapshot_image = None


def on_set(key, val):
    if key == 'snapshot_flag':
        global snapshot_flag
        snapshot_flag = str(val).lower() in ['yes', 'y', 'true']


def on_get(key):
    if key == 'snapshot_flag':
        return snapshot_flag


def on_run(preview: np.ndarray):
    global snapshot_image
    global snapshot_flag

    if snapshot_flag:
        snapshot_image = preview.copy()
        snapshot_flag = False

    if snapshot_image is not None:
        return {'result': snapshot_image}
    else:
        return {}


if __name__ == '__main__':
    pass
