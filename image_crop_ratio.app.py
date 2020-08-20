# -*- coding: utf-8 -*-

import numpy as np
import sys


LOGGING_PREFIX = '[image.crop_ratio] '
LOGGING_SUFFIX = '\n'

verbose = False


def print_out(message):
    sys.stdout.write(LOGGING_PREFIX + message + LOGGING_SUFFIX)
    sys.stdout.flush()


def on_run(image: np.ndarray, roi: np.ndarray):
    x1, y1, x2, y2 = roi[:4]
    h, w = image.shape[:2]
    crop_y1 = int(h*y1)
    crop_y2 = int(h*y2)
    crop_x1 = int(w*x1)
    crop_x2 = int(w*x2)

    if verbose:
        print_out(f'image shape: {image.shape}')
        print_out(f'roi: [{x1}, {y1}, {x2}, {y2}]')

    return {'output_image': image[crop_y1:crop_y2, crop_x1:crop_x2, :]}


if __name__ == '__main__':
    pass
