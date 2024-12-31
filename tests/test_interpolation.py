import pytest
from projection.base.interpolation import BaseInterpolation
from projection.gnomonic.config import GnomonicConfig
from projection.exceptions import InterpolationError
import numpy as np
import cv2

def test_base_interpolation_apply_mask():
    config = GnomonicConfig()
    interpolation = BaseInterpolation(config)
    input_img = np.ones((2, 2, 3), dtype=np.uint8) * 255  # Correct shape to match broadcasting
    map_x = np.array([[0, 1], [0, 1]])
    map_y = np.array([[0, 1], [0, 1]])
    mask = np.array([[1, 0], [1, 0]], dtype=np.uint8)
    output_img = interpolation.interpolate(input_img, map_x, map_y, mask)
    assert np.array_equal(output_img, np.array([[[255, 255, 255], [0, 0, 0]], [[255, 255, 255], [0, 0, 0]]]))