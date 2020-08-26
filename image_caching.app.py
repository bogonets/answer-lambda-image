# -*- coding: utf-8 -*-
# @see <https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html>

import numpy as np
import cv2
import sys

filename = "sample.jpg"


def on_run(preview):
    cv2.imwrite(filename, preview)

def on_destroy():
    return True
