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


class JpegEncodeError(Exception):

    def __init__(self, *args):
        super().__init__('Jpeg encode error.')


class ManageRois:

    def __init__(self):
        self.rois: np.ndarray = np.empty(0)
        self.sizes: np.ndarray = np.empty(0)
        self.props: np.ndarray = np.empty(0)
        self.snaps: np.ndarray = np.empty(0)

    # def set_rois(self, val: str):
    #     rois_list = json.loads(val)
    #     if not isinstance(rois_list, list):
    #         raise TypeError('Root json is not a list type.')
    #
    #     points = []
    #     sizes = []
    #     for item in rois_list:
    #         if not isinstance(item, list):
    #             raise TypeError('list element is not a list type.')
    #
    #         for x, y in zip(item[0::2], item[1::2]):
    #             points.append(float(x))
    #             points.append(float(y))
    #         sizes.append(int(len(item)/2))
    #
    #     self.rois = np.array(points, dtype=float)
    #     self.sizes = np.array(sizes, dtype=float)
    #
    # def set_props(self, val: str):
    #     props_list = json.loads(val)
    #     if not isinstance(props_list, list):
    #         raise TypeError('Root json is not a list type.')
    #
    #     props = []
    #     for item in props_list:
    #         if not isinstance(item, list):
    #             raise TypeError('list element is not a str type.')
    #         props.append([float(x) for x in item])
    #
    #     self.props = np.array(props, dtype=float)
    #
    # def set_snaps(self, val: str):
    #     snaps_list = json.loads(val)
    #     if not isinstance(snaps_list, list):
    #         raise TypeError('Root json is not a list type.')
    #
    #     snaps = []
    #     for item in snaps_list:
    #         if not isinstance(item, str):
    #             raise TypeError('list element is not a str type.')
    #         data = base64.b64decode(item.encode("UTF-8"))
    #         snaps.append(cv2.imdecode(data, cv2.IMREAD_COLOR))
    #
    #     self.snaps = np.stack(snaps)

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
        ret, jpeg = cv2.imencode('.jpg', image)
        if not ret:
            raise JpegEncodeError()
        return base64.b64encode(jpeg.tobytes()).decode('UTF-8')

    @staticmethod
    def decode_from_base64_jpeg(base64_text: str) -> np.ndarray:
        if not base64_text:
            return np.empty(0, dtype=np.uint8)
        data = base64.b64decode(base64_text.encode("UTF-8"))
        return cv2.imdecode(data, cv2.IMREAD_COLOR)

    @staticmethod
    def encode_to_properties(props: np.ndarray) -> dict:
        return {
            greaterThanEnable: props[0] == 1,
            greaterThanValue: float(props[1]),
            lessThanEnable: props[2] == 1,
            lessThanValue: float(props[3]),
            withinRangeEnable: props[4] == 1,
            withinRangeValue: {
                "min": float(props[5]),
                "max": float(props[6])
            },
            outOfRangeEnable: props[7] == 1,
            outOfRangeValue: {
                "min": float(props[8]),
                "max": float(props[9])
            },
            thresholdEnable: props[10] == 1,
            thresholdValue: float(props[11]),
            rgbColorEnable: props[12] == 1,
            rgbColorValue: {
                "r": float(props[13]),
                "g": float(props[14]),
                "b": float(props[15])
            },
            lineStyleColorEnable: props[16] == 1,
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
            result[str(i)] = {
                "points": [{"x": p[0], "y": p[1]} for p in rois[i]],
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
