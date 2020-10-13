# -*- coding: utf-8 -*-

import sys
import json
import base64
import numpy as np
import cv2


class JpegEncodeError(Exception):

    def __init__(self, *args):
        super().__init__('Jpeg encode error.')


class ManageRois:

    def __init__(self):
        self.rois: np.ndarray = np.empty(0)
        self.sizes: np.ndarray = np.empty(0)
        self.props: np.ndarray = np.empty(0)
        self.snaps: np.ndarray = np.empty(0)

    def set_rois(self, val: str):
        rois_list = json.loads(val)
        if not isinstance(rois_list, list):
            raise TypeError('Root json is not a list type.')

        points = []
        sizes = []
        for item in rois_list:
            if not isinstance(item, list):
                raise TypeError('list element is not a list type.')

            for x, y in zip(item[0::2], item[1::2]):
                points.append(float(x))
                points.append(float(y))
            sizes.append(int(len(item)/2))

        self.rois = np.array(points, dtype=float)
        self.sizes = np.array(sizes, dtype=float)

    def set_props(self, val: str):
        props_list = json.loads(val)
        if not isinstance(props_list, list):
            raise TypeError('Root json is not a list type.')

        props = []
        for item in props_list:
            if not isinstance(item, list):
                raise TypeError('list element is not a str type.')
            props.append([float(x) for x in item])

        self.props = np.array(props, dtype=float)

    def set_snaps(self, val: str):
        snaps_list = json.loads(val)
        if not isinstance(snaps_list, list):
            raise TypeError('Root json is not a list type.')

        snaps = []
        for item in snaps_list:
            if not isinstance(item, str):
                raise TypeError('list element is not a str type.')
            data = base64.b64decode(item.encode("UTF-8"))
            snaps.append(cv2.imdecode(data, cv2.IMREAD_COLOR))

        self.snaps = np.stack(snaps)

    def get_rois(self):
        begin = 0
        end = 0
        result = []

        for i in self.sizes:
            begin = end
            end = begin + i
            result.append(self.rois[begin:end].tolist())

        return json.dumps(result)

    def get_props(self):
        result = []
        for prop in self.props:
            result.append(prop.tolist())
        return json.dumps(result)

    def get_snaps(self):
        result = []
        for snap in self.snaps:
            ret, jpeg = cv2.imencode('.jpg', snap)
            if not ret:
                raise JpegEncodeError()
            result.append(base64.b64encode(jpeg.tobytes()).decode('UTF-8'))
        return json.dumps(result)

    def on_set(self, key, val):
        if key == 'rois':
            self.set_rois(val)
        elif key == 'props':
            self.set_props(val)
        elif key == 'snaps':
            self.set_snaps(val)

    def on_get(self, key):
        if key == 'rois':
            return self.get_rois()
        elif key == 'props':
            return self.get_props()
        elif key == 'snaps':
            return self.get_snaps()

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
