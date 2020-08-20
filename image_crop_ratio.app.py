# -*- coding: utf-8 -*-

import numpy as np


def on_run(image: np.ndarray, roi: np.ndarray):
    x1, y1, x2, y2 = roi[:4]
    h, w = image.shape[:2]
    crop_y1 = int(h*y1)
    crop_y2 = int(h*y2)
    crop_x1 = int(w*x1)
    crop_x2 = int(w*x2)
    return {'output_image': image[crop_y1:crop_y2, crop_x1:crop_x2, :]}


if __name__ == '__main__':
    pass
