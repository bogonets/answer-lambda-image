# -*- coding: utf-8 -*-

import sys
import json
import base64
import numpy as np
import cv2
from typing import List

greaterThanEnable = "greaterThanEnable"
greaterThanValue = "greaterThanValue"
lessThanEnable = "lessThanEnable"
lessThanValue = "lessThanValue"
withinRangeEnable = "withinRangeEnable"
withinRangeValue = "withinRangeValue"
outOfRangeEnable = "outOfRangeEnable"
outOfRangeValue = "outOfRangeValue"
thresholdEnable = "thresholdEnable"
thresholdValue = "thresholdValue"
rgbColorEnable = "rgbColorEnable"
rgbColorValue = "rgbColorValue"
lineStyleColorEnable = "lineStyleColorEnable"
lineStyleColorValue = "lineStyleColorValue"

JPEG_BASE64_MIME_PREFIX = "data:image/jpeg;base64,"
LOGGING_PREFIX = '[manage_rois] '
LOGGING_SUFFIX = '\n'


def print_out(message):
    sys.stdout.write(LOGGING_PREFIX + message + LOGGING_SUFFIX)
    sys.stdout.flush()


def print_error(message):
    sys.stderr.write(LOGGING_PREFIX + message + LOGGING_SUFFIX)
    sys.stderr.flush()


class JpegEncodeError(Exception):

    def __init__(self, *args):
        super().__init__('Jpeg encode error.')


class ManageRois:

    def __init__(self):
        self.rois: np.ndarray = np.empty(0)
        self.sizes: np.ndarray = np.empty(0)
        self.props: np.ndarray = np.empty(0)
        self.snaps: np.ndarray = np.empty(0)

    def to_rois(self):
        size = self.sizes.size
        if size == 0:
            return []

        begin = 0
        end = self.sizes[0]
        result = [self.rois[begin:end].tolist()]

        for i in self.sizes[1:]:
            begin = end
            end = begin + i
            result.append(self.rois[begin:end].tolist())
        return result

    @staticmethod
    def encode_to_base64_jpeg(image: np.ndarray) -> str:
        if image is None or image.size == 0:
            return ''
        ret, jpeg = cv2.imencode('.jpg', image)
        if not ret:
            raise JpegEncodeError()
        result = base64.b64encode(jpeg.tobytes()).decode('UTF-8')
        if not result:
            return ''
        return JPEG_BASE64_MIME_PREFIX + result

    @staticmethod
    def decode_from_base64_jpeg(base64_text: str) -> np.ndarray:
        if not base64_text:
            return np.empty(0, dtype=np.uint8)
        if JPEG_BASE64_MIME_PREFIX != base64_text[0:len(JPEG_BASE64_MIME_PREFIX)]:
            return np.empty(0, dtype=np.uint8)
        jpeg = base64.b64decode(base64_text[len(JPEG_BASE64_MIME_PREFIX):].encode("UTF-8"))
        data = np.frombuffer(jpeg, dtype=np.uint8)
        return cv2.imdecode(data, cv2.IMREAD_COLOR)

    @staticmethod
    def encode_to_properties(props: np.ndarray) -> dict:
        return {
            greaterThanEnable: bool(int(props[0]) != 0),
            greaterThanValue: float(props[1]),
            lessThanEnable: bool(int(props[2]) != 0),
            lessThanValue: float(props[3]),
            withinRangeEnable: bool(int(props[4]) != 0),
            withinRangeValue: {
                "min": float(props[5]),
                "max": float(props[6])
            },
            outOfRangeEnable: bool(int(props[7]) != 0),
            outOfRangeValue: {
                "min": float(props[8]),
                "max": float(props[9])
            },
            thresholdEnable: bool(int(props[10]) != 0),
            thresholdValue: float(props[11]),
            rgbColorEnable: bool(int(props[12]) != 0),
            rgbColorValue: {
                "r": float(props[13]),
                "g": float(props[14]),
                "b": float(props[15])
            },
            lineStyleColorEnable: bool(int(props[16]) != 0),
            lineStyleColorValue: {
                "r": float(props[17]),
                "g": float(props[18]),
                "b": float(props[19])
            }
        }

    @staticmethod
    def decode_from_properties(obj: dict) -> np.ndarray:
        return np.array([
            1.0 if obj[greaterThanEnable] else 0.0,
            float(obj[greaterThanValue]),
            1.0 if obj[lessThanEnable] else 0.0,
            float(obj[lessThanValue]),
            1.0 if obj[withinRangeEnable] else 0.0,
            float(obj[withinRangeValue]["min"]),
            float(obj[withinRangeValue]["max"]),
            1.0 if obj[outOfRangeEnable] else 0.0,
            float(obj[outOfRangeValue]["min"]),
            float(obj[outOfRangeValue]["max"]),
            1.0 if obj[thresholdEnable] else 0.0,
            float(obj[thresholdValue]),
            1.0 if obj[rgbColorEnable] else 0.0,
            float(obj[rgbColorValue]["r"]),
            float(obj[rgbColorValue]["g"]),
            float(obj[rgbColorValue]["b"]),
            1.0 if obj[lineStyleColorEnable] else 0.0,
            float(obj[lineStyleColorValue]["r"]),
            float(obj[lineStyleColorValue]["g"]),
            float(obj[lineStyleColorValue]["b"]),
        ], dtype=float)

    def set_infos(self, val: str):
        infos = json.loads(val)
        rois = []
        sizes = []
        props = []
        snaps = []

        for index in sorted(infos.keys()):
            for p in infos[index]["points"]:
                rois.append(p["x"])
                rois.append(p["y"])
            sizes.append(len(infos[index]["points"]))
            props.append(ManageRois.decode_from_properties(infos[index]["property"]))
            snaps.append(ManageRois.decode_from_base64_jpeg(infos[index]["snapshotInBase64Jpeg"]))

        self.rois = np.array(rois, dtype=float)
        self.sizes = np.array(sizes, dtype=int)
        self.props = np.stack(props)
        self.snaps = np.stack(snaps)

    def get_infos(self):
        result = {}
        rois = self.to_rois()
        for i in range(self.sizes.size):
            xs = rois[i][0::2]
            ys = rois[i][1::2]
            result[str(i)] = {
                "points": [{"x": float(x), "y": float(y)} for x, y in zip(xs, ys)],
                "property": ManageRois.encode_to_properties(self.props[i]),
                "snapshotInBase64Jpeg": ManageRois.encode_to_base64_jpeg(self.snaps[i])
            }
        return json.dumps(result)

    def on_set(self, key, val):
        if key == 'infos':
            self.set_infos(val)

    def on_get(self, key):
        if key == 'infos':
            return self.get_infos()

    def on_run(self, preview: np.ndarray):
        return {
            "rois": self.rois,
            "sizes": self.sizes,
            "props": self.props,
            "snaps": self.snaps,
        }


MAIN_HANDLER = ManageRois()


def on_set(key, val):
    MAIN_HANDLER.on_set(key, val)


def on_get(key):
    return MAIN_HANDLER.on_get(key)


def on_run(preview: np.ndarray):
    return MAIN_HANDLER.on_run(preview)


if __name__ == '__main__':
    pass
