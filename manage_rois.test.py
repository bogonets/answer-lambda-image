# -*- coding: utf-8 -*-

import unittest
import numpy as np
from base_lambda_tester import BaseLambdaTester

TEST_JSON = """{
    "0": {
        "points": [
            { "x": 1, "y": 2 },
            { "x": 3, "y": 4 }
        ],
        "property": {
            "greaterThanEnable": true,
            "greaterThanValue": 1,
            "lessThanEnable": false,
            "lessThanValue": 0,
            "withinRangeEnable": false,
            "withinRangeValue": { "max": 0, "min": 0 },
            "outOfRangeEnable": false,
            "outOfRangeValue": { "max": 0, "min": 0 },
            "thresholdEnable": false,
            "thresholdValue": 0,
            "rgbColorEnable": false,
            "rgbColorValue": { "b": 0, "g": 0, "r": 0 },
            "lineStyleColorEnable": false,
            "lineStyleColorValue": { "b": 0, "g": 0, "r": 0 }
        },
        "snapshotInBase64Jpeg": ""
    },
    "1": {
        "points": [
            { "x": 5, "y": 6 },
            { "x": 7, "y": 8 }
        ],
        "property": {
            "greaterThanEnable": false,
            "greaterThanValue": 0,
            "lessThanEnable": false,
            "lessThanValue": 0,
            "withinRangeEnable": false,
            "withinRangeValue": { "max": 0, "min": 0 },
            "outOfRangeEnable": false,
            "outOfRangeValue": { "max": 0, "min": 0 },
            "thresholdEnable": false,
            "thresholdValue": 0,
            "rgbColorEnable": true,
            "rgbColorValue": { "b": 0, "g": 0, "r": 1 },
            "lineStyleColorEnable": false,
            "lineStyleColorValue": { "b": 0, "g": 0, "r": 0 }
        },
        "snapshotInBase64Jpeg": ""
    }
}"""


class TestManageRois(unittest.TestCase):

    def __init__(self, test_method_name='runTest'):
        super().__init__(test_method_name)
        self.module = BaseLambdaTester('manage_rois')

    def setUp(self):
        self.module.set_dict(infos=TEST_JSON)
        self.assertTrue(self.module.init())
        self.assertTrue(self.module.valid())

    def tearDown(self):
        self.module.destroy()

    def test_default(self):
        result: dict = self.module.run(np.empty(0))
        rois: np.ndarray = result["rois"]
        sizes: np.ndarray = result["sizes"]
        props: np.ndarray = result["props"]
        snaps: np.ndarray = result["snaps"]

        expect_rois = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
        expect_sizes = np.array([2, 2], dtype=int)
        expect_props = np.array([[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]], dtype=float)
        expect_snaps = np.empty(0, dtype=np.uint8)

        self.assertTrue(np.all(rois == expect_rois))
        self.assertTrue(np.all(sizes == expect_sizes))
        self.assertTrue(np.all(props == expect_props))
        self.assertTrue(np.all(snaps == expect_snaps))


if __name__ == '__main__':
    unittest.main()
