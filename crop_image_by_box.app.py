import numpy as np
import sys

LOGGING_PREFIX = "[crop_image_by_box.app.py] "
LOGGING_SUFFIX = "\n"

def print_out(message):
    sys.stdout.write(LOGGING_PREFIX + message + LOGGING_SUFFIX)
    sys.stdout.flush()

def print_err(message):
    sys.stderr.write(LOGGING_PREFIX + message + LOGGING_SUFFIX)
    sys.stderr.flush()

def get_rect(r):
    return [r[0], r[1], r[2], r[3]]

def on_run(source: np.ndarray, bbox: np.ndarray):

    image_zip = []
    for by in bbox:
        x1, y1, x2, y2 = by[:4]
        h, w = source.shape[:2]
        crop_y1 = int(h*y1)
        crop_y2 = int(h*y2)
        crop_x1 = int(w*x1)
        crop_x2 = int(w*x2)

        a = source[crop_y1:crop_y2, crop_x1:crop_x2, :]
        image_zip.append(a)
    return {'result': np.array(image_zip)}

if __name__=='__main__':
    pass

