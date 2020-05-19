# -*- coding: utf-8 -*-
# @see <https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html>

import numpy as np
import sys


def on_run(image, roi):

    shape = image.shape

    # sys.stdout.write(f"crop roi shape {shape}")
    # sys.stdout.write(f"roi: {roi}")
    # sys.stdout.flush()

    if len(shape) != 3:
        raise ValueError(f"The length of a image's shape must be 3! ({len(shape)})")

    if len(roi) != 4:
        raise ValueError(f"The length of roi must be 4! ({len(roi)})")

    rx1, ry1, rw, rh = roi

    rx2 = rx1 + rw
    ry2 = ry1 + rh

    if 0 > rx1 and rx1 >= 1:
        raise ValueError(f"ROI's x1 should be greater than or equal to 0 and less than 1 ({rx1})")
    
    if 0 > ry1 and ry1 >= 1:
        raise ValueError(f"ROI's y1 should be greater than or equal to 0 and less than 1 ({ry1})")

    if 0 >= rx2 and rx2 > 1:
        raise ValueError(f"ROI's x2 should be greater than 0 and less than or equal to 1 ({rx2})")

    if 0 >= ry2 and ry2 > 1:
        raise ValueError(f"ROI's y2 should be greater than 0 and less than or equal to 1 ({ry2})")

    h = shape[0]
    w = shape[1]
    
    real_x1 = int(w * rx1)
    real_y1 = int(h * ry1)
    real_x2 = int(w * rx2)
    real_y2 = int(h * ry2)

    # sys.stdout.write(f"real x1: {real_x1}, y1: {real_y1}, x2: {real_x2}, y2: {real_y2}")
    # sys.stdout.flush()

    return {
        "output_image": image[real_y1:real_y2, real_x1:real_x2, :]
    }


def on_destroy():
    return True


if __name__ == '__main__':
    pass
